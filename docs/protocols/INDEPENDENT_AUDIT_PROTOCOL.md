# Independent Audit Protocol

## 无论结果都必须回传

- SUCCESS: `<TASK>_REVIEW.zip`
- FAILED: `<TASK>_FAILED_REVIEW.zip`
- BLOCKED: `<TASK>_BLOCKED_REVIEW.zip`
- PARTIAL: `<TASK>_PARTIAL_REVIEW.zip`

## ZIP 最低内容

全部新增/修改文件、删除/重命名记录、baseline、精确 iteration patch、changed-files manifest、symbol-change manifest、requirements、claims、evidence plan、测试源码与原始日志、build/runtime evidence、side-effect ledger、dependency manifest、source-preservation evidence、NOT_DONE、UNKNOWNS、ASSUMPTIONS、BOM、artifact manifest、ZIP SHA256/size/entry count。

Audit Verdict 必须同时绑定 exact artifact SHA-256 与被批准的 immutable source identity；只绑定 ZIP 而不绑定源码版本不能 `AUDIT_APPROVED`。

## Evidence Level

E0 Claim only  
E1 Static  
E2 Unit  
E3 Integration  
E4 Live Runtime / Browser  
E5 Independent Audit

低等级证据不得冒充高等级验收。
