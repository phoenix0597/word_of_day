# tests/conftest.py
from os.path import join

import pytest
from app.core.config import Settings, settings


def pytest_configure():
    import os

    if not os.path.exists(join(settings.BASE_DIR, ".env.test")):
        raise FileNotFoundError(
            "Create .env.test file in project root with test environment variables"
        )


@pytest.fixture(autouse=True)
def setup_test_environment(monkeypatch):
    monkeypatch.setenv("ENV_FILE", ".env.test")


@pytest.fixture
def mock_settings(monkeypatch):
    # Мокаем переменные окружения
    monkeypatch.setenv("PROXY_API_KEY", "test-key")
    monkeypatch.setenv("PROXY_API_BASE_URL", "http://test.ai")
    monkeypatch.setenv("REDIS_MAX_KEYS", "2")
    monkeypatch.setenv("REDIS_TTL", "86400")

    return Settings()
