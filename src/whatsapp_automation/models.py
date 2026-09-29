from dataclasses import dataclass


@dataclass(frozen=True)
class Message:
    phone: str
    text: str
