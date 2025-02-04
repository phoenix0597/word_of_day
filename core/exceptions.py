class WordOfDayException(Exception):
    """Base exception for the application"""

    pass


class RSSFeedError(WordOfDayException):
    """Raised when there's an error fetching RSS feed"""

    pass


class AIGenerationError(WordOfDayException):
    """Raised when there's an error generating article using AI"""

    pass


class CacheError(WordOfDayException):
    """Raised when there's an error with cache operations"""

    pass
