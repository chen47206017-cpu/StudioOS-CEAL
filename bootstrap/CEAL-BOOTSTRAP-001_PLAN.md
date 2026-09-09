# CEAL-BOOTSTRAP-001

目标：把 StudioOS-CEAL 从设计基线升级为可运行 CEAL v1.0 Kernel。

## 必做
- ceal init/start/status/verify/package/audit-import/close
- Project Profile
- Task Contract
- Plan Gate
- Risk / Capability Boundary
- Baseline
- Complete changeset detection（含 untracked）
- Evidence Plan
- Requirement / Claim Trace
- Review Artifact
- Audit Verdict
- Close Gate

## 暂不做
OPA / Sigstore / SLSA Attestation / OpenTelemetry backend / Multi-Agent / Web UI / Kubernetes / 强制 SBOM。

CEAL 自己第一次开发也必须：baseline → 实施 → verify → 无论成功失败都打 Review ZIP → STOP → GPT-5.6 Sol 独立审计。
