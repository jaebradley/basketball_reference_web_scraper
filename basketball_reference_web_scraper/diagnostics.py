"""Retained diagnostic evidence for investigating past runs.

Every CLI invocation or library session records structured JSON events to one
JSONL journal file per run under a bounded diagnostics directory. The journal
answers "what did this run actually do?" after the process exits: which URLs
were requested, what each returned, how long it took, which operation it
belonged to, and how the run ended.

Design constraints:
- Writes never raise into the application: telemetry failure must not change
  scrape behavior or exit codes.
- Volume and retention are bounded: at most ``MAX_JOURNAL_FILES`` run files of
  at most ``MAX_JOURNAL_BYTES`` bytes each; the oldest run files are pruned.
- Only bounded, non-secret values are recorded: no response bodies, headers
  (except ``Retry-After``), cookies, or environment variables. Values are
  truncated and non-scalar arguments are reduced to their type name.

Retrieval: ``basketball-reference diagnostics`` (see cli.py) or
``read_events``/``run_summaries`` from this module.
"""

import contextlib
import datetime
import functools
import inspect
import json
import os
import platform
import sys
import threading
import traceback
import uuid
from importlib.metadata import PackageNotFoundError
from importlib.metadata import version as _importlib_version
from pathlib import Path

DEFAULT_JOURNAL_DIR = Path.home() / ".basketball_reference_web_scraper" / "diagnostics"
MAX_JOURNAL_FILES = 20
MAX_JOURNAL_BYTES = 5 * 1024 * 1024
MAX_FIELD_CHARS = 300
MAX_TRACEBACK_CHARS = 2000
DISABLE_ENV_VAR = "BASKETBALL_REFERENCE_DIAGNOSTICS"
DIR_ENV_VAR = "BASKETBALL_REFERENCE_DIAGNOSTICS_DIR"

_JOURNAL_FILE_GLOB = "*.jsonl"

_LOCK = threading.Lock()
_run = None
_STATE_LOCK = threading.Lock()


def _disabled():
    return os.environ.get(DISABLE_ENV_VAR, "").strip().lower() == "off"


def _journal_directory():
    configured = os.environ.get(DIR_ENV_VAR)
    return Path(configured) if configured else DEFAULT_JOURNAL_DIR


def package_version():
    try:
        return _importlib_version("basketball_reference_web_scraper")
    except PackageNotFoundError:
        return "unknown"
    except Exception:
        return "unknown"


def _utc_now_iso():
    return (
        datetime.datetime.now(datetime.timezone.utc)
        .isoformat(timespec="milliseconds")
        .replace("+00:00", "Z")
    )


def _parse_timestamp(value):
    text = str(value)
    if text.endswith("Z"):
        text = text[:-1] + "+00:00"
    parsed = datetime.datetime.fromisoformat(text)
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=datetime.timezone.utc)
    return parsed


def _bounded(value, limit=MAX_FIELD_CHARS):
    text = str(value)
    if len(text) > limit:
        return text[:limit] + "…[truncated]"
    return text


def _safe_value(value):
    if value is None or isinstance(value, (bool, int, float)):
        return value
    if isinstance(value, str):
        return _bounded(value)
    # Non-scalars are recorded as type names only: bounded and free of content.
    return f"<{type(value).__name__}>"


def _safe_params(mapping):
    if not isinstance(mapping, dict):
        return None
    return {str(key): _safe_value(value) for key, value in list(mapping.items())[:20]}


def _bounded_traceback(exc):
    parts = traceback.format_exception(type(exc), exc, exc.__traceback__)
    return _bounded("".join(parts).strip(), MAX_TRACEBACK_CHARS)


class _Run:
    def __init__(self, run_id, directory, path):
        self.id = run_id
        self.directory = directory
        self.path = path
        self.bytes_written = 0
        self.capped = False
        self.last_url_by_operation = {}

    def write(self, event):
        line = json.dumps(event, ensure_ascii=False, default=str) + "\n"
        encoded = len(line.encode("utf-8"))
        with _LOCK:
            if self.capped:
                return
            if self.bytes_written + encoded > MAX_JOURNAL_BYTES:
                self.capped = True
                self._append(
                    {
                        "ts": _utc_now_iso(),
                        "run_id": self.id,
                        "event": "journal_limit",
                        "message": (
                            "Journal size cap reached; later events were not retained"
                        ),
                    }
                )
                return
            self._append_raw(line, encoded)

    def _append(self, event):
        line = json.dumps(event, ensure_ascii=False, default=str) + "\n"
        self._append_raw(line, len(line.encode("utf-8")))

    def _append_raw(self, line, encoded):
        try:
            with open(self.path, "a", encoding="utf-8") as journal:
                journal.write(line)
            self.bytes_written += encoded
        except OSError:
            # Telemetry failure must never break application behavior.
            self.capped = True

    def note_url(self, operation, url):
        with _LOCK:
            self.last_url_by_operation[operation] = url

    def last_url(self, operation):
        with _LOCK:
            return self.last_url_by_operation.get(operation)


