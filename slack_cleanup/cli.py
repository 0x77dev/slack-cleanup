import logging
from typing import Optional

import typer

from .cleaner import SlackCleaner

app = typer.Typer()

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

@app.command()
def cleanup(
    channel: Optional[str] = typer.Option(None, "--channel", "-c", help="Channel ID or name"),
    phrase: Optional[str] = typer.Option(None, "--phrase", "-p", help="Search phrase"),
    hours: Optional[int] = typer.Option(None, "--hours", "-h", help="Hours to look back"),
    non_interactive: bool = typer.Option(False, "--non-interactive", "-n", help="Run in non-interactive mode"),
    token: Optional[str] = typer.Option(None, "--token", "-t", help="Slack Bot User OAuth Token")
):
    """Clean up Slack messages containing specific phrases."""
    try:
        cleaner = SlackCleaner(token)

        if not channel or not phrase:
            if non_interactive:
                typer.echo("Error: channel and phrase are required in non-interactive mode")
                raise typer.Exit(1)
            return interactive_cleanup(cleaner)

        deleted_count = cleaner.delete_messages(
            channel_id=channel,
            search_phrase=phrase,
            hours_to_look_back=hours,
            interactive=not non_interactive
        )
        
        typer.echo(f"\nSuccessfully deleted {deleted_count} messages containing '{phrase}'")

    except Exception as e:
        typer.echo(f"Error: {str(e)}", err=True)
        raise typer.Exit(1)

def interactive_cleanup(cleaner: SlackCleaner):
    """Interactive mode for cleaning up messages."""
    channels = cleaner.list_channels()
    
    typer.echo("\nAvailable channels:")
    for idx, channel in enumerate(channels, 1):
        typer.echo(f"{idx}. #{channel['name']}")

    while True:
        try:
            selection = int(typer.prompt("\nSelect channel number")) - 1
            if 0 <= selection < len(channels):
                selected_channel = channels[selection]
                break
            typer.echo("Invalid selection. Please try again.")
        except ValueError:
            typer.echo("Please enter a valid number.")

    phrase = typer.prompt("\nEnter phrase to search for deletion")
    
    deleted_count = cleaner.delete_messages(
        channel_id=selected_channel["id"],
        search_phrase=phrase,
        interactive=True
    )
    
    typer.echo(f"\nSuccessfully deleted {deleted_count} messages containing '{phrase}'")

if __name__ == "__main__":
    app() 