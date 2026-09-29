import json

import pytest

from whatsapp_automation.validation import load_messages


def test_load_messages(tmp_path):
    path = tmp_path / "messages.json"
    path.write_text(
        json.dumps(
            [
                {
                    "phone": "+8801700000000",
                    "message": "Hello",
                }
            ]
        ),
        encoding="utf-8",
    )

    messages = load_messages(path)

    assert len(messages) == 1
    assert messages[0].phone == "+8801700000000"
    assert messages[0].text == "Hello"


@pytest.mark.parametrize(
    "payload",
    [
        [{"phone": "01700000000", "message": "Hello"}],
        [{"phone": "+8801700000000", "message": ""}],
        {"phone": "+8801700000000", "message": "Hello"},
    ],
)
def test_invalid_messages(tmp_path, payload):
    path = tmp_path / "messages.json"
    path.write_text(json.dumps(payload), encoding="utf-8")

    with pytest.raises(ValueError):
        load_messages(path)
