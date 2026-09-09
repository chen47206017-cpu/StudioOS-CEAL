# CEAL Branch Integration & Adversarial Review Report

Reviewed branches: `main@22b94abcd0da9ec9de10ea91f6efaddfbca84416`, `ceal-bootstrap-001@d33356a3abe303fdb7822926f3c9f5415c245852`, `codex/ceal-bootstrap-v0.1.0@ebcfd87fe74cb819877aa5f7c24ad045e601af60`.

Integration policy: preserve stronger v1 bootstrap governance, selectively integrate executable assurance runtime, reject duplicate authority docs, and repair governance/runtime contradictions before merge.

Key repairs: lifecycle phase now has semantic effect; new policy/task-contract drift, untracked omission and audit-rule self-modification attacks; independent invariant tests beyond oracle comparison; Task Package binds canonical contract/policy/baseline and L4; closure-level states require discovered complete changeset; manifest verification detects path escape, duplicate/missing/size/hash drift; competing v0.1 architecture/threat-model authority docs are not introduced.

Local verification of integrated candidate: compile PASS; 29 tests PASS; Task Package validation PASS; Draft 2020-12 schemas PASS; contract/package templates PASS; audit verdict positive/negative fixtures PASS; secret scan 0 confirmed; 11,200 unique scenarios × 3 sweeps = 33,600 invocations / 201,600 gate evaluations, oracle mismatches 0, phase-sensitive contexts 8, status `STABLE_FOR_DEFINED_P0_P1_SPACE`; evidence manifest PASS.

Residual risks: main is currently unprotected; integrated Assurance Runtime is not the full persistent CEAL v1 Transaction Manager; agent-created commits may be unsigned; stability only covers explicitly modelled space.

Merge gate: GitHub CI on the integration commit must succeed and PR must remain conflict-free. After merge correct state is `BOOTSTRAP_GOVERNANCE + ASSURANCE_RUNTIME_0.2.0_MERGED`, not full CEAL v1 Kernel completion.
