import json
import logging
from datetime import datetime, timedelta
from typing import List, Dict, Optional
import time

from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

from .config import settings
from .exceptions import ChannelNotFoundError

logger = logging.getLogger(__name__)


class SlackCleaner:
    def __init__(self, token: Optional[str] = None):
        """Initialize the Slack cleaner with bot token."""
        self.client = WebClient(token=token or settings.slack_token)

    def list_channels(self) -> List[Dict[str, str]]:
        """Get list of available channels."""
        try:
            response = self.client.conversations_list()
            return [
                {"id": channel["id"], "name": channel["name"]}
                for channel in response["channels"]
            ]
        except SlackApiError as e:
            logger.error(f"Error listing channels: {str(e)}")
            raise

    def delete_messages(
        self,
        channel_id: str,
        search_phrase: str,
        hours_to_look_back: int = None,
        interactive: bool = True,
    ) -> int:
        """Delete messages containing specified phrase from the selected channel."""
        try:
            self._verify_channel(channel_id)

            hours = hours_to_look_back or settings.default_hours
            messages_to_delete = self._find_messages(channel_id, search_phrase, hours)

            if not messages_to_delete:
                logger.info(f"No messages found containing '{search_phrase}'")
                return 0

            if interactive:
                messages_to_process = self._interactive_selection(
                    messages_to_delete, search_phrase
                )
                if not messages_to_process:
                    logger.info("Deletion cancelled by user")
                    return 0
            else:
                messages_to_process = messages_to_delete

            return self._delete_messages(channel_id, messages_to_process)

        except Exception as e:
            logger.error(f"Error during cleanup: {str(e)}")
            raise

    def _verify_channel(self, channel_id: str) -> None:
        try:
            self.client.conversations_info(channel=channel_id)
        except SlackApiError as e:
            logger.error(f"Could not find channel {channel_id}: {str(e)}")
            raise ChannelNotFoundError(f"Channel {channel_id} not found")

    def _find_messages(
        self, channel_id: str, search_phrase: str, hours: int
    ) -> List[Dict]:
        oldest_timestamp = (datetime.now() - timedelta(hours=hours)).timestamp()
        messages_to_delete = []
        cursor = None

        while True:
            response = self.client.conversations_history(
                channel=channel_id,
                oldest=oldest_timestamp,
                limit=settings.batch_size,
                cursor=cursor,
            )

            for message in response.get("messages", []):
                message_json = json.dumps(message, ensure_ascii=False).lower()
                if search_phrase.lower() in message_json:
                    messages_to_delete.append(message)

            cursor = response.get("response_metadata", {}).get("next_cursor")
            if not cursor:
                break

            time.sleep(settings.delay_between_requests)

        return messages_to_delete

    def _interactive_selection(
        self, messages: List[Dict], search_phrase: str
    ) -> List[Dict]:
        """Interactive message selection for deletion."""
        print(f"\nFound {len(messages)} messages containing '{search_phrase}':")
        for idx, message in enumerate(messages, 1):
            timestamp = datetime.fromtimestamp(float(message["ts"]))
            print(
                f"{idx}. [{timestamp.strftime('%Y-%m-%d %H:%M:%S')}] {message.get('text', '')[:100]}..."
            )

        while True:
            print("\nOptions:")
            print("1. Delete all messages")
            print("2. Delete range of messages")
            print("3. Cancel")

            choice = input("\nEnter your choice (1-3): ")

            if choice == "1":
                return messages
            elif choice == "2":
                try:
                    range_input = input("\nEnter range (e.g., 1-3 or 1,3,5): ")
                    if "-" in range_input:
                        start, end = map(int, range_input.split("-"))
                        indices = range(start - 1, end)
                    else:
                        indices = [int(i) - 1 for i in range_input.split(",")]
                    selected_messages = [
                        messages[i] for i in indices if 0 <= i < len(messages)
                    ]
                    if selected_messages:
                        return selected_messages
                    print("Invalid range. Please try again.")
                except (ValueError, IndexError):
                    print("Invalid range format. Please try again.")
            elif choice == "3":
                return []
            else:
                print("Invalid choice. Please try again.")

    def _delete_messages(self, channel_id: str, messages: List[Dict]) -> int:
        deleted_count = 0
        for message in messages:
            try:
                self.client.chat_delete(channel=channel_id, ts=message["ts"])
                deleted_count += 1
                logger.info(f"Deleted message: {message.get('text', '')[:50]}...")
                time.sleep(settings.delay_between_deletions)
            except SlackApiError as e:
                logger.error(f"Error deleting message: {str(e)}")

        return deleted_count
