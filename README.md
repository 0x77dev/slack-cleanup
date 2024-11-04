# Slack Cleanup

![License](https://img.shields.io/github/license/0x77dev/slack-cleanup) [![FOSSA License Status](https://app.fossa.com/api/projects/git%2Bgithub.com%2F0x77dev%2Fslack-cleanup.svg?type=shield&issueType=license)](https://app.fossa.com/projects/git%2Bgithub.com%2F0x77dev%2Fslack-cleanup?ref=badge_shield&issueType=license) [![FOSSA Security Status](https://app.fossa.com/api/projects/git%2Bgithub.com%2F0x77dev%2Fslack-cleanup.svg?type=shield&issueType=security)](https://app.fossa.com/projects/git%2Bgithub.com%2F0x77dev%2Fslack-cleanup?ref=badge_shield&issueType=security) ![GitHub Release](https://img.shields.io/github/v/release/0x77dev/slack-cleanup)

A powerful CLI tool for bulk deletion of Slack messages containing specific phrases. Features interactive and non-interactive modes, with built-in rate limiting and pagination to handle large message volumes efficiently.

[![asciicast](https://asciinema.org/a/5zAZcsXYMBZihiF406T7WvC3R.svg)](https://asciinema.org/a/5zAZcsXYMBZihiF406T7WvC3R)

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
docker run -it --rm -e SLACK_CLEANUP_SLACK_TOKEN=<your-slack-bot-token> ghcr.io/0x77dev/slack-cleanup:latest --help

Usage: slack-cleanup [OPTIONS]

  Clean up Slack messages containing specific phrases.

Options:
  -c, --channel TEXT              Channel ID or name
  -p, --phrase TEXT               Search phrase
  -h, --hours INTEGER             Hours to look back
  -n, --non-interactive           Run in non-interactive mode
  -t, --token TEXT                Slack Bot User OAuth Token
  --install-completion [bash|zsh|fish|powershell|pwsh]
                                  Install completion for the specified shell.
  --show-completion [bash|zsh|fish|powershell|pwsh]
                                  Show completion for the specified shell, to
                                  copy it or customize the installation.
  --help                          Show this message and exit.
```

Use interactive mode to select channels and phrases for deletion.

## Options

- `--channel, -c`: Channel ID or name
- `--phrase, -p`: Search phrase
- `--hours, -h`: Hours to look back
- `--non-interactive, -n`: Run in non-interactive mode
- `--token, -t` or `SLACK_CLEANUP_SLACK_TOKEN`: Slack Bot User OAuth Token
- `--install-completion`: Install completion for the current shell
- `--show-completion`: Show completion for the current shell
- `--help`: Show help message and exit
