# tests/unit/test_rss_service.py
import pytest
from unittest.mock import AsyncMock, patch
from app.infrastructure.rss_service import WordsmithRSSReader
from app.core.exceptions import RSSFeedError


@pytest.mark.asyncio
async def test_get_word_of_day_success(mock_settings):
    mock_response = AsyncMock()
    mock_response.status = 200
    mock_response.text = AsyncMock(
        return_value="""
    <rss>
        <channel>
            <item>
                <title>Test Word</title>
                <description>Test Description</description>
            </item>
        </channel>
    </rss>
    """
    )

    with patch(
        "aiohttp.ClientSession.get",
        return_value=AsyncMock(__aenter__=AsyncMock(return_value=mock_response)),
    ):

        reader = WordsmithRSSReader("http://test.rss")
        result = await reader.get_word_of_day()

        assert result.word == "Test Word"
        assert result.description == "Test Description"


@pytest.mark.asyncio
async def test_get_word_of_day_http_error():
    mock_response = AsyncMock()
    mock_response.status = 500

    with patch("aiohttp.ClientSession.get", return_value=mock_response):
        reader = WordsmithRSSReader("http://test.rss")
        with pytest.raises(RSSFeedError):
            await reader.get_word_of_day()


@pytest.mark.asyncio
async def test_get_word_of_day_parsing_error():
    mock_response = AsyncMock()
    mock_response.status = 200
    mock_response.text.return_value = "invalid xml"

    with patch("aiohttp.ClientSession.get", return_value=mock_response):
        reader = WordsmithRSSReader("http://test.rss")
        with pytest.raises(RSSFeedError):
            await reader.get_word_of_day()