def _prune_old_runs(directory, keep):
    try:
        run_files = sorted(directory.glob(_JOURNAL_FILE_GLOB))
        excess = len(run_files) - keep
        for stale in run_files[:excess]:
            with contextlib.suppress(OSError):
                stale.unlink()
    except OSError:
        pass


def start_run():
    """Start the process-wide run journal. Safe to call repeatedly."""
    global _run
    with _STATE_LOCK:
        if _run is not None or _disabled():
            return _run
        directory = _journal_directory()
        run_id = uuid.uuid4().hex[:12]
        started_at = datetime.datetime.now(datetime.timezone.utc)
        filename = "{}Z-{}.jsonl".format(started_at.strftime("%Y%m%dT%H%M%S"), run_id)
        path = directory / filename
        try:
            directory.mkdir(parents=True, exist_ok=True)
        except OSError:
            # No writable evidence location: run without a journal.
            return None
        _prune_old_runs(directory, MAX_JOURNAL_FILES - 1)
        run = _Run(run_id, directory, path)
        _run = run
        run.write(
            {
                "ts": started_at.isoformat(timespec="milliseconds").replace(
                    "+00:00", "Z"
                ),
                "run_id": run_id,
                "event": "run_start",
                "environment": {
                    "package_version": package_version(),
                    "python": platform.python_version(),
                    "platform": platform.platform(),
                    "pid": os.getpid(),
                    "executable": _bounded(sys.executable),
                },
            }
        )
        return _run


def ensure_run():
    if _run is None:
        return start_run()
    return _run


def reset():
    """Clear process run state; re-reads configuration on the next event."""
    global _run
    with _STATE_LOCK:
        _run = None


def current_run_id():
    run = _run
    return run.id if run is not None else None


def current_journal_path():
    run = _run
    return str(run.path) if run is not None else None


def _emit(event):
    run = ensure_run()
    if run is None:
        return
    run.write(event)


class _Operation:
    """Context manager recording operation_start/operation_end evidence."""

    def __init__(self, name, params):
        self.name = name
        self.params = params
        self.started = None
        self.finished = False

    def __enter__(self):
        self.started = datetime.datetime.now(datetime.timezone.utc)
        _emit(
            {
                "ts": _utc_now_iso(),
                "run_id": current_run_id(),
                "event": "operation_start",
                "operation": self.name,
                "params": self.params,
            }
        )
        return self

    def finish(self, row_count=None):
        self.finished = True
        elapsed_ms = None
        if self.started is not None:
            elapsed_ms = round(
                (
                    datetime.datetime.now(datetime.timezone.utc) - self.started
                ).total_seconds()
                * 1000,
                2,
            )
        _emit(
            {
                "ts": _utc_now_iso(),
                "run_id": current_run_id(),
                "event": "operation_end",
                "operation": self.name,
                "outcome": "ok",
                "row_count": row_count,
                "elapsed_ms": elapsed_ms,
            }
        )

    def __exit__(self, exc_type, exc, exc_traceback):
        if self.finished or exc_type is None:
            return False
        run = _run
        _emit(
            {
                "ts": _utc_now_iso(),
                "run_id": current_run_id(),
                "event": "operation_end",
                "operation": self.name,
                "outcome": "error",
                "error": {
                    "type": exc_type.__name__ if exc_type else None,
                    "message": _bounded(str(exc)) if exc is not None else None,
                    "traceback": _bounded_traceback(exc) if exc is not None else None,
                },
                "last_url": run.last_url(self.name) if run is not None else None,
            }
        )
        return False


@contextlib.contextmanager
def operation(name, params=None):
    """Record one named operation's start and end (ok or error)."""
    with _Operation(name, _safe_params(params)) as current:
        yield current


def traced(function):
    """Decorator for client operations: records start, end, outcome, and counts.

    Scalar arguments are recorded bounded; non-scalar arguments (options
    mappings, callbacks) are recorded as type names only. Results that are
    lists (or ``{"players": [...]}`` search results) contribute a row_count.
    """

    @functools.wraps(function)
    def wrapper(*args, **kwargs):
        try:
            bound = inspect.signature(function).bind(*args, **kwargs)
            bound.apply_defaults()
            params = _safe_params(dict(bound.arguments))
        except TypeError:
            bound = None
            params = None
        contract_counter = [0]
        counts_contracts = False

        if bound is not None:
            candidate_processor = bound.arguments.get("contract_processor")
            if callable(candidate_processor):

                def count_contracts(row, _processor=candidate_processor):
                    contract_counter[0] += 1
                    return _processor(row)

                bound.arguments["contract_processor"] = count_contracts
                counts_contracts = True

        with _Operation(function.__name__, params) as current:
            if bound is not None:
                result = function(*bound.args, **bound.kwargs)
            else:
                result = function(*args, **kwargs)
            if counts_contracts:
                current.finish(row_count=contract_counter[0])
            elif isinstance(result, dict) and "players" in result:
                current.finish(row_count=len(result["players"]))
            elif isinstance(result, list):
                current.finish(row_count=len(result))
            else:
                current.finish(row_count=None)
            return result

    return wrapper


