# Contributing

所有变更遵守根目录 \`AGENTS.md\`。

## 本地检查

\`\`\`bash
PYTHONPATH=src python -m unittest discover -s tests -v
PYTHONPATH=src python -m studioos_ceal validate-task templates/TASK_PACKAGE.example.json
PYTHONPATH=src python -m studioos_ceal run --output-dir evidence
\`\`\`

提交 PR 时说明：

- 变更对应的 Task ID；
- allowlist/denylist；
- 实际测试和退出码；
- 是否改变对抗矩阵维度、决策优先级或状态语义；
- 风险与回滚。

修改策略或 oracle 时必须同时增加回归测试，不能为了得到 PASS 同时弱化二者。
