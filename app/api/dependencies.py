from functools import lru_cache

from app.core.logger import logger
from app.core.config import settings

from app.infrastructure.ai_service import OpenAIArticleGenerator
from app.infrastructure.cache_service import RedisCache
from app.infrastructure.rss_service import WordsmithRSSReader
from app.use_cases.article_generator import ArticleGeneratorUseCase


@lru_cache
def get_rss_reader() -> WordsmithRSSReader:
    return WordsmithRSSReader(settings.RSS_FEED_URL)


@lru_cache
def get_ai_generator() -> OpenAIArticleGenerator:
    return OpenAIArticleGenerator(settings.PROXY_API_KEY)


@lru_cache
def get_cache_service() -> RedisCache:
    return RedisCache()


@lru_cache
def get_article_generator_use_case() -> ArticleGeneratorUseCase:
    logger.info("Creating article generator use case")
    return ArticleGeneratorUseCase(
        rss_reader=get_rss_reader(),
        ai_generator=get_ai_generator(),
        cache_service=get_cache_service(),
    )
