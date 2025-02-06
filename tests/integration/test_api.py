# tests/integration/test_api.py
from app.core.logger import logger

from datetime import datetime
from fastapi.testclient import TestClient
from unittest.mock import patch, AsyncMock
from app.schemas.article_schema import ArticleResponse


# @patch("app.api.dependencies.get_article_generator_use_case")
def test_get_word_of_day_success():
    from app.main import app

    client = TestClient(app)

    # Создаем мок для экземпляра use_case
    mock_uc_instance = AsyncMock()
    mock_uc_instance.get_article.return_value = ArticleResponse(
        header="Test",
        body="Content",
        word="test",
        created_at=datetime(2024, 1, 1, 0, 0, 0),
    )

    # Переопределяем зависимость
    from app.api.dependencies import get_article_generator_use_case

    app.dependency_overrides[get_article_generator_use_case] = lambda: mock_uc_instance  # type: ignore

    response = client.get("/api/v1/article/word-of-day")
    print(f"{response.json()=}")

    assert response.status_code == 200
    assert response.json()["word"] == "test"

    # Чистим переопределения, если потребуется
    app.dependency_overrides.clear()  # type: ignore


# @patch("app.api.dependencies.get_article_generator_use_case")
def test_get_word_of_day_error():
    from app.core.exceptions import WordOfDayException

    from app.main import app

    # Переопределяем зависимость
    from app.api.dependencies import get_article_generator_use_case

    client = TestClient(app)

    # Создаем мок для экземпляра use_case,
    # который при вызове метода get_article кидает исключение WordOfDayException
    mock_uc_instance = AsyncMock()
    mock_uc_instance.get_article.side_effect = WordOfDayException("Test error")

    # Переопределяем зависимость FastAPI. Используем lambda без параметров
    app.dependency_overrides[get_article_generator_use_case] = lambda: mock_uc_instance  # type: ignore

    # Выполняем запрос к эндпоинту
    response = client.get("/api/v1/article/word-of-day")

    assert response.status_code == 500
    assert "Test error" in response.json()["detail"]

    # Чистим переопределения зависимости, чтобы они не влияли на другие тесты
    app.dependency_overrides.clear()  # type: ignore
