import argparse
import logging
import math
import sys
from datetime import datetime
from pathlib import Path

from .models import Message
from .scheduler import wait_until
from .sender import WhatsAppSender
from .validation import load_messages


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Prepare and send WhatsApp messages through WhatsApp Web."
    )
    parser.add_argument("--file", type=Path, default=Path("messages.json"))
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--send", action="store_true")
    parser.add_argument("--yes", action="store_true")
    parser.add_argument("--at", type=_parse_datetime)
    parser.add_argument("--delay", type=float, default=3.0)
    parser.add_argument(
        "--profile",
        type=Path,
        default=Path("data/browser-profile"),
    )
    return parser


def _parse_datetime(value: str) -> datetime:
    try:
        return datetime.fromisoformat(value)
    except ValueError as exc:
        raise argparse.ArgumentTypeError(
            "Use ISO 8601 format such as 2026-10-01T10:30:00."
        ) from exc


def _print_preview(messages: list[Message]) -> None:
    print(f"Validated {len(messages)} message(s).")
    for index, message in enumerate(messages, start=1):
        print(f"{index}. {message.phone}: {message.text}")


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    logging.basicConfig(
        filename="whatsapp-automation.log",
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(message)s",
    )

    if not math.isfinite(args.delay) or args.delay < 0:
        parser.error("--delay must be a finite, non negative number.")

    try:
        messages = load_messages(args.file)
    except ValueError as exc:
        parser.error(str(exc))

    _print_preview(messages)

    if args.dry_run or not args.send:
        print("Dry run only. No message was sent.")
        return 0

    # Confirm before waiting so a scheduled invocation does not block for input
    # at the target time, when the user may no longer be present.
    if not args.yes:
        try:
            answer = input("Send these messages through WhatsApp Web? [y/N] ")
        except (EOFError, KeyboardInterrupt):
            print("\\nSend cancelled.", file=sys.stderr)
            return 130
        if answer.strip().lower() != "y":
            print("\\nSend cancelled.", file=sys.stderr)
            return 0

    if args.at is not None:
        print(f"Waiting until {args.at.isoformat()}...")
        try:
            wait_until(args.at)
        except KeyboardInterrupt:
            print("\\nScheduled send cancelled before sending.", file=sys.stderr)
            return 130
        except ValueError as exc:
            parser.error(str(exc))

    logging.info("Starting send of %d message(s)", len(messages))

    try:
        WhatsAppSender(args.profile).send_batch(messages, delay=args.delay)
    except KeyboardInterrupt:
        logging.warning("Message batch interrupted by user")
        print(
            "Message batch interrupted. Check WhatsApp before retrying; "
            "a send may have completed.",
            file=sys.stderr,
        )
        return 130
    except Exception as exc:
        # Avoid logging a traceback: chained Playwright exceptions can contain
        # recipient-specific WhatsApp URLs and expose phone numbers in local logs.
        logging.error(
            "Message batch failed (%s); send status may be uncertain",
            type(exc).__name__,
        )
        print(
            f"Message batch failed: {exc}. Check WhatsApp before retrying because "
            "send status may be uncertain.",
            file=sys.stderr,
        )
        return 1

    logging.info("Message batch automation completed; delivery was not independently verified")
    print(
        "Message batch automation completed. This confirms the browser steps finished, "
        "not that recipients received or read every message."
    )
    return 0
