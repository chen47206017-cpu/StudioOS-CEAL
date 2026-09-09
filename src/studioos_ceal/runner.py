from __future__ import annotations
import hashlib,json,os
from collections import Counter,defaultdict
from datetime import UTC,datetime
from pathlib import Path,PurePosixPath
from typing import Any
from .engine import PolicyEngine
from .matrix import EVIDENCE_STATES,MATRIX_SIZE,MUTATIONS,PHASES,PRESSURES,generate_scenarios
from .models import Decision,Scenario

def _canonical_json(v:Any)->str: return json.dumps(v,ensure_ascii=False,sort_keys=True,separators=(",",":"))
def _atomic_write(path:Path,content:str):
    path.parent.mkdir(parents=True,exist_ok=True); tmp=path.with_suffix(path.suffix+".tmp"); tmp.write_text(content,encoding="utf-8",newline="\n"); os.replace(tmp,path)
def write_matrix(path,scenarios):
    body="\n".join(_canonical_json(s.as_dict()) for s in scenarios)+"\n"; _atomic_write(path,body); return hashlib.sha256(body.encode()).hexdigest()
def load_matrix(path):
    out=[]
    for n,line in enumerate(path.read_text(encoding="utf-8").splitlines(),1):
        if not line.strip(): continue
        try:
            r=json.loads(line); out.append(Scenario(r["scenario_id"],r["phase"],r["mutation"],r["evidence"],r["pressure"],Decision(r["expected_decision"])))
        except (KeyError,TypeError,ValueError,json.JSONDecodeError) as e: raise ValueError(f"invalid matrix row {n}: {e}") from e
    return out
def _orders(scenarios,sweeps):
    out=[]
    for sweep in range(sweeps):
        if sweep%3==0: out.append(list(scenarios))
        elif sweep%3==1: out.append(list(reversed(scenarios)))
        else: out.append(sorted(scenarios,key=lambda x:hashlib.sha256(f"{sweep}:{x.scenario_id}".encode()).digest()))
    return out
def _phase_sensitivity_count(scenarios,engine):
    g=defaultdict(set)
    for s in scenarios: g[(s.mutation,s.evidence,s.pressure)].add(engine.evaluate(s).decision)
    return sum(1 for v in g.values() if len(v)>1)
def run_assurance(scenarios=None,*,sweeps=3,generated_at=None):
    if sweeps<3: raise ValueError("at least three sweeps are required for stability evidence")
    scenarios=scenarios or generate_scenarios()
    if len(scenarios)!=MATRIX_SIZE: raise ValueError(f"full assurance run requires exactly {MATRIX_SIZE} scenarios")
    ids=[s.scenario_id for s in scenarios]; combos=[(s.phase,s.mutation,s.evidence,s.pressure) for s in scenarios]
    if len(set(ids))!=MATRIX_SIZE or len(set(combos))!=MATRIX_SIZE: raise ValueError("scenario matrix contains duplicate identifiers or combinations")
    engine=PolicyEngine(); known=set(); reports=[]; mismatches=[]; decision_counts=Counter()
    for sweep_number,ordered in enumerate(_orders(scenarios,sweeps),1):
        new=set(); counts=Counter()
        for s in ordered:
            e=engine.evaluate(s); counts[e.decision.value]+=1
            if sweep_number==1:
                decision_counts[e.decision.value]+=1
                if e.decision!=s.expected_decision: mismatches.append({"scenario_id":s.scenario_id,"expected":s.expected_decision.value,"actual":e.decision.value})
            for fam in e.high_priority_families:
                if fam not in known: new.add(fam)
        known.update(new); reports.append({"sweep":sweep_number,"scenario_evaluations":len(ordered),"gate_evaluations":len(ordered)*engine.gate_count,"new_p0_p1_finding_families":len(new),"decision_counts":dict(sorted(counts.items()))})
    stable=not mismatches and reports[-1]["new_p0_p1_finding_families"]==0 and reports[-2]["new_p0_p1_finding_families"]==0
    digest=hashlib.sha256("\n".join(_canonical_json(s.as_dict()) for s in scenarios).encode()).hexdigest()
    return {"schema_version":"1.1","generated_at":generated_at or datetime.now(UTC).isoformat(),"status":"STABLE_FOR_DEFINED_P0_P1_SPACE" if stable else "NOT_STABLE","claim_boundary":"Defined-space stability/model conformance only; not adaptive search, internet research, external runtime verification, or proof that unmodelled threats do not exist.","matrix":{"distinct_scenarios":len(scenarios),"dimensions":{"phases":len(PHASES),"mutations":len(MUTATIONS),"evidence_states":len(EVIDENCE_STATES),"pressures":len(PRESSURES)},"sha256":digest,"phase_sensitive_contexts":_phase_sensitivity_count(scenarios,engine)},"six_gate_checks_first_sweep":len(scenarios)*engine.gate_count,"actual_invocation_count":len(scenarios)*sweeps,"total_scenario_evaluations":len(scenarios)*sweeps,"total_gate_evaluations":len(scenarios)*sweeps*engine.gate_count,"decision_counts_first_sweep":dict(sorted(decision_counts.items())),"oracle_mismatches":mismatches,"p0_p1_finding_families":sorted(known),"sweeps":reports,"stop_rule":{"required_consecutive_zero_novelty_sweeps":2,"observed_consecutive_zero_novelty_sweeps":2 if stable else 0,"scope":"defined high-value non-duplicate P0/P1 families","interpretation":"full-space stability confirmation; not adaptive search"}}
