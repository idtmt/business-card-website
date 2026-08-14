import pytest

from backend.core.exceptions import ValidationError
from backend.utils.validators import (
    normalize_optional,
    validate_bool,
    validate_collection_not_empty,
    validate_id,
    validate_ids,
    validate_latitude,
    validate_longitude,
    validate_position,
    validate_required,
    validate_time,
    validate_visibility,
    validate_weekday,
)


# ============================================================
# validate_required
# ============================================================


@pytest.mark.unit
@pytest.mark.parametrize(
    ("value", "expected"),
    [
        ("Hello", "Hello"),
        (" Hello ", "Hello"),
        ("  Hello world  ", "Hello world"),
    ],
)
def test_validate_required_returns_stripped_value(
    value,
    expected,
):
    assert validate_required(value, "name") == expected


@pytest.mark.unit
@pytest.mark.parametrize(
    "value",
    [
        "",
        " ",
        "   ",
        "\t",
        "\n",
    ],
)
def test_validate_required_rejects_empty_value(value):
    with pytest.raises(
        ValidationError,
        match='Поле "name" не может быть пустым.',
    ):
        validate_required(value, "name")


@pytest.mark.unit
@pytest.mark.parametrize(
    "value",
    [
        None,
        123,
        1.5,
        True,
        False,
        [],
        {},
    ],
)
def test_validate_required_rejects_non_string(value):
    with pytest.raises(
        ValidationError,
        match='Поле "name" должно быть строкой.',
    ):
        validate_required(value, "name")


# ============================================================
# normalize_optional
# ============================================================


@pytest.mark.unit
@pytest.mark.parametrize(
    ("value", "expected"),
    [
        (None, None),
        ("", None),
        (" ", None),
        ("   ", None),
        ("Hello", "Hello"),
        (" Hello ", "Hello"),
    ],
)
def test_normalize_optional(value, expected):
    assert normalize_optional(value) == expected


@pytest.mark.unit
@pytest.mark.parametrize(
    "value",
    [
        123,
        1.5,
        True,
        False,
        [],
        {},
    ],
)
def test_normalize_optional_rejects_non_string(value):
    with pytest.raises(
        ValidationError,
        match="Необязательное значение должно быть строкой или None.",
    ):
        normalize_optional(value)


# ============================================================
# validate_position
# ============================================================


@pytest.mark.unit
@pytest.mark.parametrize(
    ("position", "expected"),
    [
        (0, 0),
        (1, 1),
        (10, 10),
        (999, 999),
    ],
)
def test_validate_position_accepts_valid_values(
    position,
    expected,
):
    assert validate_position(position) == expected


@pytest.mark.unit
def test_validate_position_accepts_zero():
    assert validate_position(0) == 0


@pytest.mark.unit
def test_validate_position_rejects_negative_value():
    with pytest.raises(
        ValidationError,
        match="Позиция не может быть отрицательной.",
    ):
        validate_position(-1)


@pytest.mark.unit
@pytest.mark.parametrize(
    "value",
    [
        1.0,
        "1",
        None,
        [],
        {},
        True,
        False,
    ],
)
def test_validate_position_rejects_non_integer(value):
    with pytest.raises(
        ValidationError,
        match="Позиция должна быть целым числом.",
    ):
        validate_position(value)


# ============================================================
# validate_latitude
# ============================================================


@pytest.mark.unit
@pytest.mark.parametrize(
    ("latitude", "expected"),
    [
        (0, 0.0),
        (41, 41.0),
        (41.311, 41.311),
        (-41.311, -41.311),
        (90, 90.0),
        (-90, -90.0),
    ],
)
def test_validate_latitude_accepts_valid_values(
    latitude,
    expected,
):
    assert validate_latitude(latitude) == expected


@pytest.mark.unit
@pytest.mark.parametrize(
    "latitude",
    [
        90.1,
        -90.1,
        180,
        -180,
    ],
)
def test_validate_latitude_rejects_out_of_range(latitude):
    with pytest.raises(
        ValidationError,
        match="Широта должна быть в диапазоне от -90 до 90.",
    ):
        validate_latitude(latitude)


@pytest.mark.unit
@pytest.mark.parametrize(
    "value",
    [
        "41.311",
        None,
        [],
        {},
        True,
        False,
    ],
)
def test_validate_latitude_rejects_non_numeric(value):
    with pytest.raises(
        ValidationError,
        match="Широта должна быть числом.",
    ):
        validate_latitude(value)


