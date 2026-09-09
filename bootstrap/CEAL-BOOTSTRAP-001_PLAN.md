# CEAL-BOOTSTRAP-001

目标：把 StudioOS-CEAL 从治理设计基线升级为可运行 CEAL v1.0 Kernel。

## 已完成的 bootstrap / assurance 基础

- Constitution / Task Contract / Policy / Evidence / Audit schema
- project-agnostic Assurance Runtime 0.2.0
- deterministic 8000+ policy model and manifest verification

## v1 Kernel 仍必做

- ceal init/start/status/verify/package/audit-import/close
- persistent Transaction / Plan Gate / Capability Lease
- Baseline 与 complete filesystem/git changeset discovery
- Evidence Plan / Requirement Trace / Claim Trace
- Review Artifact / Audit Verdict / Close Gate

## 暂不做

OPA / Sigstore / SLSA Attestation / OpenTelemetry backend / Multi-Agent / Web UI / Kubernetes / 强制 SBOM。

CEAL 自己的后续开发也必须走 baseline → implement → verify → package → independent audit。
