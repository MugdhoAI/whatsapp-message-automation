from pathlib import Path

import pytest

from whatsapp_automation.models import Message
from whatsapp_automation.sender import WhatsAppSender


class FakeLocator:
    def __init__(self):
        self.filled = None
        self.pressed = None
        self.wait_calls = []

    def wait_for(self, **kwargs):
        self.wait_calls.append(kwargs)

    def fill(self, value):
        self.filled = value

    def press(self, value):
        self.pressed = value


class FakePage:
    def __init__(self):
        self.urls = []
        self.selectors = []
        self.composer = FakeLocator()

    def goto(self, url, **kwargs):
        self.urls.append((url, kwargs))

    def locator(self, selector):
        self.selectors.append(selector)
        return FakeLocatorChain(self.composer)


class FakeLocatorChain:
    def __init__(self, locator):
        self.last = locator


def test_send_one_opens_contact_and_uses_chat_composer():
    page = FakePage()
    message = Message("+8801700000000", "Hello")

    WhatsAppSender(Path("data/profile"))._send_one(page, message)

    assert page.urls == [
        (
            "https://web.whatsapp.com/send?phone=8801700000000",
            {"wait_until": "domcontentloaded"},
        )
    ]
    assert page.selectors == ['footer div[contenteditable="true"]']
    assert page.composer.wait_calls == [{"state": "visible", "timeout": 60_000}]
    assert page.composer.filled == "Hello"
    assert page.composer.pressed == "Enter"


@pytest.mark.parametrize("delay", [-1, float("nan"), float("inf")])
def test_send_batch_rejects_invalid_delay_before_browser_launch(monkeypatch, tmp_path, delay):
    sender = WhatsAppSender(tmp_path / "profile")
    monkeypatch.setitem(__import__("sys").modules, "playwright", None)

    with pytest.raises(ValueError, match="Delay"):
        sender.send_batch([Message("+8801700000000", "Hello")], delay=delay)


def test_send_batch_rejects_empty_batch_before_browser_launch(tmp_path):
    with pytest.raises(ValueError, match="must not be empty"):
        WhatsAppSender(tmp_path / "profile").send_batch([])


@pytest.mark.parametrize(
    "message",
    [
        Message("01700000000", "Hello"),
        Message("+8801700000000", "  "),
    ],
)
def test_send_batch_rejects_invalid_message_before_browser_launch(tmp_path, message):
    with pytest.raises(ValueError):
        WhatsAppSender(tmp_path / "profile").send_batch([message])
