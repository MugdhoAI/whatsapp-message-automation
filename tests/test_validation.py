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
        [{"phone": "+8801700000000", "message": "   "}],
        [{"phone": "+8801700000000", "message": 42}],
        [{"phone": "+8801700000000", "message": "Hello", "extra": True}],
    ],
)
def test_invalid_messages(tmp_path, payload):
    path = tmp_path / "messages.json"
    path.write_text(json.dumps(payload), encoding="utf-8")

    with pytest.raises(ValueError):
        load_messages(path)


def test_missing_file_has_actionable_error(tmp_path):
    with pytest.raises(ValueError, match="Message file not found"):
        load_messages(tmp_path / "missing.json")


def test_invalid_utf8_has_actionable_error(tmp_path):
    path = tmp_path / "messages.json"
    path.write_bytes(bytes([0xFF]))

    with pytest.raises(ValueError, match="valid UTF-8"):
        load_messages(path)
