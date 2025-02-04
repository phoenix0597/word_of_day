import aiohttp
import xml.etree.ElementTree as ET

from core.logger import logger
from domain.interfaces import RSSReader
from domain.entities import WordOfDay
from core.exceptions import RSSFeedError


class WordsmithRSSReader(RSSReader):
    def __init__(self, rss_url: str):
        self.rss_url = rss_url

    async def get_word_of_day(self) -> WordOfDay:
        try:
            logger.info(f"Fetching RSS feed from {self.rss_url}")
            async with aiohttp.ClientSession() as session:
                async with session.get(self.rss_url) as response:
                    if response.status != 200:
                        raise RSSFeedError(
                            f"RSS feed returned status: {response.status}"
                        )
                    content = await response.text()

                root = ET.fromstring(content)
                item = root.find(".//item")
                if item is None:
                    raise RSSFeedError("No item found in RSS feed")

                word = item.find("title").text
                description = item.find("description").text
                logger.info(f"RSS feed returned: {word=}")
                logger.info(f"RSS feed returned: {description=}")

                return WordOfDay(
                    word=word,
                    description=description,
                )

        except Exception as e:
            raise RSSFeedError(f"Error fetching word of day: {e}")
