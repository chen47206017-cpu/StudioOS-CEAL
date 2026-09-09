# CEAL Threat Model

重点防御：

- T1 Agent 遗漏改动
- T2 自测假通过
- T3 Scope drift
- T4 Agent 修改自己的审计政策
- T5 Stale runtime
- T6 Stale artifact
- T7 Test gaming / oracle 共因错误
- T8 Side-effect escape
- T9 Source loss
- T10 Secret leakage
- T11 Dependency drift
- T12 Evidence contamination
- T13 Baseline tampering
- T14 Untracked-file omission
- T15 Review ZIP 漏包
- T16 Audit verdict 未绑定 exact source identity
- T17 把旧的人类授权推断为本轮授权
- T18 Governance overhead explosion
- T19 用语义无效维度虚增“8000+”覆盖数字
- T20 JSON Schema 与实际 CLI validator 漂移
- T21 Manifest 声明的 size/hash 与真实 blob 不一致
- T22 分支并行演化后直接 merge，导致较弱治理覆盖较强治理
- T23 未受保护 main 被绕过 PR/CI 直接写入

默认处置：对 P0 风险 BLOCK；对授权/范围/完整性不确定 HOLD 或 ESCALATE；保留 source identity 和最小复现。

## 当前非目标 / 外部控制面

CEAL 当前不提供 OS sandbox、Secret 托管、数字签名服务或 GitHub branch protection 的平台级强制执行。它们必须由真实平台配置证明。
