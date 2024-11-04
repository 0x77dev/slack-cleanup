class SlackCleanerError(Exception):
    """Base exception for slack-cleanup errors."""
    pass

class ChannelNotFoundError(SlackCleanerError):
    """Raised when a specified channel cannot be found."""
    pass

class TokenError(SlackCleanerError):
    """Raised when there are issues with the Slack token."""
    pass

class RateLimitError(SlackCleanerError):
    """Raised when Slack API rate limits are hit."""
    pass 