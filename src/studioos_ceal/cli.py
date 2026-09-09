from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from .contracts import ContractError, validate_task_package
from .matrix import MATRIX_SIZE, generate_scenarios
from .runner import run_assurance, write_manifest, write_matrix, write_report


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="ceal",
        description="Controlled Engineering Assurance Lifecycle utilities",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    validate = subparsers.add_parser("validate-task", help="validate a task package")
    validate.add_argument("path", type=Path)

    matrix = subparsers.add_parser("generate-matrix", help="write deterministic scenarios")
    matrix.add_argument("--output", type=Path, required=True)
    matrix.add_argument("--count", type=int, default=MATRIX_SIZE)

    run = subparsers.add_parser("run", help="generate and evaluate the full matrix")
    run.add_argument("--output-dir", type=Path, default=Path("evidence"))
    run.add_argument("--sweeps", type=int, default=3)
    run.add_argument(
        "--keep-matrix",
        action="store_true",
        help="retain the generated JSONL matrix; it is ignored by Git by default",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    args = _build_parser().parse_args(argv)
    try:
        if args.command == "validate-task":
            package = json.loads(args.path.read_text(encoding="utf-8"))
            validate_task_package(package)
            print(f"VALID: {package['task_id']}")
            return 0

        if args.command == "generate-matrix":
            scenarios = generate_scenarios(args.count)
            digest = write_matrix(args.output, scenarios)
            print(f"WROTE {len(scenarios)} scenarios sha256={digest}")
            return 0

        if args.command == "run":
            args.output_dir.mkdir(parents=True, exist_ok=True)
            matrix_path = args.output_dir / "adversarial-matrix.jsonl"
            report_path = args.output_dir / "adversarial-summary.json"
            manifest_path = args.output_dir / "manifest.json"
            scenarios = generate_scenarios()
            write_matrix(matrix_path, scenarios)
            report = run_assurance(scenarios, sweeps=args.sweeps)
            write_report(report_path, report)
            manifest_files = [report_path]
            if args.keep_matrix:
                manifest_files.append(matrix_path)
            else:
                matrix_path.unlink()
            write_manifest(manifest_path, manifest_files)
            print(
                f"{report['status']}: {report['matrix']['distinct_scenarios']} scenarios, "
                f"{report['total_gate_evaluations']} gate evaluations"
            )
            return 0 if report["status"] == "CONVERGED_FOR_P0_P1" else 2
    except (ContractError, OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
