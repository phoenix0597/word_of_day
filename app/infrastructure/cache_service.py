import redis.asyncio as redis
import json
from datetime import datetime, timezone

from app.core.logger import logger
from app.domain.interfaces import CacheService
from app.domain.entities import Article
from app.core.exceptions import CacheError
from app.core.config import settings


class RedisCache(CacheService):
    key_prefix = "word_of_day:"

    def __init__(self):
        self.redis = redis.from_url(
            url=f"redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}",
            password=settings.REDIS_PASSWORD,
            decode_responses=True,
        )

    async def get_article(self) -> Article | None:
        try:
            key = self._get_today_key()
            data = await self.redis.get(key)
            logger.info(f"Article got from cache: \n{data=}")
            if not data:
                return None

            article_dict = json.loads(data)
            return Article(**article_dict)

        except Exception as e:
            raise CacheError(f"Error retrieving article from cache: {e}")

    async def save_article(
        self, article: Article, max_keys_limit: int = settings.REDIS_MAX_KEYS
    ) -> None:
        try:
            key = self._get_today_key()
            article_dict = {
                "header": article.header,
                "body": article.body,
                "word": article.word,
                "created_at": datetime.now(timezone.utc).date().isoformat(),
            }
            logger.info(f"Article to save to cache: {article_dict=}")

            # Управляем размером кэша
            await self._manage_cache_size()

            # Сохраняем новый ключ с установленным временем жизни (24 часа)
            await self.redis.set(
                key,
                json.dumps(article_dict),
                ex=settings.REDIS_TTL,  # 60 * 60 * 24 = 86400 (expires in 24 hours)
            )

        except Exception as e:
            raise CacheError(f"Error saving article to cache: {e}")

    async def _manage_cache_size(self) -> None:
        """
        Управление размером кэша.
        Удаляет самый старый ключ, если количество ключей достигает или превышает лимит.
        """
        keys = await self.redis.keys(f"{self.key_prefix}*")
        if len(keys) >= settings.REDIS_MAX_KEYS:
            oldest_key = min(keys)
            await self.redis.delete(oldest_key)
            logger.info(f"Deleted oldest cache key: {oldest_key}")

    @staticmethod
    def _get_today_key() -> str:
        today = datetime.now(timezone.utc).date().isoformat()
        return f"{RedisCache.key_prefix}{today}"
