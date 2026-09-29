from pathlib import Path
from time import sleep
from typing import Any

from .models import Message


class WhatsAppSender:
    def __init__(self, profile_dir: Path, headless: bool = False) -> None:
        self.profile_dir = profile_dir
        self.headless = headless

    def send_batch(self, messages: list[Message], delay: float = 3.0) -> None:
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
                    self._send_one(page, message)
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

        composer = page.locator('div[contenteditable="true"]').last
        composer.wait_for(state="visible", timeout=60_000)
        composer.fill(message.text)
        composer.press("Enter")
        page.wait_for_timeout(500)
