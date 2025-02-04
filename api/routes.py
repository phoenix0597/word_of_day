from fastapi import APIRouter, Depends, HTTPException

from core.logger import logger
from schemas.article_schema import ArticleResponse
from use_cases.article_generator import ArticleGeneratorUseCase
from api.dependencies import get_article_generator_use_case
from core.exceptions import WordOfDayException


router = APIRouter(prefix="/article", tags=["article"])


@router.get(
    "/word-of-day",
    response_model=ArticleResponse,
    summary="Get word of day article",
    description="Fetches the daily word and returns a generated article explaining it.",
)
async def get_word_of_day_article(
    use_case: ArticleGeneratorUseCase = Depends(get_article_generator_use_case),
):
    try:
        article = await use_case.get_article()
        return ArticleResponse.model_validate(article)
    except WordOfDayException as e:
        raise HTTPException(status_code=500, detail=str(e))
