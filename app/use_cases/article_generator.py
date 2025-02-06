from datetime import datetime, timezone

from app.domain.interfaces import RSSReader, AIGenerator, CacheService
from app.core.logger import logger


class ArticleGeneratorUseCase:
    def __init__(
        self,
        rss_reader: RSSReader,
        ai_generator: AIGenerator,
        cache_service: CacheService,
    ):
        self.rss_reader = rss_reader
        self.ai_generator = ai_generator
        self.cache_service = cache_service

    async def get_article(self):
        cached_article = await self.cache_service.get_article()
        logger.info(f"Article from cache: {cached_article}")

        if cached_article and self._is_article_valid(cached_article):
            logger.info(f"Returning cached article: {cached_article=}")
            return cached_article

        word_of_day = await self.rss_reader.get_word_of_day()
        logger.info(f"Word of day: {word_of_day=}")
        article = await self.ai_generator.generate_article(word_of_day)
        await self.cache_service.save_article(article)

        logger.info(f"Article saved to cache: {article}")

        return article

    @staticmethod
    def _is_article_valid(article):
        today = datetime.now(timezone.utc).date()
        logger.info(f"Today: {today=}")
        article_date = article.created_at.date()
        logger.info(f"Article date: {article_date=}")
        logger.info(f"Is article valid: {article_date == today}")
        return article_date == today
