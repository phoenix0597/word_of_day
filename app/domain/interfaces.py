from abc import ABC, abstractmethod
from app.domain.entities import Article, WordOfDay


class RSSReader(ABC):
    @abstractmethod
    async def get_word_of_day(self) -> WordOfDay:
        pass


class AIGenerator(ABC):
    @abstractmethod
    async def generate_article(self, word: WordOfDay) -> Article:
        pass


class CacheService(ABC):
    @abstractmethod
    async def get_article(self) -> Article | None:
        pass

    @abstractmethod
    async def save_article(self, article: Article) -> None:
        pass
