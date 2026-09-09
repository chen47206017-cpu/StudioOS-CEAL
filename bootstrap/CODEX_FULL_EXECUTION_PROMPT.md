# CEAL-BOOTSTRAP-001 — Codex Full Execution Authorization

目标：实现 CEAL v1.0 Kernel 最小闭环，不扩展到 StudioOS 专用逻辑。

## 边界
- Core 禁止写死 ComfyUI / 8189 / 8190 / DRFE / Seedance / GPU。
- 不进入 Multi-Agent / OPA / Sigstore / SLSA / OpenTelemetry / Web UI。
- 不为了方便引入大型依赖；优先 Python 标准库。
- 不通过修改 Constitution / Audit Protocol 来降低验收门禁。
- 不自动进入下一阶段。

## Phase A Baseline
生成不可静默重写的 `CEAL_BOOTSTRAP_BASELINE.json`，记录文件清单、SHA256、Git HEAD（若有）、untracked、policy hash。

## Phase B Kernel
实现：
`ceal init / start / status / verify / package / audit-import / close`

## Phase C Required Objects
Project Profile / Task Contract / Transaction ID / Plan / Risk / Capability Lease / Baseline / Complete Filesystem Delta / Evidence Plan / Requirement Trace / Claim Trace / Artifact Manifest / Audit Verdict / Close Gate。

## Phase D Tests
至少验证：
1. baseline 不可静默替换；
2. untracked 能被 changeset 捕获；
3. FAILED 也会产生 ZIP；
4. Artifact 漏 changed file 时 verify FAIL；
5. verdict 必须绑定 exact artifact SHA；
6. 未导入 AUDIT_APPROVED 时 close 拒绝；
7. policy hash 漂移触发 POLICY_DRIFT；
8. task contract hash 漂移触发 TASK_CONTRACT_DRIFT；
9. 普通 task 改 protected governance path 时 FAIL；
10. manifest 引用不存在文件时 FAIL。

## Mandatory Audit Packaging
无论 SUCCESS / FAILED / BLOCKED / PARTIAL / TIMEOUT，必须 COPY-ONLY 打包本轮**全部新增、修改、删除记录与证据**。

最终必须输出：
- execution status
- review artifact absolute path
- ZIP size
- entry count
- SHA256
- SOURCE_FILES_PRESERVED=true

然后 STOP。不得自行宣布 AUDIT_APPROVED，等待用户上传给 GPT-5.6 Sol 独立审计。
