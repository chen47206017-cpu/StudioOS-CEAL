# StudioOS-CEAL

**CEAL = Controlled Engineering & Audit Lifecycle**

StudioOS-CEAL 是面向 Codex / Luna / 其他工程 Agent 的项目无关受控工程与独立审计框架。

核心原则：任何 Agent 对项目的修改，都不是普通“改代码任务”，而是一笔可追踪、可验证、可回滚、必须独立审计后才能关闭的受控工程事务。

## 核心对象
- Project Profile
- Task Contract
- Execution Transaction
- Capability Lease
- Evidence Plan
- Review Artifact
- Audit Verdict

## 状态
`DRAFT → AUTHORIZED → BASELINED → EXECUTING → SELF_VERIFIED → PACKAGED → AUDIT_PENDING → AUDIT_APPROVED / REPAIR_REQUIRED → CLOSED`

任何 FAILED / BLOCKED / PARTIAL / TIMEOUT 都必须进入 `PACKAGED → AUDIT_PENDING`。

## v1 Kernel 目标
`ceal init / start / status / verify / package / audit-import / close`

StudioOS 仅作为第一个 Project Adapter；CEAL Core 禁止写死 ComfyUI、8189、8190、DRFE、Seedance、GPU 等项目特定概念。
