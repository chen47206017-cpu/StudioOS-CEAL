# 工程交付标准

## Canonical 授权

每个实施任务必须有 Task Contract。Task Package 是绑定 Task Contract / Policy / Baseline 的运行封装，不能扩大授权。

至少明确：

- Task / Transaction identity；
- 风险等级；
- allowlist / denylist；
- capabilities / side-effect permissions；
- acceptance / evidence plan；
- rollback / stop conditions；
- complete changeset 的发现方式。

## 状态真值

CODE_COMPLETE 只证明范围内代码完成；TEST_PASS 不证明 runtime；RUNTIME_VERIFIED 不证明 production；AUDIT_APPROVED 不等于 RELEASE_APPROVED。

Closure-level 状态必须使用 `DISCOVERED_GIT` 或等价机制证明完整 changeset，不得只依赖 Agent 声明。

## 必备交付

- baseline/source identity；
- 实际 changed files；
- 测试命令、退出码、原始日志；
- evidence level 与 SHA-256；
- NOT_DONE / UNKNOWNS / assumptions；
- rollback；
- PR/commit；
- Review Artifact 和独立 audit verdict。

## CEAL 自身验证

```bash
PYTHONPATH=src python -m unittest discover -s tests -v
PYTHONPATH=src python -m studioos_ceal validate-task templates/TASK_PACKAGE.example.json
PYTHONPATH=src python -m studioos_ceal run --output-dir evidence --keep-matrix
PYTHONPATH=src python -m studioos_ceal verify-manifest evidence/manifest.json
```
