# CEAL Architecture

CEAL 不是超长 Prompt 模板，而是 **Agent Engineering Transaction Manager**。

```text
Human Intent
  ↓
Task Compiler
  ↓
Task Contract + Context + Risk
  ↓
Plan Gate
  ↓
Capability Lease
  ↓
Implementation Agent
  ↓
Execution Guard
  ↓
Evidence Broker
  ↓
Review Artifact
  ↓
Independent Audit
  ↓
Approved / Repair Required
```

## 八道 Gate
G0 Task Contract
G1 Authorization
G2 Plan
G3 Change / Scope
G4 Verification
G5 Runtime / Side Effect
G6 Artifact Integrity
G7 Independent Audit

## 六个通用 Primitive
Intent / Resource / Capability / Change / Evidence / Approval
