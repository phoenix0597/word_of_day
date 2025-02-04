# Word of Day Article API

Это FastAPI приложение, которое предоставляет API для получения ежедневного слова и генерации статьи, объясняющей его
значение. Приложение использует RSS-ленту для получения слова дня, генерирует статью с помощью AI и кэширует результаты
в Redis.

## Основные компоненты

1. FastAPI веб-сервер
2. RSS Reader для получения слова дня
3. AI генератор статей (использует OpenAI API через прокси-сервис proxyapi.ru)
4. Redis для кэширования
5. Логирование с использованием loguru

## Установка и запуск

### Предварительные требования

- Python 3.8+
- Docker и Docker Compose

### Шаги по установке

1. Клонируйте репозиторий:
   ```
   git clone https://github.com/phoenix0597/word_of_day.git
   cd word_of_day
   ```

2. Создайте виртуальное окружение и активируйте его:
   ```
   python -m venv .venv
   source venv/bin/activate  # Для Windows используйте: venv\Scripts\activate
   ```

3. Установите зависимости:
   ```
   pip install -r requirements.txt
   ```

4. Создайте файл `.env` в корневой директории проекта взяв за основу `.env.example` и заполните его своими данными:
   ```
   PROXY_API_BASE_URL=https://api.proxyapi.ru/openai/v1 - URL для конфигуурации OpenAI()
   PROXY_API_KEY=your_proxy_api_key - API-ключ сервиса proxyapi.ru
   AI_MODEL=gpt-4o-mini - здесь укажите выбранную вами модель OpenAI
   
   RSS_FEED_URL=https://wordsmith.org/awad/rss1.xml - путь для получения слова дня
   
   настройки Redis:
   REDIS_HOST=localhost
   REDIS_PORT=redis_port
   REDIS_DB=0
   REDIS_MAX_KEYS=2 - статьи за сколько дней хранить в кэше
   REDIS_TTL=86400 - время жизни статьи в секундах (24 часа = 60 * 60 * 24)
   ```

5. Запустите Redis с помощью Docker Compose:
   ```
   docker-compose up -d
   ```

6. Запустите приложение:
   ```
   python3 main.py  # Для Windows: python main.py
   ```

Приложение будет доступно по адресу `http://localhost:8000`.

API документация (Swagger UI) доступна по адресу `http://localhost:8000/docs`.

## Использование API

Для проверки получения статьи о слове дня, отправьте GET запрос на эндпоинт:

```
GET /api/v1/article/word-of-day
```

Ответ будет содержать заголовок, текст статьи, слово дня и дату создания.

## Разработка

Для запуска в режиме разработки с автоматической перезагрузкой при изменении кода:

```
uvicorn main:app --reload
```

## Логирование

Логи приложения по умолчанию выводятся в консоль, но могут быть настроены для записи в файлы.
Файлы логов будут сохраняются в директории `logs/app.log`.
