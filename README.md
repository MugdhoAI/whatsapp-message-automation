# WhatsApp Message Automation

[![CI](https://github.com/MugdhoAI/whatsapp-message-automation/actions/workflows/ci.yml/badge.svg)](https://github.com/MugdhoAI/whatsapp-message-automation/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

![Illustration of a scheduled WhatsApp reminder workflow](assets/whatsapp-automation-hero.svg)

A Python command line tool for sending WhatsApp reminders and notifications through WhatsApp Web.

It reads a list of recipients and messages from a JSON file, lets you review the batch, and can send it now or wait until a chosen time. It uses Playwright to control the regular WhatsApp Web interface.

Use it for messages people expect to receive, such as personal reminders or small internal notifications. It does not use a private WhatsApp API or try to bypass login, CAPTCHAs, rate limits, or other platform protections.

## Features

- Check phone numbers and message text before opening the browser.
- Preview a batch without sending anything.
- Send a batch now or schedule it for one date and time.
- Ask for confirmation before sending, unless you pass `--yes`.
- Keep the WhatsApp Web login in a local browser profile.
- Set a delay between messages.
- Write basic activity details to a local log.

It supports one scheduled batch at a time. It does not support recurring reminders, contact name lookup, message templates, or delivery receipt checks.

## Requirements

- Python 3.11 or newer
- A WhatsApp account
- A desktop environment that can run Chromium
- Playwright

## Install

Create a virtual environment:

```bash
python -m venv .venv
```

Activate it in Windows PowerShell:

```powershell
.\\.venv\\Scripts\\Activate.ps1
```

Or on macOS or Linux:

```bash
source .venv/bin/activate
```

Install the project and browser:

```bash
python -m pip install -e ".[dev]"
playwright install chromium
```

## Prepare your messages

Copy the example file.

Windows PowerShell:

```powershell
Copy-Item messages.example.json messages.json
```

macOS or Linux:

```bash
cp messages.example.json messages.json
```

Edit `messages.json` and add the intended recipients and message text. Each entry must contain only `phone` and `message`. Use international phone number format, for example `+8801700000000`.

## Preview and send

First, check the batch without sending:

```bash
python -m whatsapp_automation --file messages.json --dry-run
```

Read the preview carefully. It displays the phone numbers and message text.

When the preview is correct, run:

```bash
python -m whatsapp_automation --file messages.json --send
```

On the first run, WhatsApp Web opens in Chromium. Scan the QR code if you need to sign in. The tool asks you to confirm before it starts sending.

## Schedule a batch

Pass a date and time in ISO 8601 format. Replace this example with a future time in your local timezone:

```bash
python -m whatsapp_automation --file messages.json --send --at "2030-01-01T10:30:00"
```

The tool asks for confirmation before waiting, unless you pass `--yes`. Press Ctrl+C to cancel while it is waiting. Keep the terminal and computer running until the scheduled time. If you do not include a timezone offset, the time is treated as local time.

## Set the delay

The default delay between messages is three seconds. To use a different delay, pass `--delay`:

```bash
python -m whatsapp_automation --file messages.json --send --delay 5
```

The delay does not guarantee delivery or bypass WhatsApp limits.

## Use it responsibly

- Send messages only to people who expect them and have agreed to receive them.
- Do not use the tool for spam, unsolicited bulk messages, contact scraping, or attempts to evade WhatsApp protections.
- Use the preview before sending and check the recipient list.
- Pass `--yes` only when you have already reviewed the batch and want to skip confirmation.
- The browser profile in `data/browser-profile` stores login session data. Keep it private and never commit or share it.
- The preview shows message text in the terminal. Review the local log before sharing it, as it may contain operational details.

## Limitations

This tool controls WhatsApp Web. It is not an official WhatsApp API client, and changes to the website may break the automation.

A completed browser operation does not prove that a message was delivered or read. If an error occurs while sending, the status of that message may be unclear. Check WhatsApp before trying again. The tool does not retry automatically.

This project is intended for small, personal or internal workflows. It is not a bulk messaging service or a replacement for production messaging infrastructure.

## Development

Run the tests and linter:

```bash
pytest
ruff check .
```

The sender tests use a fake browser, so they do not contact WhatsApp. Passing the tests does not confirm that the current WhatsApp Web interface works or that messages will be delivered.

## Project structure

```text
src/whatsapp_automation/
├── __main__.py
├── cli.py
├── models.py
├── scheduler.py
├── sender.py
└── validation.py

tests/
├── test_cli.py
├── test_scheduler.py
├── test_sender.py
└── test_validation.py
```

The code separates input checks, scheduling, command line behavior, and browser actions. Most of it can be tested without opening a browser.

## Contributing and security

If you want to contribute, read [CONTRIBUTING.md](CONTRIBUTING.md). For security concerns, see [SECURITY.md](SECURITY.md).

## License

MIT. See [LICENSE](LICENSE).
