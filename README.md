# Slack Cleanup

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![FOSSA Status](https://app.fossa.com/api/projects/git%2Bgithub.com%2F0x77dev%2Fslack-cleanup.svg?type=shield)](https://app.fossa.com/projects/git%2Bgithub.com%2F0x77dev%2Fslack-cleanup?ref=badge_shield)

A powerful CLI tool for bulk deletion of Slack messages containing specific phrases. Features interactive and non-interactive modes, with built-in rate limiting and pagination to handle large message volumes efficiently.

## Motivation

Managing Slack integrations can sometimes lead to unexpected message bloat in your channels. When an integration isn't working as intended, it may flood your channels with unwanted messages. While Slack's native interface doesn't provide bulk message deletion capabilities, this tool fills that gap by offering an efficient way to clean up unwanted messages.

## Prerequisites

- Docker installed on your system
- Slack Bot Token with appropriate permissions (Generate using the provided [App Manifest](./app_manifest.json))

## Quick Start

### Setting Up Your Slack Token

1. Visit the [Slack API Dashboard](https://api.slack.com/apps) and create a new app
2. Import the [App Manifest](./app_manifest.json) to configure necessary permissions
3. Install the app to your workspace and copy the User OAuth Token

### Running the Cleanup Tool

```bash
docker run -it --rm -e SLACK_CLEANUP_SLACK_TOKEN=<your-slack-bot-token> ghcr.io/0x77dev/
slack-cleanup:latest
```


## License
[![FOSSA Status](https://app.fossa.com/api/projects/git%2Bgithub.com%2F0x77dev%2Fslack-cleanup.svg?type=large)](https://app.fossa.com/projects/git%2Bgithub.com%2F0x77dev%2Fslack-cleanup?ref=badge_large)