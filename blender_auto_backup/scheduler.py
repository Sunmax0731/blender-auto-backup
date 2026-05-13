"""Timer scheduling for automatic backups."""

from __future__ import annotations

from datetime import datetime, timedelta
import time

import bpy

from .services.backup_service import BackupError

_next_due_monotonic = 0.0
_timer_enabled = False
_in_progress = False


def ensure_timer(first_interval: float = 1.0) -> None:
    global _timer_enabled
    _timer_enabled = True
    if not bpy.app.timers.is_registered(_timer_tick):
        bpy.app.timers.register(_timer_tick, first_interval=first_interval, persistent=True)


def disable_timer() -> None:
    global _timer_enabled
    _timer_enabled = False
    if bpy.app.timers.is_registered(_timer_tick):
        bpy.app.timers.unregister(_timer_tick)


def start_for_settings(settings) -> None:
    global _next_due_monotonic
    interval_seconds = _interval_seconds(settings)
    _next_due_monotonic = time.monotonic() + interval_seconds
    settings.next_run_at = _format_datetime(datetime.now() + timedelta(seconds=interval_seconds))
    ensure_timer(first_interval=1.0)


def _interval_seconds(settings) -> int:
    return max(60, int(settings.interval_minutes) * 60)


def _format_datetime(value: datetime) -> str:
    return value.strftime("%Y-%m-%d %H:%M:%S")


def _timer_tick():
    global _in_progress, _next_due_monotonic
    if not _timer_enabled:
        return None

    scene = getattr(bpy.context, "scene", None)
    settings = getattr(scene, "blender_auto_backup", None) if scene else None
    if settings is None or not settings.enabled:
        return 30.0

    interval_seconds = _interval_seconds(settings)
    now = time.monotonic()
    if _next_due_monotonic <= 0.0:
        _next_due_monotonic = now + interval_seconds
        settings.next_run_at = _format_datetime(datetime.now() + timedelta(seconds=interval_seconds))
        return min(30.0, float(interval_seconds))

    if now < _next_due_monotonic:
        return max(1.0, min(30.0, _next_due_monotonic - now))

    if _in_progress:
        return 5.0

    _in_progress = True
    try:
        from .operators import perform_backup_for_settings

        perform_backup_for_settings(settings)
    except BackupError as exc:
        settings.last_run_at = _format_datetime(datetime.now())
        settings.last_status = f"Error: {exc}"
    except Exception as exc:  # Keep the Blender timer alive after unexpected failures.
        settings.last_run_at = _format_datetime(datetime.now())
        settings.last_status = f"Unexpected error: {exc}"
    finally:
        _in_progress = False

    _next_due_monotonic = time.monotonic() + interval_seconds
    settings.next_run_at = _format_datetime(datetime.now() + timedelta(seconds=interval_seconds))
    return min(30.0, float(interval_seconds))

