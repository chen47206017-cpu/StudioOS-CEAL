from __future__ import annotations

from dataclasses import asdict, dataclass
from enum import IntEnum, StrEnum
from typing import Any


class Decision(StrEnum):
    ALLOW = "ALLOW"
    HOLD = "HOLD"
    ESCALATE = "ESCALATE"
    BLOCK = "BLOCK"


class Severity(IntEnum):
    P3 = 0
    P2 = 1
    P1 = 2
    P0 = 3

    @property
    def label(self) -> str:
        return self.name


DECISION_PRECEDENCE = {
    Decision.ALLOW: 0,
    Decision.HOLD: 1,
    Decision.ESCALATE: 2,
    Decision.BLOCK: 3,
}


@dataclass(frozen=True, slots=True)
class Scenario:
    scenario_id: str
    phase: str
    mutation: str
    evidence: str
    pressure: str
    expected_decision: Decision

    def as_dict(self) -> dict[str, Any]:
        data = asdict(self)
        data["expected_decision"] = self.expected_decision.value
        return data


@dataclass(frozen=True, slots=True)
class GateResult:
    gate: str
    decision: Decision
    severity: Severity
    reason_code: str
    detail: str

    @property
    def finding_family(self) -> str:
        return f"{self.gate}:{self.reason_code}:{self.decision.value}:{self.severity.label}"

    def as_dict(self) -> dict[str, Any]:
        data = asdict(self)
        data["decision"] = self.decision.value
        data["severity"] = self.severity.label
        return data


@dataclass(frozen=True, slots=True)
class Evaluation:
    scenario: Scenario
    decision: Decision
    gate_results: tuple[GateResult, ...]

    @property
    def high_priority_families(self) -> frozenset[str]:
        return frozenset(
            result.finding_family
            for result in self.gate_results
            if result.severity >= Severity.P1 and result.decision is not Decision.ALLOW
        )

    def as_dict(self) -> dict[str, Any]:
        return {
            "scenario": self.scenario.as_dict(),
            "decision": self.decision.value,
            "gate_results": [result.as_dict() for result in self.gate_results],
        }


def strongest_decision(results: tuple[GateResult, ...]) -> Decision:
    return max(
        (result.decision for result in results),
        key=DECISION_PRECEDENCE.__getitem__,
        default=Decision.ALLOW,
    )
