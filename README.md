# StudioOS-CEAL

StudioOS-CEAL 是一个项目无关的受控工程保障框架。任何 Codex、Luna 或其他工程代理的修改，都被视为一笔可追踪、可验证、可回滚、经过独立证据才能关闭的工程事务。

本仓库当前是 **CEAL v0.1 治理内核**，不是 StudioOS 产品源码，也不证明任何外部 Runtime、ComfyUI、云 GPU 或生产环境已经可用。

## 已实现

- 任务包合同校验：模式、状态、风险、文件 allowlist/denylist、验收命令、回滚和停止条件。
- 六道独立门禁：Contract、Scope、Risk、Execution、Evidence、Closure。
- Fail-closed 决策：\`ALLOW / HOLD / ESCALATE / BLOCK\`。
- 确定性的 8000 个唯一对抗场景：
  - 10 个生命周期阶段；
  - 10 类变更或攻击；
  - 10 种证据状态；
  - 8 类交付压力。
- 每轮 48000 次门禁检查；三轮共 24000 次场景评估、144000 次门禁评估。
- 独立结果 oracle、重复检测、证据摘要、SHA-256 manifest 和两轮零新增 P0/P1 收敛规则。
- 仓库级 \`AGENTS.md\`：以后 Codex 自动继承范围、验收和交付要求。

## 快速开始

无需第三方 Python 依赖：

\`\`\`bash
PYTHONPATH=src python -m unittest discover -s tests -v
PYTHONPATH=src python -m studioos_ceal validate-task templates/TASK_PACKAGE.example.json
PYTHONPATH=src python -m studioos_ceal run --output-dir evidence
\`\`\`

完整矩阵默认不提交 Git；需要审计原始行时：

\`\`\`bash
PYTHONPATH=src python -m studioos_ceal run --output-dir evidence --keep-matrix
\`\`\`

## 诚实口径

“8000+”表示由代码确定性生成并实际执行的 8000 个不同场景，不表示人工完成 8000 次互联网搜索。收敛只证明：

1. 当前定义的 CEAL 范围全部被遍历；
2. 策略结果与独立 oracle 没有偏差；
3. 后续两次不同顺序的全量扫描没有新增高价值、非重复、范围内 P0/P1 finding family。

它不证明外部产品或生产运行时 READY。新增维度、风险或产品能力后，必须重新运行。

## 设计依据

- [NIST SSDF SP 800-218](https://csrc.nist.gov/projects/ssdf)：安全开发实践、完整性与来源证据。
- [SLSA v1.2](https://slsa.dev/spec/v1.2/)：可验证 provenance 与构建完整性。
- [OWASP SAMM Verification](https://owaspsamm.org/model/verification/)：贯穿生命周期的验证活动。
- [OpenSSF Scorecard checks](https://github.com/ossf/scorecard/blob/main/docs/checks.md)：分支保护、最小令牌权限、固定依赖等仓库安全基线。

## 目录

- \`src/studioos_ceal/\`：无第三方运行依赖的 CEAL 内核与 CLI。
- \`tests/\`：合同、门禁、矩阵和 CLI 回归测试。
- \`templates/\`：任务包和一次性 Codex 指令模板。
- \`schemas/\`：机器可读任务包 JSON Schema。
- \`docs/\`：架构、对抗方法、威胁模型和交付标准。
- \`evidence/\`：已执行验证摘要与哈希清单。

## 当前边界

- IN：工程任务治理、范围控制、证据链、审计状态、收敛验证。
- OUT：StudioOS 业务 UI、视频生成、模型下载、云 GPU、生产数据库、真实 Secret、付费调用、不可逆升级。
- 状态：\`CEAL_POLICY_RUNTIME_VERIFIED\`；外部产品状态为 \`NOT_EVALUATED\`。