# ============================================================
# validate_longitude
# ============================================================


@pytest.mark.unit
@pytest.mark.parametrize(
    ("longitude", "expected"),
    [
        (0, 0.0),
        (69, 69.0),
        (69.279, 69.279),
        (-69.279, -69.279),
        (180, 180.0),
        (-180, -180.0),
    ],
)
def test_validate_longitude_accepts_valid_values(
    longitude,
    expected,
):
    assert validate_longitude(longitude) == expected


@pytest.mark.unit
@pytest.mark.parametrize(
    "longitude",
    [
        180.1,
        -180.1,
        360,
        -360,
    ],
)
def test_validate_longitude_rejects_out_of_range(longitude):
    with pytest.raises(
        ValidationError,
        match="Долгота должна быть в диапазоне от -180 до 180.",
    ):
        validate_longitude(longitude)


@pytest.mark.unit
@pytest.mark.parametrize(
    "value",
    [
        "69.279",
        None,
        [],
        {},
        True,
        False,
    ],
)
def test_validate_longitude_rejects_non_numeric(value):
    with pytest.raises(
        ValidationError,
        match="Долгота должна быть числом.",
    ):
        validate_longitude(value)


# ============================================================
# validate_visibility
# ============================================================


@pytest.mark.unit
@pytest.mark.parametrize(
    "value",
    [
        True,
        False,
    ],
)
def test_validate_visibility_accepts_bool(value):
    assert validate_visibility(value) is value


@pytest.mark.unit
@pytest.mark.parametrize(
    "value",
    [
        0,
        1,
        "true",
        "false",
        None,
        [],
        {},
    ],
)
def test_validate_visibility_rejects_non_bool(value):
    with pytest.raises(
        ValidationError,
        match="Значение is_hidden должно быть bool.",
    ):
        validate_visibility(value)


# ============================================================
# validate_id
# ============================================================


@pytest.mark.unit
@pytest.mark.parametrize(
    ("record_id", "expected"),
    [
        (1, 1),
        (2, 2),
        (100, 100),
        (999999, 999999),
    ],
)
def test_validate_id_accepts_positive_integer(
    record_id,
    expected,
):
    assert validate_id(record_id) == expected


@pytest.mark.unit
def test_validate_id_rejects_zero():
    with pytest.raises(
        ValidationError,
        match='"id" должен быть больше нуля.',
    ):
        validate_id(0)


@pytest.mark.unit
@pytest.mark.parametrize(
    "record_id",
    [
        -1,
        -100,
    ],
)
def test_validate_id_rejects_negative_integer(record_id):
    with pytest.raises(
        ValidationError,
        match='"id" должен быть больше нуля.',
    ):
        validate_id(record_id)


@pytest.mark.unit
@pytest.mark.parametrize(
    "value",
    [
        True,
        False,
        1.0,
        "1",
        None,
        [],
        {},
    ],
)
def test_validate_id_rejects_invalid_type(value):
    with pytest.raises(
        ValidationError,
        match='"id" должен быть целым числом.',
    ):
        validate_id(value)


@pytest.mark.unit
def test_validate_id_uses_custom_field_name():
    with pytest.raises(
        ValidationError,
        match='"location_id" должен быть больше нуля.',
    ):
        validate_id(0, "location_id")


# ============================================================
# validate_ids
# ============================================================


@pytest.mark.unit
def test_validate_ids_accepts_valid_ids():
    assert validate_ids(1, 2, 3, 10) is None


@pytest.mark.unit
def test_validate_ids_accepts_empty_arguments():
    assert validate_ids() is None


@pytest.mark.unit
def test_validate_ids_rejects_invalid_id():
    with pytest.raises(
        ValidationError,
        match='"id" должен быть больше нуля.',
    ):
        validate_ids(1, 2, 0, 4)


@pytest.mark.unit
def test_validate_ids_rejects_invalid_type():
    with pytest.raises(
        ValidationError,
        match='"id" должен быть целым числом.',
    ):
        validate_ids(1, "2", 3)


# ============================================================
# validate_weekday
# ============================================================


@pytest.mark.unit
@pytest.mark.parametrize(
    "weekday",
    range(7),
)
def test_validate_weekday_accepts_valid_values(weekday):
    assert validate_weekday(weekday) == weekday


