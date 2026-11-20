from datetime import datetime, time, timedelta

import pytest

from healthyday.hydration import (
    daily_water_norm,
    glasses_left,
    is_quiet_time,
    progress_percent,
    should_remind,
)


# ---------- daily_water_norm ----------
@pytest.mark.parametrize(
    "weight, expected",
    [
        (70, 2100),     # 70 × 30 = 2100
        (60, 1800),
        (82.5, 2500),   # 2475 → округлення до 50 мл
        (40, 1500),     # 1200 → нижня межа
        (150, 4000),    # 4500 → верхня межа
    ],
)
def test_daily_water_norm(weight, expected):
    assert daily_water_norm(weight) == expected


@pytest.mark.parametrize("weight", [0, 19.9, 301, -70])
def test_daily_water_norm_out_of_range(weight):
    with pytest.raises(ValueError):
        daily_water_norm(weight)


@pytest.mark.parametrize("weight", ["70", None, True])
def test_daily_water_norm_wrong_type(weight):
    with pytest.raises(TypeError):
        daily_water_norm(weight)


# ---------- progress_percent / glasses_left ----------
@pytest.mark.parametrize(
    "drunk, norm, expected",
    [(0, 2100, 0), (1050, 2100, 50), (1250, 2100, 59), (2100, 2100, 100), (3000, 2100, 100)],
)
def test_progress_percent(drunk, norm, expected):
    assert progress_percent(drunk, norm) == expected


def test_progress_percent_invalid():
    with pytest.raises(ValueError):
        progress_percent(500, 0)
    with pytest.raises(ValueError):
        progress_percent(-1, 2000)


@pytest.mark.parametrize(
    "drunk, norm, glass, expected",
    [(0, 2100, 250, 9), (1250, 2100, 250, 4), (2100, 2100, 250, 0), (2500, 2100, 250, 0), (1000, 2000, 500, 2)],
)
def test_glasses_left(drunk, norm, glass, expected):
    assert glasses_left(drunk, norm, glass) == expected


def test_glasses_left_invalid_glass():
    with pytest.raises(ValueError):
        glasses_left(0, 2000, 0)


# ---------- is_quiet_time ----------
def hhmm(value):
    return value.strftime("%H:%M") if isinstance(value, time) else str(value)


@pytest.mark.parametrize(
    "t, expected",
    [
        (time(21, 59), False),
        (time(22, 0), True),    # початок тихих годин включно
        (time(23, 30), True),
        (time(0, 0), True),     # північ
        (time(3, 15), True),
        (time(7, 59), True),
        (time(8, 0), False),    # кінець тихих годин не включно
        (time(12, 0), False),
    ],
    ids=hhmm,
)
def test_quiet_hours_across_midnight(t, expected):
    assert is_quiet_time(t, time(22, 0), time(8, 0)) is expected


@pytest.mark.parametrize(
    "t, expected",
    [(time(12, 59), False), (time(13, 0), True), (time(14, 30), True), (time(15, 0), False)],
    ids=hhmm,
)
def test_quiet_hours_within_day(t, expected):
    assert is_quiet_time(t, time(13, 0), time(15, 0)) is expected


def test_quiet_hours_disabled_when_start_equals_end():
    assert is_quiet_time(time(10, 0), time(9, 0), time(9, 0)) is False


# ---------- should_remind ----------
@pytest.fixture
def noon():
    return datetime(2026, 11, 20, 12, 0)


def test_remind_when_nothing_happened_yet(noon):
    assert should_remind(noon, last_reminder=None, last_drink=None) is True


def test_no_remind_during_quiet_hours():
    night = datetime(2026, 11, 20, 23, 30)
    assert should_remind(night, last_reminder=None, last_drink=None) is False


def test_smart_pause_after_drink(noon):
    assert should_remind(noon, None, last_drink=noon - timedelta(minutes=10)) is False
    assert should_remind(noon, None, last_drink=noon - timedelta(minutes=30)) is True


def test_interval_between_reminders(noon):
    assert should_remind(noon, last_reminder=noon - timedelta(minutes=45), last_drink=None) is False
    assert should_remind(noon, last_reminder=noon - timedelta(minutes=60), last_drink=None) is True
    assert should_remind(noon, noon - timedelta(minutes=80), None, interval_min=90) is False
