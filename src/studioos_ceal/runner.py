from __future__ import annotations

import hashlib
import json
import os
from collections import Counter
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from .engine import PolicyEngine
from .matrix import MATRIX_SIZE, generate_scenarios
from .models import Decision, Scenario


def _canonical_json(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def _atomic_write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(content, encoding="utf-8", newline="\n")
    os.replace(temporary, path)


def write_matrix(path: Path, scenarios: list[Scenario]) -> str:
    body = "\n".join(_canonical_json(scenario.as_dict()) for scenario in scenarios) + "\n"
    _atomic_write(path, body)
    return hashlib.sha256(body.encode("utf-8")).hexdigest()


def load_matrix(path: Path) -> list[Scenario]:
    scenarios: list[Scenario] = []
    for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        if not line.strip():
            continue
        try:
            raw = json.loads(line)
            scenarios.append(
                Scenario(
                    scenario_id=raw["scenario_id"],
                    phase=raw["phase"],
                    mutation=raw["mutation"],
                    evidence=raw["evidence"],
                    pressure=raw["pressure"],
                    expected_decision=Decision(raw["expected_decision"]),
                )
            )
        except (KeyError, TypeError, json.JSONDecodeError) as exc:
            raise ValueError(f"invalid matrix row {line_number}: {exc}") from exc
    return scenarios


def _orders(scenarios: list[Scenario], sweeps: int) -> list[list[Scenario]]:
    orders: list[list[Scenario]] = []
    for sweep in range(sweeps):
        mode = sweep % 3
        if mode == 0:
            orders.append(list(scenarios))
        elif mode == 1:
            orders.append(list(reversed(scenarios)))
        else:
            orders.append(
                sorted(
                    scenarios,
                    key=lambda item: hashlib.sha256(
                        f"{sweep}:{item.scenario_id}".encode("utf-8")
                    ).digest(),
                )
            )
    return orders


def run_assurance(
    scenarios: list[Scenario] | None = None,
    *,
    sweeps: int = 3,
    generated_at: str | None = None,
) -> dict[str, Any]:
    if sweeps < 3:
        raise ValueError("at least three sweeps are required for convergence evidence")
    scenarios = scenarios or generate_scenarios()
    if len(scenarios) != MATRIX_SIZE:
        raise ValueError(f"full assurance run requires exactly {MATRIX_SIZE} scenarios")

    ids = [scenario.scenario_id for scenario in scenarios]
    combinations = [
        (scenario.phase, scenario.mutation, scenario.evidence, scenario.pressure)
        for scenario in scenarios
    ]
    if len(set(ids)) != MATRIX_SIZE or len(set(combinations)) != MATRIX_SIZE:
        raise ValueError("scenario matrix contains duplicate identifiers or combinations")

    engine = PolicyEngine()
    known_high_priority_families: set[str] = set()
    sweep_reports: list[dict[str, Any]] = []
    mismatches: list[dict[str, str]] = []
    decision_counts: Counter[str] = Counter()

    for sweep_number, ordered in enumerate(_orders(scenarios, sweeps), start=1):
        new_families: set[str] = set()
        sweep_counts: Counter[str] = Counter()
        for scenario in ordered:
            evaluation = engine.evaluate(scenario)
            sweep_counts[evaluation.decision.value] += 1
            if sweep_number == 1:
                decision_counts[evaluation.decision.value] += 1
                if evaluation.decision != scenario.expected_decision:
                    mismatches.append(
                        {
                            "scenario_id": scenario.scenario_id,
                            "expected": scenario.expected_decision.value,
                            "actual": evaluation.decision.value,
                        }
                    )
            for family in evaluation.high_priority_families:
                if family not in known_high_priority_families:
                    new_families.add(family)
        known_high_priority_families.update(new_families)
        sweep_reports.append(
            {
                "sweep": sweep_number,
                "scenario_evaluations": len(ordered),
                "gate_evaluations": len(ordered) * engine.gate_count,
                "new_p0_p1_finding_families": len(new_families),
                "decision_counts": dict(sorted(sweep_counts.items())),
            }
        )

    converged = (
        not mismatches
        and sweep_reports[-1]["new_p0_p1_finding_families"] == 0
        and sweep_reports[-2]["new_p0_p1_finding_families"] == 0
    )
    scenario_digest = hashlib.sha256(
        "\n".join(_canonical_json(scenario.as_dict()) for scenario in scenarios).encode("utf-8")
    ).hexdigest()

    return {
        "schema_version": "1.0",
        "generated_at": generated_at or datetime.now(UTC).isoformat(),
        "status": "CONVERGED_FOR_P0_P1" if converged else "NOT_CONVERGED",
        "claim_boundary": (
            "This verifies the CEAL policy implementation and generated scenario space; "
            "it does not prove any external product runtime or production system."
        ),
        "matrix": {
            "distinct_scenarios": len(scenarios),
            "dimensions": {
                "phases": 10,
                "mutations": 10,
                "evidence_states": 10,
                "pressures": 8,
            },
            "sha256": scenario_digest,
        },
        "six_gate_checks_first_sweep": len(scenarios) * engine.gate_count,
        "total_scenario_evaluations": len(scenarios) * sweeps,
        "total_gate_evaluations": len(scenarios) * sweeps * engine.gate_count,
        "decision_counts_first_sweep": dict(sorted(decision_counts.items())),
        "oracle_mismatches": mismatches,
        "p0_p1_finding_families": sorted(known_high_priority_families),
        "sweeps": sweep_reports,
        "stop_rule": {
            "required_consecutive_zero_novelty_sweeps": 2,
            "observed_consecutive_zero_novelty_sweeps": 2 if converged else 0,
            "scope": "high-value, non-duplicate, in-scope P0/P1 policy findings",
        },
    }


def write_report(path: Path, report: dict[str, Any]) -> str:
    body = json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    _atomic_write(path, body)
    return hashlib.sha256(body.encode("utf-8")).hexdigest()


def write_manifest(path: Path, files: list[Path]) -> None:
    records = []
    for file_path in sorted(files, key=lambda item: item.as_posix()):
        content = file_path.read_bytes()
        records.append(
            {
                "path": file_path.as_posix(),
                "bytes": len(content),
                "sha256": hashlib.sha256(content).hexdigest(),
            }
        )
    _atomic_write(path, json.dumps({"files": records}, indent=2, sort_keys=True) + "\n")
