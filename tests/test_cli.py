from datetime import datetime
from pathlib import Path
from unittest.mock import Mock

import pytest

from whatsapp_automation import cli
from whatsapp_automation.models import Message


@pytest.fixture
def valid_messages():
    return [Message("+8801700000000", "Hello")]


def test_dry_run_never_starts_sender(monkeypatch, capsys, valid_messages, tmp_path):
    monkeypatch.setattr(
        "sys.argv", ["whatsapp-automation", "--file", str(tmp_path / "messages.json"), "--dry-run"]
    )
    monkeypatch.setattr(cli, "load_messages", lambda _path: valid_messages)
    sender = Mock()
    monkeypatch.setattr(cli, "WhatsAppSender", lambda _profile: sender)

    assert cli.main() == 0
    sender.send_batch.assert_not_called()
    assert "Dry run only" in capsys.readouterr().out


@pytest.mark.parametrize("delay", ["nan", "inf", "-inf", "-1"])
def test_invalid_delay_fails_before_loading_messages(monkeypatch, delay):
    monkeypatch.setattr("sys.argv", ["whatsapp-automation", "--delay", delay])
    loader = Mock()
    monkeypatch.setattr(cli, "load_messages", loader)

    with pytest.raises(SystemExit) as error:
        cli.main()

    assert error.value.code == 2
    loader.assert_not_called()


def test_scheduled_send_confirms_before_waiting(monkeypatch, tmp_path, valid_messages):
    events = []
    monkeypatch.setattr(
        "sys.argv",
        [
            "whatsapp-automation",
            "--file",
            str(tmp_path / "messages.json"),
            "--send",
            "--at",
            "2026-10-16T10:00:00",
        ],
    )
    monkeypatch.setattr(cli, "load_messages", lambda _path: valid_messages)
    monkeypatch.setattr("builtins.input", lambda _prompt: events.append("confirm") or "y")
    monkeypatch.setattr(
        cli, "wait_until", lambda target: events.append(("wait", isinstance(target, datetime)))
    )
    sender = Mock()
    monkeypatch.setattr(cli, "WhatsAppSender", lambda _profile: sender)

    assert cli.main() == 0

    assert events == ["confirm", ("wait", True)]
    sender.send_batch.assert_called_once_with(valid_messages, delay=3.0)


def test_declined_scheduled_send_does_not_wait_or_send(
    monkeypatch, tmp_path, valid_messages
):
    monkeypatch.setattr(
        "sys.argv",
        [
            "whatsapp-automation",
            "--file",
            str(tmp_path / "messages.json"),
            "--send",
            "--at",
            "2026-10-16T10:00:00",
        ],
    )
    monkeypatch.setattr(cli, "load_messages", lambda _path: valid_messages)
    monkeypatch.setattr("builtins.input", lambda _prompt: "n")
    wait = Mock()
    sender = Mock()
    monkeypatch.setattr(cli, "wait_until", wait)
    monkeypatch.setattr(cli, "WhatsAppSender", lambda _profile: sender)

    assert cli.main() == 0

    wait.assert_not_called()
    sender.send_batch.assert_not_called()
