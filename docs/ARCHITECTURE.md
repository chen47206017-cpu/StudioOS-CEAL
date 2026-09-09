# CEAL v0.1 架构

## 目标

CEAL 将工程代理行为约束为一条可审计状态机，而不是自由扩张的“多做一点”。系统保持项目无关，不包含 StudioOS 业务实现。

\`\`\`mermaid
flowchart TD
    A["Task Contract"] --> B["Baseline"]
    B --> C["Six Gates"]
    C --> D["Implementation"]
    D --> E["Tests"]
    E --> F["Evidence + SHA-256"]
    F --> G["Independent Audit"]
    G --> H["Close or Block"]
\`\`\`

## 组件

| 组件 | 职责 | 不负责 |
|---|---|---|
| Contract validator | 校验任务模式、状态、范围、验收、回滚和停止条件 | 替用户授予权限 |
| Scenario generator | 生成确定性的 8000 个唯一组合 | 模拟真实产品运行时 |
| Policy engine | 通过六道门禁产生 fail-closed 决策 | 自动修改仓库 |
| Assurance runner | 对比独立 oracle、统计 finding family、判定收敛 | 宣称生产 READY |
| Evidence writer | 原子写报告与 SHA-256 manifest | 代替签名或可信构建平台 |
| Repository contract | 让 Codex 自动继承长期规则 | 覆盖用户本轮明确指令 |

## 六道门禁

1. Contract：授权是否明确。
2. Scope：路径、依赖和架构是否在范围内。
3. Risk：Secret、破坏性动作、生产写入、付费调用和证据篡改。
4. Execution：工具失败、重试失控和生产事故。
5. Evidence：缺失、陈旧、mock、矛盾、副作用和 provenance。
6. Closure：拒绝 partial success 与 historical PASS 冒充本轮完成。

最终决策使用严格优先级：

\`BLOCK > ESCALATE > HOLD > ALLOW\`

任何 deadline 压力都不能降低门禁结果。

## 数据流

\`\`\`text
Task Package
  -> validate_task_package()
  -> deterministic scenario matrix
  -> PolicyEngine.evaluate()
  -> independent oracle comparison
  -> novelty sweeps
  -> adversarial-summary.json
  -> manifest.json
\`\`\`

## 信任边界

- 仓库代码和本地生成报告属于 CEAL 自身验证范围。
- GitHub Actions、分支保护和托管环境属于外部控制面，只能按真实配置陈述。
- StudioOS、ComfyUI、模型、GPU、API 和生产数据属于外部产品面，必须另有产品任务包和运行证据。
