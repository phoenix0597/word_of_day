# tests/unit/test_cache_service.py
import pytest
from datetime import datetime, timezone
from unittest.mock import AsyncMock
from app.infrastructure.cache_service import RedisCache
from app.domain.entities import Article


@pytest.fixture
def redis_mock():
    mock = AsyncMock()
    mock.get.return_value = None
    mock.set.return_value = True
    mock.keys.return_value = []
    return mock


@pytest.mark.asyncio
async def test_save_and_get_article(redis_mock):
    cache = RedisCache()
    cache.redis = redis_mock

    test_article = Article(
        header="Test",
        body="Content",
        word="test",
        created_at=datetime.now(timezone.utc),
    )

    await cache.save_article(test_article)
    await cache.get_article()

    assert redis_mock.set.called
    assert redis_mock.get.called


@pytest.mark.asyncio
async def test_cache_management(redis_mock, mocker):
    mocker.patch("app.core.config.settings.REDIS_MAX_KEYS", 3)  # Мокаем REDIS_MAX_KEYS
    cache = RedisCache()
    cache.redis = redis_mock
    redis_mock.keys.return_value = ["key1", "key2", "key3"]

    await cache.save_article(
        Article(
            header="Test",
            body="Content",
            word="test",
            created_at=datetime.now(timezone.utc),
        )
    )

    assert redis_mock.delete.called


@pytest.mark.asyncio
async def test_get_today_key():
    cache = RedisCache()
    key = cache._get_today_key()
    assert key.startswith("word_of_day:")
    assert datetime.now(timezone.utc).date().isoformat() in key
