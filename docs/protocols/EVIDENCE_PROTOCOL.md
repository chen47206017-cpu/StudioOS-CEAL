# Evidence Protocol

每条关键 Evidence 应绑定：

- evidence_id
- transaction_id
- exact source_tree_hash / commit
- evidence_level
- generated_at
- producer
- requirement / claim references

任务执行前生成并冻结 Required Evidence Plan。

Claim 链：

`Requirement → Claim → Test → Raw Evidence → Source Identity`

源码变化后旧证据必须标记 `STALE_EVIDENCE`。

P0 / 高风险能力必须包含 negative / counterexample test。

## 8000+ Matrix evidence

- 场景必须唯一并实际调用被测策略。
- 维度必须至少在部分上下文中改变可观察决策；语义无效维度不能拿来扩大 coverage 数字。
- 必须记录 matrix digest、actual invocation count、oracle mismatches 和独立不变量测试。
- 重复全空间扫描零新增只可作为稳定性证据，不得称为未知风险已穷尽。
- 审计模式应保留 raw matrix，并由 `manifest.json` 绑定大小和 SHA-256。
