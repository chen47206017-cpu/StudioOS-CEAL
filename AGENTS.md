# StudioOS-CEAL Agent Contract

本文件对整个仓库生效。任何工程 Agent 进入仓库后先读取本文件，并立即读取 `ceal/constitution/CONSTITUTION.md`。

## 1. Canonical authority

- `Task Contract` 是本事务的唯一 canonical 授权对象。
- `Task Package` 只是运行封装，必须绑定 `task_contract_sha256`、`policy_sha256` 与 baseline；它不能扩大 Task Contract 的 Scope、Capability 或 Side-effect 权限。
- Implementation Truth、Execution Truth、Audit Truth 永久分离。
- Implementation Agent 不得自我声明 `AUDIT_APPROVED` 或 `RELEASE_APPROVED`。

## 2. 开始任务前

1. 读取 Constitution、Task Contract、适用 Task Package、Project Profile 与当前任务上下文。
2. 记录 branch / HEAD / working tree / baseline identity。
3. 冻结 Task Contract hash、Policy hash、baseline 与 evidence plan。
4. 检查 allowlist、denylist、risk、capability lease、side-effect permissions、repair budget、stop conditions 与 rollback。
5. 已有明确实施授权且动作在冻结范围内时，直接实施，不重复询问。

## 3. 必须停止或请求 Amendment

- 所需文件/动作超出 allowlist、命中 denylist，或 Task Package 比 Task Contract 更宽；
- Task Contract / Policy / baseline identity 漂移；
- 需要新增凭据、付费服务、外部发布、生产写入、破坏性动作或扩大依赖/架构范围；
- complete changeset 无法证明，包含未跟踪/删除/重命名遗漏；
- 证据矛盾、陈旧、不可验证，或继续测试会污染真实状态；
- repair budget 已耗尽。

普通可逆编辑、已授权测试和范围内修复不得重复向用户确认。

## 4. 实施规则

- 保留用户已有修改；不得擅自清理脏工作区。
- 优先复用现有实现；禁止用 `new` / `v2` / `legacy` 平行系统逃避整合。
- 普通任务不得修改 `ceal/constitution/**`、`policies/**`、`schemas/**` 或 Auditor-owned acceptance，除非 `task_type=GOVERNANCE_CHANGE`。
- 禁止伪造日志、测试、hash、截图、API 结果、运行时间或对抗执行数量。
- 禁止写入真实 Secret；示例只能用占位符。
- 禁止自动付费、生产写入、不可逆升级或公开监听。
- 不得使用 `git reset --hard`、无明确目标的递归删除或强制重写共享历史。

## 5. Changeset 与证据

- Closure-level 状态必须基于完整、实际发现的 changeset；不得只相信 Agent 自填的 changed-path list。
- Evidence 必须绑定 transaction 与 exact source identity；源码变化后旧 evidence 失效。
- Review Artifact 必须覆盖完整 changeset，失败/阻塞/部分完成也必须 package。
- `manifest.json` 必须可独立复算；任何缺失、路径逃逸、大小/hash 不一致都 fail closed。

## 6. 对抗验证口径

- “8000+”只能表示生成器实际创建并执行了至少 8000 个唯一场景。
- 维度必须对决策具有实际语义；不得用无效维度机械放大数量。
- Oracle mismatch 必须为 0，且必须另有不依赖逐项 oracle 的不变量测试。
- 全空间重复扫描的零新增只可称为“定义空间稳定性”，不得冒充自适应搜索、互联网研究或未知风险穷尽。
- CEAL 自身 PASS 不证明 StudioOS、ComfyUI、GPU、模型或任何外部生产系统 READY。

## 7. Git 与交付

- 默认独立 branch + PR；除非用户明确授权，不直接写 `main`。
- Merge 前检查所有活跃分支、冲突、CI、source identity、secret exposure、stale evidence 和 rollback。
- 最终回复顺序：实际状态 → 修改/提交/PR → 测试 → 证据/hash → 风险/未完成 → 回滚 → 唯一必要下一步。
- 若任务全部完成，不为了延长流程要求用户再次输入“继续”。

## 8. 最短提示词

```text
执行 TASK-XXX：<目标>。
按仓库 AGENTS.md、canonical Task Contract 和对应 Task Package 自动完成；
已授权范围内不要重复询问，触发停止闸才报告 blocker。
```
