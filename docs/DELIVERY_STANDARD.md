# 工程交付标准

## 最小任务包

每个实施任务必须明确：

- Task ID、标题、模式、状态、风险等级；
- 文件 allowlist 与 denylist；
- 完成标准和必跑命令；
- 是否要求 runtime/production evidence；
- 回滚策略；
- 停止条件。

模板见 \`templates/TASK_PACKAGE.example.json\`。

## 状态语义

| 状态 | 可以证明 | 不能暗示 |
|---|---|---|
| CODE_COMPLETE | 范围内代码已写完 | 测试通过 |
| TEST_PASS | 指定自动测试当前通过 | 真实运行时可用 |
| RUNTIME_VERIFIED | 隔离或指定运行时有真实证据 | 生产环境已验证 |
| PRODUCTION_VERIFIED | 指定生产证据链完成 | 所有未来场景无风险 |
| BLOCKED | 有明确阻塞和证据 | 任务失败或可静默跳过 |

## IMPLEMENTATION_REPORT 必备字段

1. Task ID、模式和最终状态。
2. 基线分支、基线 commit、变更 commit。
3. 实际 changed files；不得只列计划文件。
4. 每条测试命令、退出码和关键输出。
5. runtime/production evidence 的来源、时间、环境和 hash。
6. 未完成项、风险、假设和 blocker。
7. 文件级或提交级回滚方法。
8. PR/提交链接。

## 自动执行与再次确认

当用户已经给出变更目标，且任务包为 \`APPROVED_FOR_IMPLEMENTATION\`、所有动作均在 allowlist 内时，代理直接实施、测试和交付，不再次询问“是否继续”。

仅当 \`AGENTS.md\` 第 3 节的停止闸触发时，才需要用户提供新决定或权限。

## 关闭条件

关闭必须同时满足：

- diff 与 allowlist 一致；
- denylist 未触碰；
- 必跑测试退出码全部为 0；
- 要求的证据存在且属于当前版本；
- hash manifest 可复算；
- 没有把较低状态写成 READY；
- 回滚路径有效。
