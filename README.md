# StudioOS-CEAL

**CEAL = Controlled Engineering & Audit Lifecycle**

StudioOS-CEAL 是项目无关的受控工程与独立审计框架。任何 Codex、Luna 或其他工程 Agent 的修改，都被视为一笔可追踪、可验证、可回滚、必须由独立证据才能关闭的工程事务。

## 当前真实状态

本仓库现在同时包含两层，必须区分：

1. **CEAL v1.0 Bootstrap Governance**：Constitution、Task Contract、Policy、Evidence、Independent Audit 等 canonical 治理合同。
2. **Assurance Runtime 0.2.0**：无第三方运行依赖的 Python 策略模型、CLI、合同封装校验、证据 manifest 校验和 8000+ 确定性对抗矩阵。

尚未完成的 v1 Kernel Transaction Manager：

`ceal init / start / status / verify / package / audit-import / close`

因此不能把本仓库称为完整 CEAL v1 Kernel，也不能据此声称 StudioOS、ComfyUI、GPU、模型或任何生产 Runtime READY。

## Canonical 对象

- Project Profile
- Task Contract
- Execution Transaction
- Capability Lease
- Baseline / Source Identity
- Evidence Plan
- Review Artifact
- Audit Verdict

`Task Package` 是运行封装，必须绑定 frozen Task Contract / Policy / Baseline，不能扩大 canonical 授权。

## 当前 Assurance Runtime

```bash
PYTHONPATH=src python -m studioos_ceal validate-task templates/TASK_PACKAGE.example.json
PYTHONPATH=src python -m studioos_ceal run --output-dir evidence --keep-matrix
PYTHONPATH=src python -m studioos_ceal verify-manifest evidence/manifest.json
```

当前定义空间：10 phases × 14 mutations × 10 evidence states × 8 pressures = **11,200** unique scenarios；三轮共 33,600 场景调用、201,600 次 Gate 评估。阶段维度参与证据要求决策，不再只是机械乘数；除逐场景 oracle 外，还有不依赖逐项 expected 的全矩阵不变量测试。

这里的“稳定”只证明当前定义策略空间与当前实现一致，并不证明未建模风险不存在。

## 两套 Gate 的关系

治理层八道事务 Gate：`G0 Contract → G1 Authorization → G2 Plan → G3 Change/Scope → G4 Verification → G5 Runtime/Side-effect → G6 Artifact Integrity → G7 Independent Audit`。

Assurance Runtime 六个策略检查器：`Contract / Scope / Risk / Execution / Evidence / Closure`。六检查器是测试/建模工具，不替代八道事务生命周期 Gate。

## 安全边界

默认 fail-closed：Scope/denylist 逃逸、Policy/Task Contract drift、Secret/付费/生产写入/破坏性动作、修改自己的审计规则、untracked changeset omission、stale/mock/contradictory evidence、artifact hash 或 source identity 不一致。

低等级证据不能冒充高等级验收；`AUDIT_APPROVED != RELEASE_APPROVED`。main 分支保护、数字签名、OS sandbox、Secret 托管等仍属于外部平台控制面，不能由本仓库代码自行宣称完成。