def record_http(
    operation_name,
    method,
    url,
    *,
    request_seq,
    outcome,
    status=None,
    elapsed_ms=None,
    error=None,
    params=None,
    retry_after=None,
):
    event = {
        "ts": _utc_now_iso(),
        "run_id": current_run_id(),
        "event": "http_request",
        "operation": operation_name,
        "method": method,
        "url": _bounded(url),
        "request_seq": request_seq,
        "outcome": outcome,
    }
    if status is not None:
        event["status"] = status
    if elapsed_ms is not None:
        event["elapsed_ms"] = elapsed_ms
    if error is not None:
        event["error"] = _bounded(error)
    if retry_after is not None:
        event["retry_after"] = _bounded(retry_after, 64)
    if params:
        event["params"] = _safe_params(params)
    _emit(event)
    run = _run
    if run is not None:
        run.note_url(operation_name, url)


def record_stream(
    operation_name,
    url,
    request_seq,
    *,
    outcome,
    stream_chunks,
    stream_chars,
    elapsed_ms=None,
    error=None,
):
    event = {
        "ts": _utc_now_iso(),
        "run_id": current_run_id(),
        "event": "http_stream",
        "operation": operation_name,
        "url": _bounded(url),
        "request_seq": request_seq,
        "outcome": outcome,
        "stream_chunks": stream_chunks,
        "stream_chars": stream_chars,
    }
    if elapsed_ms is not None:
        event["elapsed_ms"] = elapsed_ms
    if error is not None:
        event["error"] = _bounded(error)
    _emit(event)
    run = _run
    if run is not None:
        run.note_url(operation_name, url)


def record_error(kind, message, **details):
    """Record a terminal error into the current run, if one exists."""
    run = _run
    if run is None:
        return
    event = {
        "ts": _utc_now_iso(),
        "run_id": run.id,
        "event": "error",
        "kind": kind,
        "message": _bounded(message),
    }
    event.update(_safe_params(details) or {})
    run.write(event)


def record_run_end(exit_code):
    run = _run
    if run is None:
        return
    run.write(
        {
            "ts": _utc_now_iso(),
            "run_id": run.id,
            "event": "run_end",
            "exit_code": exit_code,
        }
    )


def journal_paths(directory=None):
    base = Path(directory) if directory else _journal_directory()
    try:
        return sorted(base.glob(_JOURNAL_FILE_GLOB), reverse=True)
    except OSError:
        return []


def read_events(
    *,
    directory=None,
    since=None,
    until=None,
    run_id=None,
    operation_name=None,
    event=None,
    kind=None,
    limit=100,
):
    """Load retained events newest-first, filtered by the given criteria."""
    since_at = _parse_timestamp(since) if since else None
    until_at = _parse_timestamp(until) if until else None
    matched = []
    for path in journal_paths(directory):
        try:
            with open(path, encoding="utf-8") as journal:
                for line in journal:
                    line = line.strip()
                    if not line:
                        continue
                    try:
                        entry = json.loads(line)
                    except json.JSONDecodeError:
                        continue  # Retain resilience to a torn final line.
                    if not _matches(
                        entry,
                        since_at,
                        until_at,
                        run_id,
                        operation_name,
                        event,
                        kind,
                    ):
                        continue
                    matched.append(entry)
        except OSError:
            continue
    matched.reverse()
    return matched[: max(0, limit)]


def _matches(entry, since_at, until_at, run_id, operation_name, event, kind):
    if event is not None and entry.get("event") != event:
        return False
    if run_id is not None and entry.get("run_id") != run_id:
        return False
    if operation_name is not None and entry.get("operation") != operation_name:
        return False
    if kind is not None and entry.get("kind") != kind:
        return False
    if since_at is not None or until_at is not None:
        try:
            entry_at = _parse_timestamp(entry.get("ts"))
        except (TypeError, ValueError):
            return False
        if since_at is not None and entry_at < since_at:
            return False
        if until_at is not None and entry_at > until_at:
            return False
    return True


def run_summaries(directory=None):
    """Summarize each retained run file: identity, span, outcome."""
    summaries = []
    for path in journal_paths(directory):
        events = []
        try:
            with open(path, encoding="utf-8") as journal:
                for line in journal:
                    line = line.strip()
                    if line:
                        with contextlib.suppress(json.JSONDecodeError):
                            events.append(json.loads(line))
        except OSError:
            continue
        if not events:
            summaries.append({"file": str(path), "events": 0})
            continue
        outcomes = [
            entry.get("outcome")
            for entry in events
            if entry.get("event") == "operation_end"
        ]
        exit_codes = [
            entry.get("exit_code")
            for entry in events
            if entry.get("event") == "run_end"
        ]
        summaries.append(
            {
                "file": str(path),
                "run_id": events[0].get("run_id"),
                "started_at": events[0].get("ts"),
                "last_event_at": events[-1].get("ts"),
                "events": len(events),
                "operation_outcomes": {
                    "ok": outcomes.count("ok"),
                    "error": outcomes.count("error"),
                },
                "exit_code": exit_codes[-1] if exit_codes else None,
                "has_error": any(entry.get("event") == "error" for entry in events),
            }
        )
    return summaries
