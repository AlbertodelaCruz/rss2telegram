from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class Publication:
    date: datetime
    title: str
    content: str
