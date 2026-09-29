import json
import re
from pathlib import Path

from .models import Message

PHONE_PATTERN = re.compile(r"^\+[1-9]\d{7,14}$")


def load_messages(path: Path) -> list[Message]:
    try:
        raw = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise ValueError(f"Message file not found: {path}") from exc
    except json.JSONDecodeError as exc:
        raise ValueError(f"Invalid JSON in {path}: {exc.msg}") from exc

    if not isinstance(raw, list):
        raise ValueError("Message file must contain a JSON array.")

    messages: list[Message] = []

    for index, item in enumerate(raw, start=1):
        if not isinstance(item, dict):
            raise ValueError(f"Entry {index} must be a JSON object.")

        phone = item.get("phone")
        text = item.get("message")

        if not isinstance(phone, str) or not PHONE_PATTERN.fullmatch(phone):
            raise ValueError(
                f"Entry {index} has an invalid phone number. "
                "Use international format such as +8801700000000."
            )

        if not isinstance(text, str) or not text.strip():
            raise ValueError(f"Entry {index} must contain a non empty message.")

        messages.append(Message(phone=phone, text=text))

    if not messages:
        raise ValueError("Message file does not contain any messages.")

    return messages
