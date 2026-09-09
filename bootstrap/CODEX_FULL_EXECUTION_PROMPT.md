# CEAL v1 Kernel — Future Codex Full Execution Authorization

本文件是未来 Kernel 实施授权文档，不因进入仓库而自动执行。

目标：在当前 Bootstrap Governance + Assurance Runtime 基础上，实现 CEAL v1 Kernel 最小闭环，不扩展到 StudioOS 专用逻辑。

## 边界

- Core 禁止写死 ComfyUI / 8189 / 8190 / DRFE / Seedance / GPU。
- 不进入 Multi-Agent / OPA / Sigstore / SLSA / OpenTelemetry / Web UI。
- 不为了方便引入大型依赖；优先 Python 标准库。
- 不通过修改 Constitution / Audit Protocol 降低验收门禁。
- Task Package 不得扩大 canonical Task Contract。
- 不自动进入下一阶段。

## Required Kernel commands

`ceal init / start / status / verify / package / audit-import / close`

## Required properties

- baseline 不可静默替换
- complete changeset 包含 untracked/deleted/renamed
- FAILED/BLOCKED/PARTIAL 也产生 Review Artifact
- artifact 漏 changed file 时 verify FAIL
- verdict 绑定 exact artifact SHA + source identity
- 未导入 AUDIT_APPROVED 时 close 拒绝
- policy/task contract/baseline drift fail closed
- ordinary task 修改 protected governance FAIL

最终必须 package 后 STOP，等待 Independent Audit。
