from datetime import datetime
from time import sleep
from typing import Callable

Clock = Callable[[], datetime]
Sleeper = Callable[[float], None]


def wait_until(
    target: datetime,
    sleep_fn: Sleeper = sleep,
    now_fn: Clock | None = None,
) -> None:
    while True:
        now = now_fn() if now_fn is not None else datetime.now(target.tzinfo)
        if (target.tzinfo is None) != (now.tzinfo is None):
            raise ValueError(
                "Scheduled time and current time must both be timezone-aware or both be local."
            )
        remaining = (target - now).total_seconds()
        if remaining <= 0:
            return
        sleep_fn(min(remaining, 1.0))
