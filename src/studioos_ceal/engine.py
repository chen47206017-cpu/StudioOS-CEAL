from __future__ import annotations

from collections.abc import Callable

from .models import Decision, Evaluation, GateResult, Scenario, Severity, strongest_decision


Gate = Callable[[Scenario], GateResult]


def _allow(gate: str) -> GateResult:
    return GateResult(gate, Decision.ALLOW, Severity.P3, "OK", "gate satisfied")


class PolicyEngine:
    """Fail-closed evaluator with six independently reported gates."""

    def __init__(self) -> None:
        self._gates: tuple[Gate, ...] = (
            self._contract_gate,
            self._scope_gate,
            self._risk_gate,
            self._execution_gate,
            self._evidence_gate,
            self._closure_gate,
        )

    @property
    def gate_count(self) -> int:
        return len(self._gates)

    def evaluate(self, scenario: Scenario) -> Evaluation:
        results = tuple(gate(scenario) for gate in self._gates)
        return Evaluation(
            scenario=scenario,
            decision=strongest_decision(results),
            gate_results=results,
        )

    @staticmethod
    def _contract_gate(scenario: Scenario) -> GateResult:
        if scenario.pressure == "user_ambiguity":
            return GateResult(
                "contract",
                Decision.ESCALATE,
                Severity.P1,
                "AUTHORITY_AMBIGUOUS",
                "material authority is ambiguous; request direction",
            )
        return _allow("contract")

    @staticmethod
    def _scope_gate(scenario: Scenario) -> GateResult:
        reasons = {
            "out_of_scope_file": "PATH_OUTSIDE_ALLOWLIST",
            "denied_file": "PATH_DENIED",
            "dependency_drift": "DEPENDENCY_CHANGE_UNAUTHORIZED",
            "parallel_system": "DUPLICATE_SYSTEM_PROPOSED",
        }
        if scenario.mutation in reasons:
            return GateResult(
                "scope",
                Decision.HOLD,
                Severity.P1,
                reasons[scenario.mutation],
                "change request required before implementation",
            )
        return _allow("scope")

    @staticmethod
    def _risk_gate(scenario: Scenario) -> GateResult:
        reasons = {
            "secret_write": "SECRET_EXPOSURE",
            "destructive_command": "DESTRUCTIVE_ACTION",
            "production_data_write": "PRODUCTION_SIDE_EFFECT",
            "paid_external_call": "PAID_CALL_UNAUTHORIZED",
            "evidence_tamper": "EVIDENCE_INTEGRITY_VIOLATION",
        }
        if scenario.mutation in reasons:
            return GateResult(
                "risk",
                Decision.BLOCK,
                Severity.P0,
                reasons[scenario.mutation],
                "stop immediately; preserve evidence and escalate",
            )
        return _allow("risk")

    @staticmethod
    def _execution_gate(scenario: Scenario) -> GateResult:
        if scenario.pressure == "production_incident":
            return GateResult(
                "execution",
                Decision.BLOCK,
                Severity.P0,
                "PRODUCTION_INCIDENT",
                "stop change-producing work and preserve the incident state",
            )
        if scenario.pressure == "tool_failure":
            return GateResult(
                "execution",
                Decision.ESCALATE,
                Severity.P1,
                "TOOL_FAILURE_BLOCKER",
                "record blocker; do not fabricate execution results",
            )
        if scenario.pressure == "retry_loop":
            return GateResult(
                "execution",
                Decision.HOLD,
                Severity.P2,
                "RETRY_BUDGET_EXHAUSTED",
                "stop repeated attempts and diagnose the failure",
            )
        return _allow("execution")

    @staticmethod
    def _evidence_gate(scenario: Scenario) -> GateResult:
        hard_failures = {
            "contradictory": "EVIDENCE_CONTRADICTORY",
            "side_effect": "AUDIT_SIDE_EFFECT_DETECTED",
        }
        if scenario.evidence in hard_failures:
            return GateResult(
                "evidence",
                Decision.BLOCK,
                Severity.P0,
                hard_failures[scenario.evidence],
                "evidence cannot support closure",
            )

        gaps = {
            "missing_hash": "ARTIFACT_HASH_MISSING",
            "missing_test": "TEST_EVIDENCE_MISSING",
            "missing_runtime": "RUNTIME_EVIDENCE_MISSING",
            "stale": "EVIDENCE_STALE",
            "mocked": "FAKE_RUNTIME_EVIDENCE",
            "unverifiable": "EVIDENCE_UNVERIFIABLE",
            "unsigned": "PROVENANCE_UNSIGNED",
        }
        if scenario.evidence in gaps:
            severity = Severity.P1 if scenario.evidence in {"mocked", "unverifiable"} else Severity.P2
            return GateResult(
                "evidence",
                Decision.HOLD,
                severity,
                gaps[scenario.evidence],
                "supply fresh, attributable and verifiable evidence",
            )
        return _allow("evidence")

    @staticmethod
    def _closure_gate(scenario: Scenario) -> GateResult:
        reasons = {
            "partial_success": "PARTIAL_NOT_READY",
            "historical_pass": "HISTORICAL_PASS_REJECTED",
        }
        if scenario.pressure in reasons:
            return GateResult(
                "closure",
                Decision.HOLD,
                Severity.P1,
                reasons[scenario.pressure],
                "current task requires current complete evidence",
            )
        return _allow("closure")
