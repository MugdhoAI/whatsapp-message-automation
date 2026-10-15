import math
import re
from pathlib import Path
from time import sleep
from typing import Any

from .models import Message

_PHONE_PATTERN = re.compile(r"^\\+[1-9]\\d{7,14}$")


class WhatsAppSender:
    def __init__(self, profile_dir: Path, headless: bool = False) -> None:
        self.profile_dir = profile_dir
        self.headless = headless

    def send_batch(self, messages: list[Message], delay: float = 3.0) -> None:
        if not messages:
            raise ValueError("Message batch must not be empty.")
        if not math.isfinite(delay) or delay < 0:
            raise ValueError("Delay must be a finite, non-negative number.")
        for index, message in enumerate(messages, start=1):
            if not _PHONE_PATTERN.fullmatch(message.phone):
                raise ValueError(f"Message {index} has an invalid international phone number.")
            if not message.text.strip():
                raise ValueError(f"Message {index} must not be empty.")

        from playwright.sync_api import sync_playwright

        self.profile_dir.mkdir(parents=True, exist_ok=True)

        with sync_playwright() as playwright:
            context = playwright.chromium.launch_persistent_context(
                str(self.profile_dir),
                headless=self.headless,
            )
            try:
                page = context.pages[0] if context.pages else context.new_page()
                page.goto("https://web.whatsapp.com/", wait_until="domcontentloaded")
                page.wait_for_selector('div[contenteditable="true"]', timeout=120_000)

                for index, message in enumerate(messages):
                    try:
                        self._send_one(page, message)
                    except Exception as exc:
                        raise RuntimeError(
                            f"Failed while processing message {index + 1} of {len(messages)}. "
                            "The current message may already have been submitted; check WhatsApp "
                            "before retrying."
                        ) from exc
                    if index < len(messages) - 1:
                        sleep(delay)
            finally:
                context.close()

    @staticmethod
    def _send_one(page: Any, message: Message) -> None:
        page.goto(
            f"https://web.whatsapp.com/send?phone={message.phone.lstrip('+')}",
            wait_until="domcontentloaded",
        )

        # Restrict the composer to the active chat footer, not the chat search field.
        composer = page.locator('footer div[contenteditable="true"]').last
        composer.wait_for(state="visible", timeout=60_000)
        composer.fill(message.text)
        composer.press("Enter")
