from collections.abc import Iterable

from backend.core.exceptions import ValidationError


def validate_required(
    value: str,
    field_name: str,
) -> str:
    """
    Проверяет обязательное строковое поле.
    Возвращает очищенное значение.
    """
    if not isinstance(value, str):
        raise ValidationError(
            f'Поле "{field_name}" должно быть строкой.'
        )

    value = value.strip()

    if not value:
        raise ValidationError(
            f'Поле "{field_name}" не может быть пустым.'
        )

    return value


def normalize_optional(
    value: str | None,
) -> str | None:
    """
    Нормализует необязательное строковое поле.
    Пустая строка преобразуется в None.
    """
    if value is None:
        return None

    if not isinstance(value, str):
        raise ValidationError(
            "Необязательное значение должно быть строкой или None."
        )

    value = value.strip()

    return value or None


def validate_position(
    position: int,
) -> int:
    """
    Проверяет корректность позиции.
    """
    if isinstance(position, bool) or not isinstance(position, int):
        raise ValidationError(
            "Позиция должна быть целым числом."
        )

    if position < 0:
        raise ValidationError(
            "Позиция не может быть отрицательной."
        )

    return position


def validate_latitude(
    latitude: float,
) -> float:
    """
    Проверяет широту.
    """
    if isinstance(latitude, bool) or not isinstance(
        latitude,
        (int, float),
    ):
        raise ValidationError(
            "Широта должна быть числом."
        )

    if not -90 <= latitude <= 90:
        raise ValidationError(
            "Широта должна быть в диапазоне от -90 до 90."
        )

    return float(latitude)


def validate_longitude(
    longitude: float,
) -> float:
    """
    Проверяет долготу.
    """
    if isinstance(longitude, bool) or not isinstance(
        longitude,
        (int, float),
    ):
        raise ValidationError(
            "Долгота должна быть числом."
        )

    if not -180 <= longitude <= 180:
        raise ValidationError(
            "Долгота должна быть в диапазоне от -180 до 180."
        )

    return float(longitude)


def validate_visibility(
    is_hidden: bool,
) -> bool:
    """
    Проверяет признак скрытия записи.
    """
    if not isinstance(is_hidden, bool):
        raise ValidationError(
            "Значение is_hidden должно быть bool."
        )

    return is_hidden


def validate_id(
    record_id: int,
    field_name: str = "id",
) -> int:
    """
    Проверяет корректность идентификатора.
    """
    if isinstance(record_id, bool) or not isinstance(
        record_id,
        int,
    ):
        raise ValidationError(
            f'"{field_name}" должен быть целым числом.'
        )

    if record_id <= 0:
        raise ValidationError(
            f'"{field_name}" должен быть больше нуля.'
        )

    return record_id


def validate_ids(*ids: int) -> None:
    """
    Проверяет несколько идентификаторов.
    """
    for record_id in ids:
        validate_id(record_id)


def validate_weekday(
    weekday: int,
) -> int:
    """
    Проверяет день недели.
    0 — понедельник, 6 — воскресенье.
    """
    if isinstance(weekday, bool) or not isinstance(
        weekday,
        int,
    ):
        raise ValidationError(
            "День недели должен быть целым числом."
        )

    if not 0 <= weekday <= 6:
        raise ValidationError(
            "День недели должен быть в диапазоне от 0 до 6."
        )

    return weekday


def validate_time(
    value: str,
    field_name: str,
) -> str:
    """
    Проверяет время в формате HH:MM.
    Возвращает нормализованное значение.
    """
    if not isinstance(value, str):
        raise ValidationError(
            f'Поле "{field_name}" должно быть строкой.'
        )

    value = value.strip()

    if not value:
        raise ValidationError(
            f'Поле "{field_name}" не может быть пустым.'
        )

    parts = value.split(":")

    if len(parts) != 2:
        raise ValidationError(
            f'Поле "{field_name}" должно иметь формат HH:MM.'
        )

    hours, minutes = parts

    if not hours.isdigit() or not minutes.isdigit():
        raise ValidationError(
            f'Поле "{field_name}" должно иметь формат HH:MM.'
        )

    hours = int(hours)
    minutes = int(minutes)

    if not 0 <= hours <= 23:
        raise ValidationError(
            f'Некорректное значение часов в поле "{field_name}".'
        )

    if not 0 <= minutes <= 59:
        raise ValidationError(
            f'Некорректное значение минут в поле "{field_name}".'
        )

    return f"{hours:02d}:{minutes:02d}"


def validate_collection_not_empty(
    values: Iterable,
    field_name: str,
) -> None:
    """
    Проверяет, что коллекция не пустая.
    """
    if not any(True for _ in values):
        raise ValidationError(
            f'"{field_name}" не может быть пустым.'
        )


def validate_bool(
    value: bool,
    field_name: str,
) -> bool:
    if not isinstance(value, bool):
        raise ValidationError(
            f'Поле "{field_name}" должно быть bool.'
        )

    return value