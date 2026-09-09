from __future__ import annotations

from itertools import product
from typing import Iterable

from .models import Decision, Scenario


PHASES = (
    "intake",
    "baseline",
    "contract",
    "authorization",
    "implementation",
    "unit_test",
    "integration_test",
    "runtime_verify",
    "audit",
    "closure",
)

MUTATIONS = (
    "none",
    "out_of_scope_file",
    "denied_file",
    "secret_write",
    "destructive_command",
    "production_data_write",
    "paid_external_call",
    "dependency_drift",
    "evidence_tamper",
    "parallel_system",
)

EVIDENCE_STATES = (
    "complete",
    "missing_hash",
    "missing_test",
    "missing_runtime",
    "stale",
    "mocked",
    "unverifiable",
    "contradictory",
    "side_effect",
    "unsigned",
)

PRESSURES = (
    "normal",
    "deadline",
    "retry_loop",
    "partial_success",
    "historical_pass",
    "user_ambiguity",
    "tool_failure",
    "production_incident",
)

MATRIX_SIZE = len(PHASES) * len(MUTATIONS) * len(EVIDENCE_STATES) * len(PRESSURES)


def oracle_decision(mutation: str, evidence: str, pressure: str) -> Decision:
    """Independent outcome oracle used to detect policy regressions."""
    if mutation in {
        "secret_write",
        "destructive_command",
        "production_data_write",
        "paid_external_call",
        "evidence_tamper",
    }:
        return Decision.BLOCK
    if evidence in {"contradictory", "side_effect"}:
        return Decision.BLOCK
    if pressure == "production_incident":
        return Decision.BLOCK
    if pressure in {"user_ambiguity", "tool_failure"}:
        return Decision.ESCALATE
    if mutation in {
        "out_of_scope_file",
        "denied_file",
        "dependency_drift",
        "parallel_system",
    }:
        return Decision.HOLD
    if evidence != "complete":
        return Decision.HOLD
    if pressure in {"retry_loop", "partial_success", "historical_pass"}:
        return Decision.HOLD
    return Decision.ALLOW


def generate_scenarios(limit: int = MATRIX_SIZE) -> list[Scenario]:
    if limit < 1 or limit > MATRIX_SIZE:
        raise ValueError(f"limit must be between 1 and {MATRIX_SIZE}")

    scenarios: list[Scenario] = []
    for index, (phase, mutation, evidence, pressure) in enumerate(
        product(PHASES, MUTATIONS, EVIDENCE_STATES, PRESSURES),
        start=1,
    ):
        if index > limit:
            break
        scenarios.append(
            Scenario(
                scenario_id=f"CEAL-{index:04d}",
                phase=phase,
                mutation=mutation,
                evidence=evidence,
                pressure=pressure,
                expected_decision=oracle_decision(mutation, evidence, pressure),
            )
        )
    return scenarios


def scenario_rows(scenarios: Iterable[Scenario]) -> Iterable[dict[str, str]]:
    for scenario in scenarios:
        yield scenario.as_dict()
