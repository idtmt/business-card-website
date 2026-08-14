class ServiceError(Exception):
    """Базовое исключение сервисного слоя."""


class NotFoundError(ServiceError):
    """Запись не найдена."""


class AlreadyExistsError(ServiceError):
    """Запись уже существует."""


class ValidationError(ServiceError):
    """Некорректные входные данные."""