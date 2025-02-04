from datetime import datetime
from pydantic import BaseModel, ConfigDict


class ArticleResponse(BaseModel):
    header: str
    body: str
    word: str
    created_at: datetime

    model_config = ConfigDict(
        from_attributes=True,
    )
