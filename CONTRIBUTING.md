# Contributing

Thanks for considering a contribution. Please keep changes focused on making the tool easier to use, safer, or more reliable.

## Set up the project

Use Python 3.11 or newer:

```bash
python -m venv .venv
python -m pip install -e ".[dev]"
playwright install chromium
```

Activate the virtual environment before installing or running the project.

## Run the checks

Before opening a pull request, run:

```bash
pytest
ruff check .
```

The sender tests use a fake browser. They do not contact WhatsApp. Do not add tests that send real messages or require a signed in WhatsApp session in CI.

## Open a pull request

- Keep each change focused and explain what it fixes or adds.
- Add a regression test for a bug fix when practical.
- Update the README if commands, behavior, or limitations change.
- Say which checks you ran and what remains untested.
- Do not claim that a message was delivered unless the code can verify it.

## Protect private information

Do not commit `messages.json`, browser profile data, logs containing private details, real phone numbers, or personal message content. Use fictional data in tests.

Do not add features for spam, unsolicited bulk messages, contact scraping, or bypassing WhatsApp protections.
