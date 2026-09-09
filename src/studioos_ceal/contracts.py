from __future__ import annotations

import re
from fnmatch import fnmatchcase
from pathlib import PurePosixPath
from typing import Any


class ContractError(ValueError):
    pass


REQUIRED_TOP_LEVEL = {"schema_version","task_id","transaction_id","task_contract_sha256","policy_sha256","baseline_id","title","mode","status","risk_level","scope","acceptance","rollback","stop_conditions","capabilities","side_effect_permissions","external_side_effects","changeset_source","changeset_complete","changed_paths"}
ALLOWED_TOP_LEVEL = REQUIRED_TOP_LEVEL
ALLOWED_MODES = {"answer", "diagnose", "implement_and_verify", "read_only_audit"}
ALLOWED_STATUSES = {"DRAFT","APPROVED_FOR_PREPARATION","APPROVED_FOR_IMPLEMENTATION","IMPLEMENTING","BLOCKED","CODE_COMPLETE","TEST_PASS","RUNTIME_VERIFIED","AUDIT_PENDING","AUDIT_APPROVED","REPAIR_REQUIRED","RELEASE_APPROVED","CLOSED"}
ALLOWED_RISK_LEVELS = {"L0", "L1", "L2", "L3", "L4"}
ALLOWED_CHANGESET_SOURCES = {"DECLARED", "DISCOVERED_GIT"}
CLOSURE_STATUSES = {"CODE_COMPLETE","TEST_PASS","RUNTIME_VERIFIED","AUDIT_PENDING","AUDIT_APPROVED","RELEASE_APPROVED","CLOSED"}
_SHA256_RE = re.compile(r"^[0-9a-fA-F]{64}$")


def _nonempty_string(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def _string_list(value: Any, *, allow_empty: bool = True) -> bool:
    return isinstance(value, list) and (allow_empty or bool(value)) and all(_nonempty_string(item) for item in value)


def _normalise_path(value: str) -> str:
    candidate = value.replace("\\", "/")
    raw_parts = PurePosixPath(candidate).parts
    if candidate.startswith("/") or any(part == ".." for part in raw_parts) or (raw_parts and raw_parts[0].endswith(":")):
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
        if _matches(path, deny): errors.append(f"{path}: denied")
        elif not _matches(path, allow): errors.append(f"{path}: outside allowlist")
    return errors


def validate_task_package(package: dict[str, Any]) -> None:
    if not isinstance(package, dict): raise ContractError("task package must be an object")
    missing = sorted(REQUIRED_TOP_LEVEL - package.keys())
    if missing: raise ContractError(f"missing required fields: {', '.join(missing)}")
    extras = sorted(package.keys() - ALLOWED_TOP_LEVEL)
    if extras: raise ContractError(f"unexpected fields: {', '.join(extras)}")
    for field in ("schema_version","task_id","transaction_id","baseline_id","title"):
        if not _nonempty_string(package[field]): raise ContractError(f"{field} must be a non-empty string")
    for field in ("task_contract_sha256","policy_sha256"):
        if not isinstance(package[field], str) or not _SHA256_RE.fullmatch(package[field]): raise ContractError(f"{field} must be a 64-hex SHA-256")
    if package["mode"] not in ALLOWED_MODES: raise ContractError(f"unsupported mode: {package['mode']}")
    if package["status"] not in ALLOWED_STATUSES: raise ContractError(f"unsupported status: {package['status']}")
    if package["risk_level"] not in ALLOWED_RISK_LEVELS: raise ContractError(f"unsupported risk_level: {package['risk_level']}")
    scope = package["scope"]
    if not isinstance(scope, dict) or set(scope) != {"allow","deny"}: raise ContractError("scope must contain only allow and deny")
    if not _string_list(scope["allow"], allow_empty=False): raise ContractError("scope.allow must be a non-empty string list")
    if not _string_list(scope["deny"]): raise ContractError("scope.deny must be a string list")
    acceptance = package["acceptance"]
    if not isinstance(acceptance, dict) or set(acceptance) != {"required_commands","runtime_evidence_required","production_evidence_required"}: raise ContractError("acceptance has unexpected or missing fields")
    if not _string_list(acceptance["required_commands"]): raise ContractError("acceptance.required_commands must be a string list")
    for field in ("runtime_evidence_required","production_evidence_required"):
        if not isinstance(acceptance[field], bool): raise ContractError(f"acceptance.{field} must be boolean")
    rollback = package["rollback"]
    if not isinstance(rollback, dict) or set(rollback) != {"strategy"} or not _nonempty_string(rollback["strategy"]): raise ContractError("rollback must contain a non-empty strategy")
    if not _string_list(package["stop_conditions"], allow_empty=False): raise ContractError("stop_conditions must be a non-empty string list")
    if not _string_list(package["capabilities"]): raise ContractError("capabilities must be a string list")
    if not _string_list(package["side_effect_permissions"]): raise ContractError("side_effect_permissions must be a string list")
    if not isinstance(package["external_side_effects"], bool): raise ContractError("external_side_effects must be boolean")
    if package["changeset_source"] not in ALLOWED_CHANGESET_SOURCES: raise ContractError(f"unsupported changeset_source: {package['changeset_source']}")
    if not isinstance(package["changeset_complete"], bool): raise ContractError("changeset_complete must be boolean")
    if package["status"] in CLOSURE_STATUSES and not package["changeset_complete"]: raise ContractError("closure-level status requires changeset_complete=true")
    if package["changeset_complete"] and package["changeset_source"] != "DISCOVERED_GIT": raise ContractError("complete changeset must use changeset_source=DISCOVERED_GIT")
    changed_paths = package["changed_paths"]
    if not _string_list(changed_paths): raise ContractError("changed_paths must be a string list")
    path_errors = validate_change_paths(package, changed_paths)
    if path_errors: raise ContractError("; ".join(path_errors))
