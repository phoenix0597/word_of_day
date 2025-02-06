# tests/integration/test_use_case.py
import pytest
from datetime import datetime, timezone, timedelta
from unittest.mock import AsyncMock
from app.use_cases.article_generator import ArticleGeneratorUseCase
from app.domain.entities import Article, WordOfDay


@pytest.fixture
def use_case_mocks():
    rss_reader = AsyncMock()
    ai_generator = AsyncMock()
    cache_service = AsyncMock()

    return ArticleGeneratorUseCase(
        rss_reader=rss_reader, ai_generator=ai_generator, cache_service=cache_service
    )


@pytest.mark.asyncio
async def test_get_article_with_cache(use_case_mocks):
    test_article = Article(
        header="Cached",
        body="Content",
        word="test",
        created_at=datetime.now(timezone.utc),
    )
    use_case_mocks.cache_service.get_article.return_value = test_article

    result = await use_case_mocks.get_article()

    assert result == test_article
    use_case_mocks.rss_reader.get_word_of_day.assert_not_called()


@pytest.mark.asyncio
async def test_get_article_without_cache(use_case_mocks):
    test_word = WordOfDay(word="test", description="test")
    test_article = Article(
        header="New", body="Content", word="test", created_at=datetime.now(timezone.utc)
    )

    use_case_mocks.cache_service.get_article.return_value = None
    use_case_mocks.rss_reader.get_word_of_day.return_value = test_word
    use_case_mocks.ai_generator.generate_article.return_value = test_article

    result = await use_case_mocks.get_article()

    assert result == test_article
    use_case_mocks.cache_service.save_article.assert_called_with(test_article)


@pytest.mark.asyncio
async def test_article_validation():
    valid_article = Article(
        header="Valid",
        body="Content",
        word="test",
        created_at=datetime.now(timezone.utc),
    )

    invalid_article = Article(
        header="Invalid",
        body="Content",
        word="test",
        created_at=datetime.now(timezone.utc) - timedelta(days=1),
    )

    assert ArticleGeneratorUseCase._is_article_valid(valid_article)
    assert not ArticleGeneratorUseCase._is_article_valid(invalid_article)
