from pathlib import Path

from whatsapp_automation.models import Message
from whatsapp_automation.sender import WhatsAppSender


class FakeLocator:
    def __init__(self):
        self.filled = None
        self.pressed = None

    def wait_for(self, **kwargs):
        return None

    def fill(self, value):
        self.filled = value

    def press(self, value):
        self.pressed = value


class FakePage:
    def __init__(self):
        self.urls = []
        self.composer = FakeLocator()

    def goto(self, url, **kwargs):
        self.urls.append(url)

    def locator(self, selector):
        assert selector == 'div[contenteditable="true"]'
        return FakeLocatorChain(self.composer)

    def wait_for_timeout(self, value):
        return None


class FakeLocatorChain:
    def __init__(self, locator):
        self.locator = locator

    def last(self):
        return self.locator


def test_send_one_opens_contact_and_sends_message():
    page = FakePage()
    message = Message("+8801700000000", "Hello")

    WhatsAppSender(Path("data/profile"))._send_one(page, message)

    assert page.urls[0].endswith("/send?phone=8801700000000")
    assert page.composer.filled == "Hello"
    assert page.composer.pressed == "Enter"
