# CEAL Constitution v1.0

1. 每个 Agent 任务必须属于一个明确 Transaction。
2. 永久区分 Implementation Truth、Execution Truth、Audit Truth。
3. Implementation Agent 不得自我批准独立审计。
4. 失败/阻塞/部分完成也必须生成审计包。
5. Task Contract、Policy、Baseline 必须在事务开始时冻结并绑定 hash。
6. 普通实施任务不得修改自己的审计规则、核心政策或 Auditor-owned acceptance tests。
7. Capability 使用最小权限；高风险能力应限时、限次数。
8. 未授权 Scope / Dependency / Production / Paid / Destructive 扩张必须 STOP 并请求 Amendment。
9. Evidence 必须绑定 transaction 与 source identity；源码变化后旧证据失效。
10. Review Artifact 必须覆盖完整 changeset，不能只挑“主要文件”。
11. 打包不得通过移动、删除或覆盖源文件完成。
12. `AUDIT_APPROVED != RELEASE_APPROVED`。
13. CEAL 必须风险自适应，避免治理开销压倒开发本身。
