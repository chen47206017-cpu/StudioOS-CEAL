# CEAL Architecture

CEAL 不是超长 Prompt 模板，而是 **Agent Engineering Transaction Manager + Assurance Model**。

## Canonical transaction path

```text
Human Intent
  ↓
Task Contract (canonical authority)
  ↓
Task Package (bound execution envelope; cannot broaden authority)
  ↓
Baseline + Policy Hash + Source Identity
  ↓
Plan Gate + Capability Lease
  ↓
Implementation Agent
  ↓
Execution Guard
  ↓
Verification + Evidence Broker
  ↓
Review Artifact
  ↓
Independent Audit
  ↓
Approved / Repair Required
  ↓
Release decision (separate)
```

## 八道事务 Gate

G0 Task Contract  
G1 Authorization  
G2 Plan  
G3 Change / Scope  
G4 Verification  
G5 Runtime / Side Effect  
G6 Artifact Integrity  
G7 Independent Audit

## 六个 Assurance Runtime 检查器

`Contract / Scope / Risk / Execution / Evidence / Closure`

它们用于对抗模型与回归验证，不等于完整事务执行器。当前 Python 0.2.0 runtime 能验证任务封装、路径/风险决策、确定性矩阵和证据 manifest；尚未实现 `init/start/status/package/audit-import/close` 的完整持久化 Transaction Manager。

## 信任边界

- 仓库源码、测试、生成报告：CEAL 自身验证范围。
- GitHub Actions、分支保护、签名：外部控制面，必须读取真实平台状态。
- StudioOS、ComfyUI、GPU、模型/API、生产数据：外部产品面，必须由独立产品 Task Contract 与运行证据证明。
