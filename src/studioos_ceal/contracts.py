from __future__ import annotations

from fnmatch import fnmatchcase
from pathlib import PurePosixPath
from typing import Any


class ContractError(ValueError):
    pass


REQUIRED_TOP_LEVEL = {
    "schema_version",
    "task_id",
    "title",
    "mode",
    "status",
    "risk_level",
    "scope",
    "acceptance",
    "rollback",
    "stop_conditions",
}

ALLOWED_MODES = {"answer", "diagnose", "implement_and_verify", "read_only_audit"}
ALLOWED_STATUSES = {
    "DRAFT",
    "APPROVED_FOR_PREPARATION",
    "APPROVED_FOR_IMPLEMENTATION",
    "IMPLEMENTING",
    "BLOCKED",
    "CODE_COMPLETE",
    "TEST_PASS",
    "RUNTIME_VERIFIED",
    "CLOSED",
}
ALLOWED_RISK_LEVELS = {"L0", "L1", "L2", "L3"}


def _nonempty_string(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def _normalise_path(value: str) -> str:
    candidate = value.replace("\\", "/")
    raw_parts = PurePosixPath(candidate).parts
    if (
        candidate.startswith("/")
        or any(part == ".." for part in raw_parts)
        or (raw_parts and raw_parts[0].endswith(":"))
    ):
        raise ContractError(f"unsafe repository path: {value}")
    while candidate.startswith("./"):
        candidate = candidate[2:]
    path = PurePosixPath(candidate)
    if not candidate or candidate == "." or path.is_absolute():
        raise ContractError(f"unsafe repository path: {value}")
    return path.as_posix()


def _matches(path: str, patterns: list[str]) -> bool:
    return any(fnmatchcase(path, pattern) or PurePosixPath(path).match(pattern) for pattern in patterns)


def validate_change_paths(package: dict[str, Any], changed_paths: list[str]) -> list[str]:
    scope = package["scope"]
    allow = [_normalise_path(item) for item in scope["allow"]]
    deny = [_normalise_path(item) for item in scope["deny"]]
    errors: list[str] = []
    for raw_path in changed_paths:
        path = _normalise_path(raw_path)
        if _matches(path, deny):
            errors.append(f"{path}: denied")
        elif not _matches(path, allow):
            errors.append(f"{path}: outside allowlist")
    return errors


def validate_task_package(package: dict[str, Any]) -> None:
    missing = sorted(REQUIRED_TOP_LEVEL - package.keys())
    if missing:
        raise ContractError(f"missing required fields: {', '.join(missing)}")

    for field in ("schema_version", "task_id", "title"):
        if not _nonempty_string(package[field]):
            raise ContractError(f"{field} must be a non-empty string")

    if package["mode"] not in ALLOWED_MODES:
        raise ContractError(f"unsupported mode: {package['mode']}")
    if package["status"] not in ALLOWED_STATUSES:
        raise ContractError(f"unsupported status: {package['status']}")
    if package["risk_level"] not in ALLOWED_RISK_LEVELS:
        raise ContractError(f"unsupported risk_level: {package['risk_level']}")

    scope = package["scope"]
    if not isinstance(scope, dict):
        raise ContractError("scope must be an object")
    for key in ("allow", "deny"):
        values = scope.get(key)
        if not isinstance(values, list) or not all(_nonempty_string(item) for item in values):
            raise ContractError(f"scope.{key} must be a list of non-empty strings")
    if not scope["allow"]:
        raise ContractError("scope.allow must not be empty")

    acceptance = package["acceptance"]
    if not isinstance(acceptance, dict):
        raise ContractError("acceptance must be an object")
    required_commands = acceptance.get("required_commands")
    if not isinstance(required_commands, list) or not all(
        _nonempty_string(item) for item in required_commands
    ):
        raise ContractError("acceptance.required_commands must be a string list")

    rollback = package["rollback"]
    if not isinstance(rollback, dict) or not _nonempty_string(rollback.get("strategy")):
        raise ContractError("rollback.strategy must be a non-empty string")

    stops = package["stop_conditions"]
    if not isinstance(stops, list) or not stops or not all(_nonempty_string(item) for item in stops):
        raise ContractError("stop_conditions must be a non-empty string list")

    changed_paths = package.get("changed_paths", [])
    if not isinstance(changed_paths, list) or not all(_nonempty_string(item) for item in changed_paths):
        raise ContractError("changed_paths must be a string list")
    path_errors = validate_change_paths(package, changed_paths)
    if path_errors:
        raise ContractError("; ".join(path_errors))
