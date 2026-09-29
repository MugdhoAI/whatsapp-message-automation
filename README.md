# WhatsApp Message Automation

A small Python command line tool for preparing and sending scheduled WhatsApp messages through WhatsApp Web.

The project is designed for personal automation and controlled testing. It does not use WhatsApp's private APIs or attempt to bypass authentication, rate limits, CAPTCHAs, or other platform protections.

## What it does

- Reads recipients and messages from a JSON file
- Validates phone numbers and message content before sending
- Supports immediate and scheduled messages
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

Use international phone number format without spaces or punctuation.

## Dry run

Before sending anything, inspect the parsed batch:

```bash
python -m whatsapp_automation --file messages.json --dry-run
```

The dry run validates the recipients and messages and prints what would be sent without opening WhatsApp Web.

## Send messages

Start the browser and send the validated batch:

```bash
python -m whatsapp_automation --file messages.json --send
```

The first run opens WhatsApp Web. Scan the QR code normally if WhatsApp asks you to sign in. The browser profile is stored locally in `data/browser-profile` so the session can be reused.

The tool asks for confirmation before a send operation unless `--yes` is supplied.

## Schedule a message batch

Use an ISO 8601 local date and time:

```bash
python -m whatsapp_automation --file messages.json --send --at "2026-10-01T10:30:00"
```

The program waits until the requested time and then starts the send operation.

## Delay between messages

A delay helps keep the tool predictable and reduces accidental rapid sending:

```bash
python -m whatsapp_automation --file messages.json --send --delay 5
```

The default delay is 3 seconds.

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

`scheduler.py` handles immediate execution and waiting for a requested send time.

`sender.py` owns Playwright and WhatsApp Web interaction. It is intentionally isolated so the rest of the application can be tested without opening a browser.

`cli.py` connects the pieces and controls the command line interface.

This separation keeps browser automation out of the validation and scheduling logic and makes those parts straightforward to test.

## Testing

Run the test suite with:

```bash
pytest
```

Run Ruff:

```bash
ruff check .
```

The browser sender is tested with a fake browser interface. The tests do not contact WhatsApp.

## Safety and scope

This project is intended for messages to people who expect to receive them. It should not be used for spam, bulk unsolicited messaging, scraping contact information, or bypassing WhatsApp security controls.

The automation uses the normal WhatsApp Web interface. WhatsApp can change its web interface at any time, so browser selectors may need maintenance when the site changes.

## License

MIT
