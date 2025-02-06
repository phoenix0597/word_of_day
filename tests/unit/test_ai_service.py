# tests/unit/test_ai_service.py
import pytest
from unittest.mock import AsyncMock
from app.infrastructure.ai_service import OpenAIArticleGenerator
from app.domain.entities import WordOfDay
from app.core.exceptions import AIGenerationError


@pytest.fixture
def mock_openai():
    mock = AsyncMock()
    mock.chat.completions.create.return_value = AsyncMock(
        choices=[AsyncMock(message=AsyncMock(content="Header\n\nBody"))]
    )
    return mock


@pytest.mark.asyncio
async def test_generate_article_success(mock_openai):
    generator = OpenAIArticleGenerator()
    generator.client = mock_openai

    word = WordOfDay(word="test", description="test description")
    result = await generator.generate_article(word)

    assert result.header == "Header"
    assert result.body == "Body"


@pytest.mark.asyncio
async def test_generate_article_error():
    generator = OpenAIArticleGenerator()
    generator.client = AsyncMock()
    generator.client.chat.completions.create.side_effect = Exception("API Error")

    with pytest.raises(AIGenerationError):
        await generator.generate_article(WordOfDay(word="test", description="test"))
