# Codex 最短任务提示词

CEAL 的 canonical 授权对象是 `Task Contract`；`Task Package` 只是绑定其 SHA-256、Policy、Baseline 与执行证据要求的运行封装，不能扩大 Task Contract 权限。

```text
执行 <TASK-ID>：<一个明确、可验证的结果>。
仓库：<owner/repository 或本地项目根>
读取 AGENTS.md、canonical Task Contract 和对应 Task Package。
在冻结的 Scope / Capability / Side-effect 边界内直接实施并验收；
只有触发 stop condition 时才询问。
完成后按 Evidence Protocol 打包并停止，等待 Independent Audit。
```

不得把旧聊天授权、历史 PASS、mock、HTTP 200、或 Task Package 中更宽的字段解释为扩大 canonical Task Contract。