@pytest.mark.unit
@pytest.mark.parametrize(
    "weekday",
    [
        -1,
        7,
        8,
        100,
    ],
)
def test_validate_weekday_rejects_out_of_range(weekday):
    with pytest.raises(
        ValidationError,
        match="День недели должен быть в диапазоне от 0 до 6.",
    ):
        validate_weekday(weekday)


@pytest.mark.unit
@pytest.mark.parametrize(
    "value",
    [
        True,
        False,
        1.0,
        "1",
        None,
        [],
        {},
    ],
)
def test_validate_weekday_rejects_invalid_type(value):
    with pytest.raises(
        ValidationError,
        match="День недели должен быть целым числом.",
    ):
        validate_weekday(value)


# ============================================================
# validate_time
# ============================================================


@pytest.mark.unit
@pytest.mark.parametrize(
    ("value", "expected"),
    [
        ("00:00", "00:00"),
        ("01:05", "01:05"),
        ("09:30", "09:30"),
        ("12:45", "12:45"),
        ("23:59", "23:59"),
        (" 09:30 ", "09:30"),
        ("9:30", "09:30"),
        ("1:05", "01:05"),
        ("9:5", "09:05"),
    ],
)
def test_validate_time_accepts_valid_values(
    value,
    expected,
):
    assert validate_time(value, "start_time") == expected


@pytest.mark.unit
@pytest.mark.parametrize(
    "value",
    [
        "",
        " ",
        "930",
        "09",
        "09:30:00",
        "09-30",
        "09.30",
        "abc",
        "09:abc",
        "abc:30",
    ],
)
def test_validate_time_rejects_invalid_format(value):
    with pytest.raises(
        ValidationError,
    ):
        validate_time(value, "start_time")


@pytest.mark.unit
@pytest.mark.parametrize(
    "value",
    [
        "24:00",
        "25:00",
        "99:00",
    ],
)
def test_validate_time_rejects_invalid_hours(value):
    with pytest.raises(
        ValidationError,
        match='Некорректное значение часов в поле "start_time".',
    ):
        validate_time(value, "start_time")


@pytest.mark.unit
@pytest.mark.parametrize(
    "value",
    [
        "00:60",
        "12:99",
        "23:100",
    ],
)
def test_validate_time_rejects_invalid_minutes(value):
    with pytest.raises(
        ValidationError,
        match='Некорректное значение минут в поле "start_time".',
    ):
        validate_time(value, "start_time")


@pytest.mark.unit
@pytest.mark.parametrize(
    "value",
    [
        None,
        930,
        9.30,
        True,
        False,
        [],
        {},
    ],
)
def test_validate_time_rejects_non_string(value):
    with pytest.raises(
        ValidationError,
        match='Поле "start_time" должно быть строкой.',
    ):
        validate_time(value, "start_time")


@pytest.mark.unit
def test_validate_time_uses_custom_field_name():
    with pytest.raises(
        ValidationError,
        match='Поле "end_time" не может быть пустым.',
    ):
        validate_time(" ", "end_time")


# ============================================================
# validate_collection_not_empty
# ============================================================


@pytest.mark.unit
@pytest.mark.parametrize(
    "values",
    [
        [1],
        [1, 2, 3],
        ("item",),
        {"key": "value"},
        {1, 2, 3},
        (value for value in [1, 2, 3]),
    ],
)
def test_validate_collection_not_empty_accepts_non_empty(
    values,
):
    assert validate_collection_not_empty(
        values,
        "items",
    ) is None


@pytest.mark.unit
@pytest.mark.parametrize(
    "values",
    [
        [],
        (),
        set(),
        {},
    ],
)
def test_validate_collection_not_empty_rejects_empty(
    values,
):
    with pytest.raises(
        ValidationError,
        match='"items" не может быть пустым.',
    ):
        validate_collection_not_empty(
            values,
            "items",
        )


# ============================================================
# validate_bool
# ============================================================


@pytest.mark.unit
@pytest.mark.parametrize(
    "value",
    [
        True,
        False,
    ],
)
def test_validate_bool_accepts_bool(value):
    assert validate_bool(value, "is_hidden") is value


@pytest.mark.unit
@pytest.mark.parametrize(
    "value",
    [
        0,
        1,
        "true",
        "false",
        None,
        [],
        {},
    ],
)
def test_validate_bool_rejects_non_bool(value):
    with pytest.raises(
        ValidationError,
        match='Поле "is_hidden" должно быть bool.',
    ):
        validate_bool(value, "is_hidden")