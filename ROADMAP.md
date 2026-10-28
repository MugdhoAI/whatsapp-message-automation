# Roadmap

This is a small command line utility for controlled, opt-in WhatsApp reminders and notifications. The list below describes possible improvements, not committed release dates.

## Current scope

- Validate a JSON batch before opening WhatsApp Web.
- Preview messages without sending.
- Send immediately or schedule one batch for a specific date and time.
- Require confirmation by default.
- Keep the authenticated browser profile local.
- Avoid automatic retries when a send result is uncertain.

## Possible future work

- Improve per-message status reporting without implying delivery when it cannot be verified.
- Document a manual smoke-test procedure for checking compatibility with current WhatsApp Web behavior.
- Evaluate recurring schedules only after cancellation, duplicate-send behavior, and consent safeguards can be specified and tested.

## Out of scope

- Unsolicited bulk messaging or spam.
- Contact scraping.
- Bypassing authentication or WhatsApp platform protections.
- Claiming delivery or read receipts without independent verification.
