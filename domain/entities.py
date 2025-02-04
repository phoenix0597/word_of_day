from dataclasses import dataclass
from datetime import datetime


@dataclass
class Article:
    header: str
    body: str
    word: str
    created_at: datetime


@dataclass
class WordOfDay:
    word: str
    description: str
