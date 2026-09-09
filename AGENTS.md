# CEAL Agent Entry

1. 先读 `ceal/constitution/CONSTITUTION.md`。
2. 读取 Project Profile、Task Contract、当前 TASK_CONTEXT。
3. 写文件前必须冻结 baseline。
4. 遵守 Scope / Capability / Runtime / Dependency / Side-effect 边界。
5. 普通任务不得修改 `ceal/constitution/**`、`policies/**`、`schemas/**`、`audit/acceptance/**`，除非 `task_type=GOVERNANCE_CHANGE`。
6. 完成后必须 verify。
7. 无论 SUCCESS / FAILED / BLOCKED / PARTIAL / TIMEOUT，都必须 package。
8. 打包后 STOP，等待 Independent Audit。
9. Implementation Agent 不得自我声明 `AUDIT_APPROVED`。

必须区分：
`IMPLEMENTED / SELF_VERIFIED / RUNTIME_VERIFIED / AUDIT_APPROVED / RELEASE_APPROVED`。
