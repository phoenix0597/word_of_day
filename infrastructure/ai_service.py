import openai
from datetime import datetime

from core.logger import logger
from core.config import settings
from core.exceptions import AIGenerationError
from domain.interfaces import AIGenerator
from domain.entities import Article, WordOfDay


class OpenAIArticleGenerator(AIGenerator):
    def __init__(
        self,
        api_key: str = settings.PROXY_API_KEY,
        api_base: str = settings.PROXY_API_BASE_URL,
    ):
        self.client = openai.AsyncOpenAI(api_key=api_key, base_url=api_base)
        logger.info(f"Using OpenAI API with base URL: {api_base=}")

    async def generate_article(self, word: WordOfDay) -> Article:
        logger.info(
            f"Generating article for word, description: {word.word=}, {word.description=}"
        )
        try:
            prompt = f"Create an educational article about the word '{word.word}'. {word.description}"

            completion = await self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {
                        "role": "system",
                        "content": "Generate a short article with header (no more than 50 chars) "
                        "and body (no more than 300 chars)",
                    },
                    {
                        "role": "user",
                        "content": prompt,
                    },
                ],
            )

            content = completion.choices[0].message.content
            header, body = content.split("\n\n", 1)

            logger.info(f"Generated article: {header=}, {body=}")

            return Article(
                header=header[:50],
                body=body[:300],
                word=word.word,
                created_at=datetime.now(),
            )
        except Exception as e:
            raise AIGenerationError(f"Error generating article: {e}")
