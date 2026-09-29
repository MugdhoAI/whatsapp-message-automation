import argparse
import logging
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

    try:
        messages = load_messages(args.file)
    except ValueError as exc:
        parser.error(str(exc))

    _print_preview(messages)

    if args.dry_run or not args.send:
        print("Dry run only. No message was sent.")
        return 0

    if args.delay < 0:
        parser.error("--delay cannot be negative.")

    if args.at is not None:
        print(f"Waiting until {args.at.isoformat()}...")
        wait_until(args.at)

    if not args.yes:
        answer = input("Send these messages through WhatsApp Web? [y/N] ")
        if answer.strip().lower() != "y":
            print("Send cancelled.")
            return 0

    logging.info("Starting send of %d message(s)", len(messages))

    try:
        WhatsAppSender(args.profile).send_batch(messages, delay=args.delay)
    except Exception:
        logging.exception("Message batch failed")
        raise

    logging.info("Message batch completed")
    print("Message batch completed.")
    return 0
