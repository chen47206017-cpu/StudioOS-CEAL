# 8000+ 对抗验证方法

## 当前定义空间

使用完整笛卡尔积，不抽样：

| 维度 | 数量 |
|---|---:|
| 生命周期阶段 | 10 |
| 变更/攻击类型 | 14 |
| 证据状态 | 10 |
| 交付压力 | 8 |

总数：`10 × 14 × 10 × 8 = 11,200`。

每个场景实际执行六个策略 Gate；三轮为 33,600 次场景调用和 201,600 次 Gate 评估。

## 对上一分支方法的修正

早期 8000-space 虽然组合唯一，但 `phase` 没有参与决策，存在“组合唯一但语义重复”的 coverage inflation 风险。0.2.0 将测试、runtime、provenance 等证据要求与生命周期阶段绑定，并要求 `phase_sensitive_contexts > 0`。

新增高价值攻击族：

- Policy drift
- Task Contract drift
- untracked changeset omission
- audit-rule self modification

## Oracle + 独立不变量

逐场景 expected decision 与 PolicyEngine 比较，但 oracle 与 engine 仍可能存在共同规格盲点，所以另外执行不依赖逐项 expected 的全矩阵不变量：

- P0 mutation 永远 BLOCK；
- Scope escape 永远不能 ALLOW；
- contradictory/side-effect evidence 永远 BLOCK；
- deadline 不能削弱硬阻断。

## 三次全空间稳定性扫描

顺序、逆序、确定性哈希顺序各扫描一次。只有 mismatch=0 且最后两轮新增 P0/P1 family=0，才输出 `STABLE_FOR_DEFINED_P0_P1_SPACE`。

这只是定义空间稳定性，不是自适应搜索或未知风险穷尽。

## Evidence

审计执行使用 `--keep-matrix`，raw JSONL 与 summary 一并写入 SHA-256 manifest；`verify-manifest` 必须独立通过。
