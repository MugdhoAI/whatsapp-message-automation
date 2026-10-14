from pathlib import Path

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
        self.composer = FakeLocator()

    def goto(self, url, **kwargs):
        self.urls.append((url, kwargs))

    def locator(self, selector):
        assert selector == 'div[contenteditable="true"]'
        return FakeLocatorChain(self.composer)

    def wait_for_timeout(self, value):
        return None


class FakeLocatorChain:
    def __init__(self, locator):
        self.last = locator


def test_send_one_opens_contact_and_sends_message():
    page = FakePage()
    message = Message("+8801700000000", "Hello")

    WhatsAppSender(Path("data/profile"))._send_one(page, message)

    assert page.urls == [
        (
            "https://web.whatsapp.com/send?phone=8801700000000",
            {"wait_until": "domcontentloaded"},
        )
    ]
    assert page.composer.wait_calls == [{"state": "visible", "timeout": 60_000}]
    assert page.composer.filled == "Hello"
    assert page.composer.pressed == "Enter"