def write_report(path,report):
    body=json.dumps(report,ensure_ascii=False,indent=2,sort_keys=True)+"\n"; _atomic_write(path,body); return hashlib.sha256(body.encode()).hexdigest()
def _safe_manifest_path(root,file_path):
    resolved=file_path.resolve()
    try: rel=resolved.relative_to(root.resolve())
    except ValueError as e: raise ValueError(f"manifest file escapes evidence root: {file_path}") from e
    posix=rel.as_posix(); parts=PurePosixPath(posix).parts
    if not posix or posix.startswith("/") or ".." in parts: raise ValueError(f"unsafe manifest path: {posix}")
    return posix
def write_manifest(path,files):
    root=path.parent; records=[]; seen=set()
    for fp in sorted(files,key=lambda x:x.as_posix()):
        rel=_safe_manifest_path(root,fp)
        if rel in seen: raise ValueError(f"duplicate manifest path: {rel}")
        seen.add(rel); data=fp.read_bytes(); records.append({"path":rel,"bytes":len(data),"sha256":hashlib.sha256(data).hexdigest()})
    _atomic_write(path,json.dumps({"schema_version":"1.0","files":records},indent=2,sort_keys=True)+"\n")
def verify_manifest(path):
    root=path.parent.resolve()
    try: raw=json.loads(path.read_text(encoding="utf-8"))
    except (OSError,json.JSONDecodeError) as e: return [f"MANIFEST_READ_ERROR: {e}"]
    records=raw.get("files")
    if not isinstance(records,list): return ["MANIFEST_FILES_INVALID"]
    errors=[]; seen=set()
    for i,r in enumerate(records):
        if not isinstance(r,dict): errors.append(f"record[{i}]: invalid"); continue
        rel=r.get("path")
        if not isinstance(rel,str): errors.append(f"record[{i}]: path invalid"); continue
        parts=PurePosixPath(rel).parts
        if not rel or rel.startswith("/") or ".." in parts or "\\" in rel: errors.append(f"{rel}: unsafe path"); continue
        if rel in seen: errors.append(f"{rel}: duplicate path"); continue
        seen.add(rel); target=(root/rel).resolve()
        try: target.relative_to(root)
        except ValueError: errors.append(f"{rel}: path escapes root"); continue
        if not target.is_file(): errors.append(f"{rel}: missing"); continue
        data=target.read_bytes()
        if r.get("bytes")!=len(data): errors.append(f"{rel}: byte size mismatch")
        if r.get("sha256")!=hashlib.sha256(data).hexdigest(): errors.append(f"{rel}: sha256 mismatch")
    return errors
