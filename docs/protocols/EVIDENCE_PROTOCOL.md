# Evidence Protocol

每条关键 Evidence 应绑定：
- evidence_id
- transaction_id
- source_tree_hash / commit
- evidence_level
- generated_at
- producer
- requirement / claim references

任务执行前生成并冻结 Required Evidence Plan。

Claim 形成：
`Requirement → Claim → Test → Raw Evidence → Source Tree`

源码变化后旧证据标记 `STALE_EVIDENCE`。

P0 / 高风险能力必须包含 negative / counterexample test。
