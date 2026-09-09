# Controlled Execution Protocol

## 执行前冻结
- transaction_id
- task_contract_hash
- policy_hash
- baseline
- evidence_plan
- risk
- capability lease

## Plan Gate
写文件前记录 planned files/symbols/tests/side effects/dependency/restart/risk。
实际变化明显超计划触发 `PLAN_EXECUTION_DRIFT`。

## Side-effect Ledger
至少记录 FILE_WRITE / FILE_DELETE / PROCESS_START / PROCESS_STOP / SERVICE_RESTART / NETWORK_READ / NETWORK_WRITE / DB_WRITE / EXTERNAL_API / CLOUD_RESOURCE / COST_ACTION / GIT_WRITE。

## Repair Budget
超过授权 repair loops 必须 STOP + PACKAGE，不允许无限扩大变更。
