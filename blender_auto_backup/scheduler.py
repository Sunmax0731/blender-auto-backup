"""Timer scheduling for automatic backups."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timedelta
from queue import Empty, SimpleQueue
from threading import Lock, Thread
import time

import bpy

from .services.backup_service import BackupError, BackupResult, run_backup

_next_due_monotonic = 0.0
_timer_enabled = False
_in_progress = False
_worker_lock = Lock()
_worker_thread: Thread | None = None
_finished_jobs: SimpleQueue["BackupJobOutcome"] = SimpleQueue()


@dataclass(frozen=True)
class BackupJobRequest:
    source_directory: str
    backup_directory: str | None
    max_backups: int
    project_label: str | None
    include_globs: str
    exclude_globs: str
    destination_mode: str


@dataclass(frozen=True)
class BackupJobOutcome:
    status: str
    finished_at: datetime
    result: BackupResult | None = None
    error: str = ""


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


def start_background_backup(
    *,
    source_directory: str,
    backup_directory: str | None,
    max_backups: int,
    project_label: str | None,
    include_globs: str,
    exclude_globs: str,
    destination_mode: str,
) -> bool:
    global _worker_thread
    request = BackupJobRequest(
        source_directory=source_directory,
        backup_directory=backup_directory,
        max_backups=max_backups,
        project_label=project_label,
        include_globs=include_globs,
        exclude_globs=exclude_globs,
        destination_mode=destination_mode,
    )
    with _worker_lock:
        if _worker_thread is not None and _worker_thread.is_alive():
            return False
        _worker_thread = Thread(
            target=_run_background_backup,
            args=(request,),
            name="BlenderAutoBackupWorker",
            daemon=True,
        )
        _worker_thread.start()
    ensure_timer(first_interval=1.0)
    return True


def is_background_backup_running() -> bool:
    with _worker_lock:
        return _worker_thread is not None and _worker_thread.is_alive()


def _interval_seconds(settings) -> int:
    return max(60, int(settings.interval_minutes) * 60)


def _format_datetime(value: datetime) -> str:
    return value.strftime("%Y-%m-%d %H:%M:%S")


def _run_background_backup(request: BackupJobRequest) -> None:
    global _worker_thread
    try:
        result = run_backup(
            source_directory=request.source_directory,
            backup_directory=request.backup_directory,
            max_backups=request.max_backups,
            project_label=request.project_label,
            include_globs=request.include_globs,
            exclude_globs=request.exclude_globs,
            destination_mode=request.destination_mode,
        )
        outcome = BackupJobOutcome(status="passed", result=result, finished_at=datetime.now())
    except BackupError as exc:
        outcome = BackupJobOutcome(status="failed", error=str(exc), finished_at=datetime.now())
    except Exception as exc:  # Keep the Blender timer alive after unexpected failures.
        outcome = BackupJobOutcome(
            status="unexpected_error",
            error=str(exc),
            finished_at=datetime.now(),
        )
    _finished_jobs.put(outcome)
    with _worker_lock:
        _worker_thread = None


def _apply_finished_jobs(settings) -> bool:
    applied = False
    while True:
        try:
            outcome = _finished_jobs.get_nowait()
        except Empty:
            break
        applied = True
        settings.last_run_at = _format_datetime(outcome.finished_at)
        if outcome.status == "passed" and outcome.result is not None:
            settings.last_backup_path = str(outcome.result.archive_path)
            settings.last_status = (
                f"OK: {outcome.result.file_count} files, {outcome.result.byte_count} bytes -> "
                f"{outcome.result.archive_path.name}"
            )
        elif outcome.status == "failed":
            settings.last_status = f"Error: {outcome.error}"
        else:
            settings.last_status = f"Unexpected error: {outcome.error}"
    return applied


def _timer_tick():
    global _in_progress, _next_due_monotonic
    scene = getattr(bpy.context, "scene", None)
    settings = getattr(scene, "blender_auto_backup", None) if scene else None
    if settings is not None:
        _apply_finished_jobs(settings)

    if not _timer_enabled:
        return None

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

    if is_background_backup_running():
        return 5.0

    if _in_progress:
        return 5.0

    _in_progress = True
    try:
        from .operators import perform_backup_for_settings, start_background_backup_for_settings

        if settings.use_background_worker:
            started, _message = start_background_backup_for_settings(settings)
            if not started:
                return 5.0
        else:
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
