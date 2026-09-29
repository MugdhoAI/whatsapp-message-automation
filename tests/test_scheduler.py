from datetime import datetime
from unittest.mock import Mock

from whatsapp_automation.scheduler import wait_until


def test_wait_until_returns_when_target_is_now():
    sleep = Mock()

    wait_until(datetime.now(), sleep)

    sleep.assert_not_called()
