# Contributing

所有变更遵守根目录 `AGENTS.md` 与 `ceal/constitution/CONSTITUTION.md`。

本地检查：

```bash
python -m compileall -q src tests
PYTHONPATH=src python -m unittest discover -s tests -v
PYTHONPATH=src python -m studioos_ceal validate-task templates/TASK_PACKAGE.example.json
PYTHONPATH=src python -m studioos_ceal run --output-dir evidence --keep-matrix
PYTHONPATH=src python -m studioos_ceal verify-manifest evidence/manifest.json
```

PR 必须说明 Task/Transaction ID、Scope、实际测试、是否改变 policy/oracle/schema、风险与回滚。修改 PolicyEngine、oracle 或矩阵维度时必须增加独立不变量测试，不能为了得到 PASS 同时弱化 engine 与 oracle。
