from datetime import datetime
from time import sleep
from typing import Callable


def wait_until(target: datetime, sleep_fn: Callable[[float], None] = sleep) -> None:
    while True:
        remaining = (target - datetime.now()).total_seconds()
        if remaining <= 0:
            return
        sleep_fn(min(remaining, 1.0))
