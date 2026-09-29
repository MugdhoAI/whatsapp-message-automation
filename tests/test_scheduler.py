from datetime import datetime, timedelta
from unittest.mock import Mock

from whatsapp_automation.scheduler import wait_until


def test_wait_until_returns_when_target_is_now():
    sleep = Mock()

    wait_until(datetime.now(), sleep)

    sleep.assert_not_called()


def test_wait_until_sleeps_until_target():
    now = datetime(2026, 10, 1, 10, 0, 0)
    target = now + timedelta(seconds=2)
    sleep = Mock()
    clock = Mock(side_effect=[now, now + timedelta(seconds=1), target])

    wait_until(target, sleep, clock)

    assert sleep.call_args_list[0].args == (1.0,)
    assert sleep.call_args_list[1].args == (1.0,)
