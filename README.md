# WhatsApp Message Automation

A Python command line tool for preparing and sending scheduled WhatsApp messages through WhatsApp Web.

The project is designed for personal automation and controlled testing. It does not use WhatsApp's private APIs or attempt to bypass authentication, rate limits, CAPTCHAs, or other platform protections.

## What it does

- Reads recipients and messages from a JSON file
- Validates international phone numbers and message content before sending
- Rejects unsupported fields in message entries
- Supports immediate and scheduled message batches
- Opens WhatsApp Web through Playwright
- Uses a persistent browser profile so the normal WhatsApp Web login can be reused
- Provides a dry run mode for checking a batch without sending anything
- Adds a configurable delay between messages
- Writes a local activity log
- Keeps browser automation separate from scheduling and input validation

## Requirements

- Python 3.11 or newer
- A WhatsApp account
- A desktop browser environment
- Playwright

## Setup

Create a virtual environment:

```bash
python -m venv .venv
```

Activate it on Windows:

```powershell
.\.venv\Scripts\Activate.ps1
```

Activate it on macOS or Linux:

```bash
source .venv/bin/activate
```

Install the project:

```bash
pip install -e ".[dev]"
playwright install chromium
```

## Message file

Copy the example file:

```bash
cp messages.example.json messages.json
```

On Windows PowerShell:

```powershell
Copy-Item messages.example.json messages.json
```

A message entry looks like this:

```json
[
  {
    "phone": "+8801700000000",
    "message": "Hello from my automation project."
  }
]
```

Use international phone number format without spaces or punctuation. Each entry must contain only the `phone` and `message` fields. The tool rejects missing files, invalid UTF-8, malformed JSON, unsupported fields, invalid phone numbers, and empty messages before opening the browser.

## Dry run

Before sending anything, inspect the parsed batch:

```bash
python -m whatsapp_automation --file messages.json --dry-run
```

The dry run validates the recipients and messages and prints what would be sent without opening WhatsApp Web. Message text is included in the terminal preview, so avoid running it where that content can be seen by others.

## Send messages

Start the browser and send the validated batch:

```bash
python -m whatsapp_automation --file messages.json --send
```

The first run opens WhatsApp Web. Scan the QR code normally if WhatsApp asks you to sign in. The browser profile is stored locally in `data/browser-profile` so the session can be reused.

The tool asks for confirmation before a send operation unless `--yes` is supplied. Use `--yes` only when you have reviewed the exact batch and intend to send it without an interactive confirmation.

If a browser or network error occurs during a batch, the status of the current message may be uncertain. Check the WhatsApp chat before retrying because the message may already have been submitted. The tool does not automatically retry uncertain sends.

A completed browser operation is not proof that every message was delivered or read. WhatsApp Web can change, and the sender currently does not independently verify delivery receipts.

## Schedule a message batch

Use an ISO 8601 local date and time:

```bash
python -m whatsapp_automation --file messages.json --send --at "2026-10-16T10:30:00"
```

The program asks for confirmation before waiting, unless `--yes` is supplied. It then waits until the requested time and starts the send operation. A date and time without a timezone is interpreted as local time. If you include a timezone offset, the scheduler compares it as an aware datetime. Keep the terminal session and computer running while waiting.

## Delay between messages

Set a non negative, finite delay between messages:

```bash
python -m whatsapp_automation --file messages.json --send --delay 5
```

The default delay is 3 seconds. The delay is not a guarantee of delivery or protection against platform limits.

## Project structure

```text
whatsapp-message-automation/
├── src/
│   └── whatsapp_automation/
│       ├── __main__.py
│       ├── cli.py
│       ├── models.py
│       ├── scheduler.py
│       ├── sender.py
│       └── validation.py
├── tests/
│   ├── test_cli.py
│   ├── test_scheduler.py
│   ├── test_validation.py
│   └── test_sender.py
├── .github/
│   └── workflows/
│       └── ci.yml
├── messages.example.json
├── pyproject.toml
└── README.md
```

## Design

The application has four small responsibilities.

`validation.py` turns untrusted JSON input into validated message objects.

`scheduler.py` handles waiting for a requested send time.

`sender.py` owns Playwright and WhatsApp Web interaction. It is isolated so the rest of the application can be tested without opening a browser.

`cli.py` connects the pieces and controls the command line interface.

## Testing

Run the test suite with:

```bash
pytest
```

Run Ruff:

```bash
ruff check .
```

The sender tests use a fake browser interface and do not contact WhatsApp. They verify the automation calls, not the live website, message delivery, or account state.

## Session and message privacy

The persistent browser profile contains authenticated session data and must be treated as sensitive. Do not share it or commit it to version control. The `data/` directory and local message file are ignored by Git. Keep access to the profile limited to your own account and device.

The activity log records operational events and errors. Review local logs before sharing them publicly.

## Safety and scope

This project is intended for messages to people who expect to receive them. It should not be used for spam, bulk unsolicited messaging, scraping contact information, or bypassing WhatsApp security controls.

The automation uses the normal WhatsApp Web interface. WhatsApp can change its web interface at any time, so browser selectors may need maintenance when the site changes.

## License

MIT
