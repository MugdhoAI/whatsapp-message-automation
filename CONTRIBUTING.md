# Contributing

Contributions should improve correctness, reliability, safety, or usability without expanding the project beyond its intended scope.

## Development setup

Use Python 3.11 or newer:

```bash
python -m venv .venv
```

Activate the environment, then install the development dependencies:

```bash
python -m pip install -e ".[dev]"
playwright install chromium
```

## Checks

Run the test suite and linter before opening a pull request:

```bash
pytest
ruff check .
```

The automated sender tests use a fake browser interface. They do not contact WhatsApp and do not prove live delivery. Do not add tests that send real messages to people or require an authenticated WhatsApp session in CI.

## Pull requests

- Keep each change focused and explain the behavior it changes.
- Add regression tests for bug fixes where practical.
- Update the README when commands, behavior, or limitations change.
- Report the checks you actually ran and identify anything that remains unverified.
- Do not claim delivery verification unless the implementation independently establishes it.

## Privacy and responsible use

Never commit `messages.json`, `data/browser-profile`, logs containing private information, real phone numbers, or personal message content. Use fictional test data. Do not contribute features intended for spam, unsolicited bulk messaging, contact scraping, or bypassing WhatsApp protections.
