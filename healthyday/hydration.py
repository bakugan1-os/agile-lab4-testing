"""Розрахунок питного режиму та логіка нагадувань HealthyDay."""
from __future__ import annotations

import math
from datetime import datetime, time, timedelta

ML_PER_KG = 30          # базова норма: 30 мл води на 1 кг ваги
MIN_NORM_ML = 1500      # нижня межа денної норми
MAX_NORM_ML = 4000      # верхня межа денної норми
DEFAULT_GLASS_ML = 250


def daily_water_norm(weight_kg: float) -> int:
    """Денна норма води в мл, округлена до 50 мл і обмежена межами MIN..MAX."""
    if isinstance(weight_kg, bool) or not isinstance(weight_kg, (int, float)):
        raise TypeError("вага має бути числом")
    if not 20 <= weight_kg <= 300:
        raise ValueError("вага має бути в межах 20–300 кг")
    norm = round(weight_kg * ML_PER_KG / 50) * 50
    return max(MIN_NORM_ML, min(MAX_NORM_ML, norm))


def progress_percent(drunk_ml: int, norm_ml: int) -> int:
    """Відсоток виконання денної норми для кільцевого індикатора (0–100)."""
    if norm_ml <= 0:
        raise ValueError("норма має бути додатною")
    if drunk_ml < 0:
        raise ValueError("випитий об'єм не може бути від'ємним")
    return min(100, drunk_ml * 100 // norm_ml)


def glasses_left(drunk_ml: int, norm_ml: int, glass_ml: int = DEFAULT_GLASS_ML) -> int:
    """Скільки склянок ще потрібно випити до виконання норми."""
    if glass_ml <= 0:
        raise ValueError("об'єм склянки має бути додатним")
    remaining = norm_ml - drunk_ml
    return max(0, math.ceil(remaining / glass_ml))


def is_quiet_time(t: time, start: time = time(22, 0), end: time = time(8, 0)) -> bool:
    """Чи припадає момент t на «тихі години», коли нагадування не надсилаються."""
    if start == end:
        return False
    if start < end:                     # інтервал у межах однієї доби, напр. 13:00–15:00
        return start <= t < end
    return t >= start or t < end        # інтервал через північ, напр. 22:00–08:00


def should_remind(
    now: datetime,
    last_reminder: datetime | None,
    last_drink: datetime | None,
    interval_min: int = 60,
    pause_min: int = 30,
    quiet_start: time = time(22, 0),
    quiet_end: time = time(8, 0),
) -> bool:
    """Чи надсилати нагадування випити води в момент now."""
    if is_quiet_time(now.time(), quiet_start, quiet_end):
        return False
    if last_drink is not None and now - last_drink < timedelta(minutes=pause_min):
        return False                    # «розумна пауза»: користувач щойно пив
    if last_reminder is not None and now - last_reminder < timedelta(minutes=interval_min):
        return False
    return True
