# Codex 最短任务提示词

复制后只替换尖括号内容：

\`\`\`text
执行 <TASK-ID>：<一个明确、可验证的结果>。

仓库：<owner/repository 或本地项目根>
模式：implement_and_verify
范围：<允许修改的目录或任务包路径>

按仓库 AGENTS.md 自动完成。已授权范围内不要重复询问；触发停止闸时只报告具体 blocker 和所需选择。
完成后提交 IMPLEMENTATION_REPORT，并给出测试退出码、证据 SHA-256、风险、回滚和 PR/提交链接。
\`\`\`

如果仓库已有有效的 \`TASK_PACKAGE\`，可以缩短为：

\`\`\`text
执行 TASK-XXX：<目标>。
读取仓库 AGENTS.md 和对应 TASK_PACKAGE，直接实施并验收；触发停止闸才询问。
\`\`\`

## 不需要重复写的内容

以下要求已固化在 \`AGENTS.md\`，以后无需每次粘贴：

- 中文报告；
- 先检查范围和基线；
- 不碰 denylist、生产数据、真实 Secret、付费调用；
- 不伪造 PASS；
- 自动测试与运行证据；
- SHA-256、风险、回滚；
- 独立分支和 PR；
- 完成后不反复要求“继续”。
