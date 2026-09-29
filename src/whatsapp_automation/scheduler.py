from datetime import datetime
from time import sleep
from typing import Callable

Clock = Callable[[], datetime]
Sleeper = Callable[[float], None]


def wait_until(
    target: datetime,
    sleep_fn: Sleeper = sleep,
    now_fn: Clock = datetime.now,
) -> None:
    while True:
        remaining = (target - now_fn()).total_seconds()
        if remaining <= 0:
            return
        sleep_fn(min(remaining, 1.0))
