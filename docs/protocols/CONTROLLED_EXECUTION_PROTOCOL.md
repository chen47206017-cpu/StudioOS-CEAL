# Controlled Execution Protocol

## 执行前冻结

- transaction_id
- canonical task_contract_hash
- policy_hash
- baseline/source identity
- evidence_plan
- risk
- capability lease

`Task Package` 必须绑定以上 identity，且任何字段不得扩大 Task Contract 的 Scope、Capability 或 Side-effect 权限。

## Plan Gate

写文件前记录 planned files/symbols/tests/side effects/dependency/restart/risk。实际变化明显超计划触发 `PLAN_EXECUTION_DRIFT`。

## Changeset Gate

关闭前必须从实际工作区/Git 状态发现完整 changeset，覆盖新增、修改、删除、重命名和相关 untracked 文件。Agent 自填 `changed_paths` 只能作为声明，不能单独证明完整。

## Side-effect Ledger

至少记录 FILE_WRITE / FILE_DELETE / PROCESS_START / PROCESS_STOP / SERVICE_RESTART / NETWORK_READ / NETWORK_WRITE / DB_WRITE / EXTERNAL_API / CLOUD_RESOURCE / COST_ACTION / GIT_WRITE。

## Repair Budget

超过授权 repair loops 必须 STOP + PACKAGE，不允许无限扩大变更。
