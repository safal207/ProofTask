#!/usr/bin/env python3
"""ProofTask CLI.

A tiny, dependency-free CLI for the first ProofTask MVP:

- create a task JSON file
- validate a task JSON file
- validate a human proof JSON file
- validate a verification trace JSON file
- create a submitted trace from task + proof
- verify or reject the submitted trace
- render a PR-ready verification comment from a trace
- keep a small local task/proof/trace ledger

This is intentionally small. It is a seed mechanism, not a full marketplace.
"""

from __future__ import annotations

import argparse
import json
import sys
import uuid
from copy import deepcopy
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


TASK_STATUSES = {"created", "accepted", "submitted", "verified", "rejected", "cancelled"}
SUBMIT_ALLOWED_STATUSES = {"created", "accepted"}
TRACE_STATUSES = {"submitted", "verified", "rejected"}
FINAL_STATUSES = {"verified", "rejected"}
PROOF_RESULTS = {"pass", "fail", "blocked", "inconclusive"}
PAYMENT_STATUSES = {"none", "pending", "escrowed", "released", "refunded"}
EVIDENCE_TYPES = {"screenshot", "video", "log", "text", "link", "other"}
LEDGER_VERSION = "0.1"
LEDGER_DIRS = ("tasks", "proofs", "traces")


class ProofTaskError(ValueError):
    """Raised when an input file is not valid for the MVP flow."""


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z")


def generate_task_id() -> str:
    return f"task_{uuid.uuid4().hex[:12]}"


def read_json(path: str | Path) -> dict[str, Any]:
    file_path = Path(path)
    try:
        with file_path.open("r", encoding="utf-8") as f:
            data = json.load(f)
    except FileNotFoundError as exc:
        raise ProofTaskError(f"File not found: {file_path}") from exc
    except json.JSONDecodeError as exc:
        raise ProofTaskError(f"Invalid JSON in {file_path}: {exc}") from exc

    if not isinstance(data, dict):
        raise ProofTaskError(f"{file_path} must contain a JSON object")

    return data


def write_json(path: str | Path, data: dict[str, Any]) -> None:
    file_path = Path(path)
    file_path.parent.mkdir(parents=True, exist_ok=True)
    with file_path.open("w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
        f.write("\n")


def write_text(path: str | Path, content: str) -> None:
    file_path = Path(path)
    file_path.parent.mkdir(parents=True, exist_ok=True)
    file_path.write_text(content, encoding="utf-8")


def require_fields(data: dict[str, Any], required: list[str], kind: str) -> None:
    missing = [field for field in required if field not in data]
    if missing:
        raise ProofTaskError(f"{kind} is missing required field(s): {', '.join(missing)}")


def require_non_empty_string(data: dict[str, Any], field: str, kind: str) -> None:
    value = data.get(field)
    if not isinstance(value, str) or not value.strip():
        raise ProofTaskError(f"{kind}.{field} must be a non-empty string")


def require_string_list(data: dict[str, Any], field: str, kind: str) -> None:
    value = data.get(field)
    if not isinstance(value, list) or not value:
        raise ProofTaskError(f"{kind}.{field} must be a non-empty list")
    if not all(isinstance(item, str) and item.strip() for item in value):
        raise ProofTaskError(f"{kind}.{field} must contain only non-empty strings")


def create_task(
    *,
    task_type: str,
    created_by: str,
    objective: str,
    acceptance_criteria: list[str],
    proof_required: list[str],
    task_id: str | None = None,
    payment_amount: float | None = None,
    payment_currency: str = "USD",
    payment_status: str = "pending",
    trace_reason: str | None = None,
    trace_source: str | None = None,
) -> dict[str, Any]:
    task: dict[str, Any] = {
        "task_id": task_id or generate_task_id(),
        "created_by": created_by,
        "task_type": task_type,
        "objective": objective,
        "acceptance_criteria": acceptance_criteria,
        "proof_required": proof_required,
        "status": "created",
    }
    if payment_amount is not None:
        task["payment"] = {"amount": payment_amount, "currency": payment_currency, "status": payment_status}
    trace: dict[str, str] = {}
    if trace_reason:
        trace["reason"] = trace_reason
    if trace_source:
        trace["source"] = trace_source
    if trace:
        task["trace"] = trace
    return validate_task(task)


def validate_task(task: dict[str, Any]) -> dict[str, Any]:
    require_fields(task, ["task_id", "created_by", "task_type", "objective", "acceptance_criteria", "proof_required", "status"], "task")
    for field in ["task_id", "created_by", "task_type", "objective", "status"]:
        require_non_empty_string(task, field, "task")
    require_string_list(task, "acceptance_criteria", "task")
    require_string_list(task, "proof_required", "task")
    if task["status"] not in TASK_STATUSES:
        raise ProofTaskError(f"task.status must be one of: {', '.join(sorted(TASK_STATUSES))}")
    payment = task.get("payment")
    if payment is not None:
        if not isinstance(payment, dict):
            raise ProofTaskError("task.payment must be an object when present")
        if "amount" in payment and not isinstance(payment["amount"], (int, float)):
            raise ProofTaskError("task.payment.amount must be a number")
        if "amount" in payment and payment["amount"] < 0:
            raise ProofTaskError("task.payment.amount must be >= 0")
        if "currency" in payment and not isinstance(payment["currency"], str):
            raise ProofTaskError("task.payment.currency must be a string")
        if "currency" in payment and not payment["currency"].strip():
            raise ProofTaskError("task.payment.currency must be a non-empty string")
        if "status" in payment and payment["status"] not in PAYMENT_STATUSES:
            raise ProofTaskError("task.payment.status must be one of: " + ", ".join(sorted(PAYMENT_STATUSES)))
    trace = task.get("trace")
    if trace is not None and not isinstance(trace, dict):
        raise ProofTaskError("task.trace must be an object when present")
    return task


def validate_proof(proof: dict[str, Any]) -> dict[str, Any]:
    require_fields(proof, ["proof_id", "task_id", "submitted_by", "result", "report", "submitted_at"], "proof")
    for field in ["proof_id", "task_id", "submitted_by", "result", "report", "submitted_at"]:
        require_non_empty_string(proof, field, "proof")
    if proof["result"] not in PROOF_RESULTS:
        raise ProofTaskError(f"proof.result must be one of: {', '.join(sorted(PROOF_RESULTS))}")
    evidence = proof.get("evidence", [])
    if evidence is not None:
        if not isinstance(evidence, list):
            raise ProofTaskError("proof.evidence must be a list when present")
        for index, item in enumerate(evidence):
            if not isinstance(item, dict):
                raise ProofTaskError(f"proof.evidence[{index}] must be an object")
            require_fields(item, ["type", "uri"], f"proof.evidence[{index}]")
            require_non_empty_string(item, "type", f"proof.evidence[{index}]")
            require_non_empty_string(item, "uri", f"proof.evidence[{index}]")
            if item["type"] not in EVIDENCE_TYPES:
                raise ProofTaskError(f"proof.evidence[{index}].type must be one of: " + ", ".join(sorted(EVIDENCE_TYPES)))
    environment = proof.get("environment")
    if environment is not None and not isinstance(environment, dict):
        raise ProofTaskError("proof.environment must be an object when present")
    return proof


def ensure_task_proof_match(task: dict[str, Any], proof: dict[str, Any]) -> None:
    if task["task_id"] != proof["task_id"]:
        raise ProofTaskError(f"Task/proof mismatch: task_id {task['task_id']!r} != {proof['task_id']!r}")


def create_submitted_trace(task: dict[str, Any], proof: dict[str, Any]) -> dict[str, Any]:
    ensure_task_proof_match(task, proof)
    if task["status"] not in SUBMIT_ALLOWED_STATUSES:
        raise ProofTaskError("Task can be submitted only from status: " + ", ".join(sorted(SUBMIT_ALLOWED_STATUSES)))
    submitted_task = deepcopy(task)
    submitted_task["status"] = "submitted"
    now = utc_now()
    trace_id = f"trace_{uuid.uuid4().hex[:12]}"
    return {
        "trace_id": trace_id,
        "task_id": submitted_task["task_id"],
        "status": "submitted",
        "created_at": now,
        "updated_at": now,
        "task": submitted_task,
        "proof": deepcopy(proof),
        "events": [
            {"event_type": "task_loaded", "status": task["status"], "at": now, "actor": task["created_by"]},
            {"event_type": "proof_submitted", "status": "submitted", "at": now, "actor": proof["submitted_by"], "proof_id": proof["proof_id"], "result": proof["result"]},
        ],
    }


def validate_trace(trace: dict[str, Any]) -> dict[str, Any]:
    require_fields(trace, ["trace_id", "task_id", "status", "created_at", "updated_at", "task", "proof", "events"], "trace")
    for field in ["trace_id", "task_id", "status", "created_at", "updated_at"]:
        require_non_empty_string(trace, field, "trace")
    if trace["status"] not in TRACE_STATUSES:
        raise ProofTaskError(f"trace.status must be one of: {', '.join(sorted(TRACE_STATUSES))}")
    if not isinstance(trace["task"], dict):
        raise ProofTaskError("trace.task must be an object")
    if not isinstance(trace["proof"], dict):
        raise ProofTaskError("trace.proof must be an object")
    task = validate_task(trace["task"])
    proof = validate_proof(trace["proof"])
    ensure_task_proof_match(task, proof)
    if trace["task_id"] != task["task_id"]:
        raise ProofTaskError(f"Trace/task mismatch: trace.task_id {trace['task_id']!r} != task.task_id {task['task_id']!r}")
    if trace["status"] != task["status"]:
        raise ProofTaskError(f"Trace/task status mismatch: trace.status {trace['status']!r} != task.status {task['status']!r}")
    events = trace["events"]
    if not isinstance(events, list) or not events:
        raise ProofTaskError("trace.events must be a non-empty list")
    for index, event in enumerate(events):
        if not isinstance(event, dict):
            raise ProofTaskError(f"trace.events[{index}] must be an object")
        require_fields(event, ["event_type", "status", "at", "actor"], f"trace.events[{index}]")
        for field in ["event_type", "status", "at", "actor"]:
            require_non_empty_string(event, field, f"trace.events[{index}]")
    if trace["status"] in FINAL_STATUSES:
        verification = trace.get("verification")
        if not isinstance(verification, dict):
            raise ProofTaskError("Final traces must include trace.verification")
        require_fields(verification, ["decision", "verifier", "verified_at"], "trace.verification")
        for field in ["decision", "verifier", "verified_at"]:
            require_non_empty_string(verification, field, "trace.verification")
        if verification["decision"] != trace["status"]:
            raise ProofTaskError(f"Verification decision mismatch: {verification['decision']!r} != trace.status {trace['status']!r}")
    elif "verification" in trace:
        raise ProofTaskError("Submitted traces must not include trace.verification yet")
    return trace


def validate_submitted_trace(trace: dict[str, Any]) -> dict[str, Any]:
    trace = validate_trace(trace)
    if trace["status"] != "submitted":
        raise ProofTaskError("Only traces with status 'submitted' can be verified")
    if trace["task"]["status"] != "submitted":
        raise ProofTaskError("trace.task.status must be 'submitted' before verification")
    return trace


def verify_trace(trace: dict[str, Any], decision: str, verifier: str, reason: str | None = None) -> dict[str, Any]:
    if decision not in FINAL_STATUSES:
        raise ProofTaskError("decision must be either 'verified' or 'rejected'")
    if not verifier.strip():
        raise ProofTaskError("verifier must be a non-empty string")
    verified_trace = deepcopy(validate_submitted_trace(trace))
    now = utc_now()
    verified_trace["status"] = decision
    verified_trace["updated_at"] = now
    verified_trace["task"]["status"] = decision
    verified_trace["verification"] = {"decision": decision, "verifier": verifier, "reason": reason or "", "verified_at": now}
    verified_trace["events"].append({"event_type": "task_verified" if decision == "verified" else "task_rejected", "status": decision, "at": now, "actor": verifier, "reason": reason or ""})
    return verified_trace


def get_nested_string(data: dict[str, Any], key: str, default: str = "") -> str:
    value = data.get(key, default)
    if value is None:
        return default
    return str(value)


def format_evidence_items(proof: dict[str, Any]) -> list[str]:
    evidence = proof.get("evidence") or []
    if not isinstance(evidence, list) or not evidence:
        return ["No evidence artifacts listed."]
    items: list[str] = []
    for item in evidence:
        if not isinstance(item, dict):
            continue
        evidence_type = get_nested_string(item, "type", "evidence")
        description = get_nested_string(item, "description", "")
        uri = get_nested_string(item, "uri", "")
        text = f"{evidence_type}: {description}" if description else evidence_type
        if uri:
            text = f"{text} ({uri})"
        items.append(text)
    return items or ["No readable evidence artifacts listed."]


def render_pr_comment(trace: dict[str, Any]) -> str:
    trace = validate_trace(trace)
    task = trace["task"]
    proof = trace["proof"]
    metadata = task.get("trace") if isinstance(task.get("trace"), dict) else {}
    verification = trace.get("verification") if isinstance(trace.get("verification"), dict) else {}

    status = trace["status"]
    decision = get_nested_string(verification, "decision", status)
    verifier = get_nested_string(verification, "verifier", "not verified yet")
    reason = get_nested_string(verification, "reason", "No verifier reason provided.")
    if not reason.strip():
        reason = "No verifier reason provided."

    if status == "verified":
        recommendation = "This PR can be considered for merge after normal code review and CI pass."
    elif status == "rejected":
        recommendation = "Do not merge this PR until the issues are fixed and verification is repeated."
    else:
        recommendation = "Verification is still pending. Do not use this trace as a merge approval yet."

    repository = get_nested_string(metadata, "repository", "unknown repository")
    pr_number = get_nested_string(metadata, "pull_request_number", "unknown")
    pr_title = get_nested_string(metadata, "pull_request_title", task["objective"])
    changed_area = get_nested_string(metadata, "changed_area", "not specified")
    risk_area = get_nested_string(metadata, "risk_area", "not specified")
    gate = get_nested_string(metadata, "verification_gate", "human verification")

    criteria = task.get("acceptance_criteria", [])
    proof_result = proof.get("result", "unknown")
    evidence_items = format_evidence_items(proof)

    lines = [
        f"## ProofTask result: {status}",
        "",
        f"Verification trace `{trace['trace_id']}` is linked to task `{trace['task_id']}`.",
        "",
        "### PR context",
        "",
        f"- Repository: `{repository}`",
        f"- Pull request: `#{pr_number} - {pr_title}`",
        f"- Changed area: `{changed_area}`",
        f"- Risk area: `{risk_area}`",
        f"- Verification gate: `{gate}`",
        "",
        "### What was checked",
        "",
    ]
    lines.extend(f"- {criterion}" for criterion in criteria)
    lines.extend([
        "",
        "### Proof submitted",
        "",
        f"- Proof ID: `{proof.get('proof_id', '')}`",
        f"- Submitted by: `{proof.get('submitted_by', '')}`",
        f"- Result: `{proof_result}`",
    ])
    lines.extend(f"- Evidence: {item}" for item in evidence_items)
    lines.extend([
        "",
        "### Verifier decision",
        "",
        f"- Decision: `{decision}`",
        f"- Verifier: `{verifier}`",
        f"- Reason: {reason}",
        "",
        "### Recommendation",
        "",
        recommendation,
        "",
        "ProofTask adds structured human proof. It does not replace code review or automated tests.",
    ])
    return "\n".join(lines) + "\n"


def ledger_metadata_path(ledger: str | Path) -> Path:
    return Path(ledger) / "ledger.json"


def ledger_events_path(ledger: str | Path) -> Path:
    return Path(ledger) / "events.jsonl"


def ledger_task_path(ledger: str | Path, task_id: str) -> Path:
    return Path(ledger) / "tasks" / f"{task_id}.json"


def ledger_proof_path(ledger: str | Path, proof_id: str) -> Path:
    return Path(ledger) / "proofs" / f"{proof_id}.json"


def ledger_trace_path(ledger: str | Path, trace_id: str) -> Path:
    return Path(ledger) / "traces" / f"{trace_id}.json"


def ledger_dir_path(ledger: str | Path, name: str) -> Path:
    return Path(ledger) / name


def append_ledger_event(ledger: str | Path, event: dict[str, Any]) -> None:
    event_record = {"event_id": f"event_{uuid.uuid4().hex[:12]}", "at": utc_now(), **event}
    events_path = ledger_events_path(ledger)
    events_path.parent.mkdir(parents=True, exist_ok=True)
    with events_path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(event_record, ensure_ascii=False) + "\n")


def init_ledger(ledger: str | Path, force: bool = False) -> dict[str, Any]:
    ledger_path = Path(ledger)
    ledger_path.mkdir(parents=True, exist_ok=True)
    for name in LEDGER_DIRS:
        ledger_dir_path(ledger_path, name).mkdir(parents=True, exist_ok=True)
    metadata_path = ledger_metadata_path(ledger_path)
    if metadata_path.exists() and not force:
        metadata = read_json(metadata_path)
        validate_ledger_metadata(metadata)
        return metadata
    metadata = {"ledger_version": LEDGER_VERSION, "created_at": utc_now(), "updated_at": utc_now(), "directories": list(LEDGER_DIRS)}
    write_json(metadata_path, metadata)
    append_ledger_event(ledger_path, {"event_type": "ledger_initialized", "actor": "prooftask", "status": "ready"})
    return metadata


def validate_ledger_metadata(metadata: dict[str, Any]) -> dict[str, Any]:
    require_fields(metadata, ["ledger_version", "created_at", "updated_at", "directories"], "ledger")
    for field in ["ledger_version", "created_at", "updated_at"]:
        require_non_empty_string(metadata, field, "ledger")
    if not isinstance(metadata["directories"], list):
        raise ProofTaskError("ledger.directories must be a list")
    return metadata


def ensure_ledger(ledger: str | Path) -> Path:
    ledger_path = Path(ledger)
    metadata_path = ledger_metadata_path(ledger_path)
    if not metadata_path.exists():
        raise ProofTaskError(f"Ledger not initialized: {ledger_path}. Run init-ledger first.")
    validate_ledger_metadata(read_json(metadata_path))
    for name in LEDGER_DIRS:
        directory = ledger_dir_path(ledger_path, name)
        if not directory.is_dir():
            raise ProofTaskError(f"Ledger directory missing: {directory}")
    return ledger_path


def update_ledger_timestamp(ledger: str | Path) -> None:
    metadata_path = ledger_metadata_path(ledger)
    metadata = read_json(metadata_path)
    metadata["updated_at"] = utc_now()
    write_json(metadata_path, metadata)


def ledger_add_task(ledger: str | Path, task: dict[str, Any], overwrite: bool = False) -> Path:
    ledger_path = ensure_ledger(ledger)
    task = validate_task(task)
    destination = ledger_task_path(ledger_path, task["task_id"])
    if destination.exists() and not overwrite:
        raise ProofTaskError(f"Task already exists in ledger: {task['task_id']}")
    write_json(destination, task)
    append_ledger_event(ledger_path, {"event_type": "task_added", "actor": task["created_by"], "task_id": task["task_id"], "status": task["status"], "path": str(destination)})
    update_ledger_timestamp(ledger_path)
    return destination


def ledger_list_tasks(ledger: str | Path, status: str | None = None) -> list[dict[str, Any]]:
    ledger_path = ensure_ledger(ledger)
    tasks = []
    for task_file in sorted(ledger_dir_path(ledger_path, "tasks").glob("*.json")):
        task = validate_task(read_json(task_file))
        if status is None or task["status"] == status:
            tasks.append(task)
    return tasks


def ledger_inspect_task(ledger: str | Path, task_id: str) -> dict[str, Any]:
    ledger_path = ensure_ledger(ledger)
    path = ledger_task_path(ledger_path, task_id)
    if not path.exists():
        raise ProofTaskError(f"Task not found in ledger: {task_id}")
    return validate_task(read_json(path))


def ledger_submit_proof(ledger: str | Path, task_id: str, proof: dict[str, Any], overwrite: bool = False) -> tuple[Path, Path]:
    ledger_path = ensure_ledger(ledger)
    task = ledger_inspect_task(ledger_path, task_id)
    proof = validate_proof(proof)
    ensure_task_proof_match(task, proof)
    proof_path = ledger_proof_path(ledger_path, proof["proof_id"])
    if proof_path.exists() and not overwrite:
        raise ProofTaskError(f"Proof already exists in ledger: {proof['proof_id']}")
    trace = create_submitted_trace(task, proof)
    trace_path = ledger_trace_path(ledger_path, trace["trace_id"])
    write_json(proof_path, proof)
    write_json(trace_path, trace)
    write_json(ledger_task_path(ledger_path, task_id), trace["task"])
    append_ledger_event(ledger_path, {"event_type": "proof_submitted", "actor": proof["submitted_by"], "task_id": task_id, "proof_id": proof["proof_id"], "trace_id": trace["trace_id"], "status": "submitted", "proof_path": str(proof_path), "trace_path": str(trace_path)})
    update_ledger_timestamp(ledger_path)
    return proof_path, trace_path


def ledger_verify(ledger: str | Path, trace_id: str, decision: str, verifier: str, reason: str | None = None) -> Path:
    ledger_path = ensure_ledger(ledger)
    trace_path = ledger_trace_path(ledger_path, trace_id)
    if not trace_path.exists():
        raise ProofTaskError(f"Trace not found in ledger: {trace_id}")
    trace = validate_submitted_trace(read_json(trace_path))
    final_trace = verify_trace(trace, decision, verifier, reason)
    write_json(trace_path, final_trace)
    write_json(ledger_task_path(ledger_path, final_trace["task_id"]), final_trace["task"])
    append_ledger_event(ledger_path, {"event_type": "trace_verified" if decision == "verified" else "trace_rejected", "actor": verifier, "task_id": final_trace["task_id"], "trace_id": trace_id, "status": decision, "path": str(trace_path), "reason": reason or ""})
    update_ledger_timestamp(ledger_path)
    return trace_path


def ledger_list_traces(ledger: str | Path, status: str | None = None) -> list[dict[str, Any]]:
    ledger_path = ensure_ledger(ledger)
    traces = []
    for trace_file in sorted(ledger_dir_path(ledger_path, "traces").glob("*.json")):
        trace = validate_trace(read_json(trace_file))
        if status is None or trace["status"] == status:
            traces.append(trace)
    return traces


def ledger_inspect_trace(ledger: str | Path, trace_id: str) -> dict[str, Any]:
    ledger_path = ensure_ledger(ledger)
    path = ledger_trace_path(ledger_path, trace_id)
    if not path.exists():
        raise ProofTaskError(f"Trace not found in ledger: {trace_id}")
    return validate_trace(read_json(path))


def print_tasks_table(tasks: list[dict[str, Any]]) -> None:
    if not tasks:
        print("No tasks found")
        return
    print("task_id\tstatus\ttask_type\tcreated_by\tobjective")
    for task in tasks:
        objective = task["objective"].replace("\t", " ").replace("\n", " ")
        print(f"{task['task_id']}\t{task['status']}\t{task['task_type']}\t{task['created_by']}\t{objective}")


def print_traces_table(traces: list[dict[str, Any]]) -> None:
    if not traces:
        print("No traces found")
        return
    print("trace_id\ttask_id\tstatus\tproof_id\tupdated_at")
    for trace in traces:
        proof_id = trace["proof"].get("proof_id", "")
        print(f"{trace['trace_id']}\t{trace['task_id']}\t{trace['status']}\t{proof_id}\t{trace['updated_at']}")


def cmd_create_task(args: argparse.Namespace) -> int:
    task = create_task(task_type=args.task_type, created_by=args.created_by, objective=args.objective, acceptance_criteria=args.acceptance, proof_required=args.proof, task_id=args.task_id, payment_amount=args.payment_amount, payment_currency=args.payment_currency, payment_status=args.payment_status, trace_reason=args.trace_reason, trace_source=args.trace_source)
    write_json(args.out, task)
    print(f"OK created task: {task['task_id']} -> {args.out}")
    return 0


def cmd_validate_task(args: argparse.Namespace) -> int:
    task = validate_task(read_json(args.path))
    print(f"OK task: {task['task_id']} status={task['status']}")
    return 0


def cmd_validate_proof(args: argparse.Namespace) -> int:
    proof = validate_proof(read_json(args.path))
    print(f"OK proof: {proof['proof_id']} task={proof['task_id']} result={proof['result']}")
    return 0


def cmd_validate_trace(args: argparse.Namespace) -> int:
    trace = validate_trace(read_json(args.path))
    print(f"OK trace: {trace['trace_id']} task={trace['task_id']} status={trace['status']}")
    return 0


def cmd_submit_proof(args: argparse.Namespace) -> int:
    task = validate_task(read_json(args.task))
    proof = validate_proof(read_json(args.proof))
    trace = create_submitted_trace(task, proof)
    write_json(args.out, trace)
    print(f"OK submitted: {trace['trace_id']} -> {args.out}")
    return 0


def cmd_verify(args: argparse.Namespace) -> int:
    trace = validate_submitted_trace(read_json(args.trace))
    verified_trace = verify_trace(trace, args.decision, args.verifier, args.reason)
    write_json(args.out, verified_trace)
    print(f"OK {args.decision}: {verified_trace['trace_id']} -> {args.out}")
    return 0


def cmd_render_pr_comment(args: argparse.Namespace) -> int:
    comment = render_pr_comment(read_json(args.trace))
    if args.out:
        write_text(args.out, comment)
        print(f"OK PR comment: {args.out}")
    else:
        print(comment, end="")
    return 0


def cmd_init_ledger(args: argparse.Namespace) -> int:
    metadata = init_ledger(args.ledger, force=args.force)
    print(f"OK ledger: {args.ledger} version={metadata['ledger_version']}")
    return 0


def cmd_ledger_add_task(args: argparse.Namespace) -> int:
    task = validate_task(read_json(args.task))
    destination = ledger_add_task(args.ledger, task, overwrite=args.overwrite)
    print(f"OK ledger task added: {task['task_id']} -> {destination}")
    return 0


def cmd_ledger_submit_proof(args: argparse.Namespace) -> int:
    proof = validate_proof(read_json(args.proof))
    _, trace_path = ledger_submit_proof(args.ledger, args.task_id, proof, overwrite=args.overwrite)
    trace = validate_trace(read_json(trace_path))
    print(f"OK ledger proof submitted: proof={proof['proof_id']} task={args.task_id} trace={trace['trace_id']} -> {trace_path}")
    return 0


def cmd_ledger_verify(args: argparse.Namespace) -> int:
    trace_path = ledger_verify(args.ledger, args.trace_id, args.decision, args.verifier, args.reason)
    trace = validate_trace(read_json(trace_path))
    print(f"OK ledger {args.decision}: {trace['trace_id']} -> {trace_path}")
    return 0


def cmd_list_tasks(args: argparse.Namespace) -> int:
    tasks = ledger_list_tasks(args.ledger, status=args.status)
    print(json.dumps(tasks, indent=2, ensure_ascii=False) if args.json else None) if args.json else print_tasks_table(tasks)
    return 0


def cmd_inspect_task(args: argparse.Namespace) -> int:
    print(json.dumps(ledger_inspect_task(args.ledger, args.task_id), indent=2, ensure_ascii=False))
    return 0


def cmd_list_traces(args: argparse.Namespace) -> int:
    traces = ledger_list_traces(args.ledger, status=args.status)
    print(json.dumps(traces, indent=2, ensure_ascii=False) if args.json else None) if args.json else print_traces_table(traces)
    return 0


def cmd_inspect_trace(args: argparse.Namespace) -> int:
    print(json.dumps(ledger_inspect_trace(args.ledger, args.trace_id), indent=2, ensure_ascii=False))
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="prooftask", description="ProofTask MVP CLI for task/proof validation and verification traces.")
    subcommands = parser.add_subparsers(dest="command", required=True)

    create_task_parser = subcommands.add_parser("create-task", help="Create a task JSON file")
    create_task_parser.add_argument("--type", dest="task_type", required=True, help="Task type, for example manual_qa_check")
    create_task_parser.add_argument("--created-by", required=True, help="Requester identifier")
    create_task_parser.add_argument("--objective", required=True, help="Human-readable task objective")
    create_task_parser.add_argument("--acceptance", action="append", required=True, help="Acceptance criterion. Can be passed multiple times.")
    create_task_parser.add_argument("--proof", action="append", required=True, help="Required proof item. Can be passed multiple times.")
    create_task_parser.add_argument("--task-id", help="Optional explicit task ID")
    create_task_parser.add_argument("--payment-amount", type=float, help="Optional payment amount")
    create_task_parser.add_argument("--payment-currency", default="USD", help="Payment currency when payment amount is set")
    create_task_parser.add_argument("--payment-status", default="pending", choices=sorted(PAYMENT_STATUSES), help="Payment status when payment amount is set")
    create_task_parser.add_argument("--trace-reason", help="Optional causal reason for task creation")
    create_task_parser.add_argument("--trace-source", help="Optional source metadata for task creation")
    create_task_parser.add_argument("--out", required=True, help="Output path for task JSON")
    create_task_parser.set_defaults(func=cmd_create_task)

    validate_task_parser = subcommands.add_parser("validate-task", help="Validate a task JSON file")
    validate_task_parser.add_argument("path", help="Path to task JSON")
    validate_task_parser.set_defaults(func=cmd_validate_task)

    validate_proof_parser = subcommands.add_parser("validate-proof", help="Validate a proof JSON file")
    validate_proof_parser.add_argument("path", help="Path to proof JSON")
    validate_proof_parser.set_defaults(func=cmd_validate_proof)

    validate_trace_parser = subcommands.add_parser("validate-trace", help="Validate a trace JSON file")
    validate_trace_parser.add_argument("path", help="Path to trace JSON")
    validate_trace_parser.set_defaults(func=cmd_validate_trace)

    submit_parser = subcommands.add_parser("submit-proof", help="Create a submitted trace from a task JSON and proof JSON")
    submit_parser.add_argument("--task", required=True, help="Path to task JSON")
    submit_parser.add_argument("--proof", required=True, help="Path to proof JSON")
    submit_parser.add_argument("--out", required=True, help="Output path for submitted trace JSON")
    submit_parser.set_defaults(func=cmd_submit_proof)

    verify_parser = subcommands.add_parser("verify", help="Verify or reject a submitted trace")
    verify_parser.add_argument("--trace", required=True, help="Path to submitted trace JSON")
    verify_parser.add_argument("--decision", required=True, choices=sorted(FINAL_STATUSES))
    verify_parser.add_argument("--verifier", required=True, help="Verifier identifier")
    verify_parser.add_argument("--reason", default="", help="Optional verification reason")
    verify_parser.add_argument("--out", required=True, help="Output path for final trace JSON")
    verify_parser.set_defaults(func=cmd_verify)

    render_pr_comment_parser = subcommands.add_parser("render-pr-comment", help="Render a PR-ready markdown comment from a trace JSON file")
    render_pr_comment_parser.add_argument("--trace", required=True, help="Path to trace JSON")
    render_pr_comment_parser.add_argument("--out", help="Optional output path for markdown comment. Prints to stdout when omitted.")
    render_pr_comment_parser.set_defaults(func=cmd_render_pr_comment)

    init_ledger_parser = subcommands.add_parser("init-ledger", help="Initialize a local ProofTask ledger")
    init_ledger_parser.add_argument("--ledger", default=".prooftask", help="Ledger directory")
    init_ledger_parser.add_argument("--force", action="store_true", help="Overwrite ledger metadata")
    init_ledger_parser.set_defaults(func=cmd_init_ledger)

    ledger_add_task_parser = subcommands.add_parser("ledger-add-task", help="Add a task JSON file to a local ledger")
    ledger_add_task_parser.add_argument("--ledger", default=".prooftask", help="Ledger directory")
    ledger_add_task_parser.add_argument("--task", required=True, help="Path to task JSON")
    ledger_add_task_parser.add_argument("--overwrite", action="store_true", help="Overwrite existing task with same ID")
    ledger_add_task_parser.set_defaults(func=cmd_ledger_add_task)

    ledger_submit_proof_parser = subcommands.add_parser("ledger-submit-proof", help="Submit proof for a ledger task and store proof + trace")
    ledger_submit_proof_parser.add_argument("--ledger", default=".prooftask", help="Ledger directory")
    ledger_submit_proof_parser.add_argument("--task-id", required=True, help="Task ID in the ledger")
    ledger_submit_proof_parser.add_argument("--proof", required=True, help="Path to proof JSON")
    ledger_submit_proof_parser.add_argument("--overwrite", action="store_true", help="Overwrite existing proof with same ID")
    ledger_submit_proof_parser.set_defaults(func=cmd_ledger_submit_proof)

    ledger_verify_parser = subcommands.add_parser("ledger-verify", help="Verify or reject a submitted trace stored in a local ledger")
    ledger_verify_parser.add_argument("--ledger", default=".prooftask", help="Ledger directory")
    ledger_verify_parser.add_argument("--trace-id", required=True, help="Trace ID in the ledger")
    ledger_verify_parser.add_argument("--decision", required=True, choices=sorted(FINAL_STATUSES))
    ledger_verify_parser.add_argument("--verifier", required=True, help="Verifier identifier")
    ledger_verify_parser.add_argument("--reason", default="", help="Optional verification reason")
    ledger_verify_parser.set_defaults(func=cmd_ledger_verify)

    list_tasks_parser = subcommands.add_parser("list-tasks", help="List tasks stored in a local ledger")
    list_tasks_parser.add_argument("--ledger", default=".prooftask", help="Ledger directory")
    list_tasks_parser.add_argument("--status", choices=sorted(TASK_STATUSES), help="Optional task status filter")
    list_tasks_parser.add_argument("--json", action="store_true", help="Output JSON instead of table text")
    list_tasks_parser.set_defaults(func=cmd_list_tasks)

    inspect_task_parser = subcommands.add_parser("inspect-task", help="Inspect one task stored in a local ledger")
    inspect_task_parser.add_argument("--ledger", default=".prooftask", help="Ledger directory")
    inspect_task_parser.add_argument("--task-id", required=True, help="Task ID to inspect")
    inspect_task_parser.set_defaults(func=cmd_inspect_task)

    list_traces_parser = subcommands.add_parser("list-traces", help="List traces stored in a local ledger")
    list_traces_parser.add_argument("--ledger", default=".prooftask", help="Ledger directory")
    list_traces_parser.add_argument("--status", choices=sorted(TRACE_STATUSES), help="Optional trace status filter")
    list_traces_parser.add_argument("--json", action="store_true", help="Output JSON instead of table text")
    list_traces_parser.set_defaults(func=cmd_list_traces)

    inspect_trace_parser = subcommands.add_parser("inspect-trace", help="Inspect one trace stored in a local ledger")
    inspect_trace_parser.add_argument("--ledger", default=".prooftask", help="Ledger directory")
    inspect_trace_parser.add_argument("--trace-id", required=True, help="Trace ID to inspect")
    inspect_trace_parser.set_defaults(func=cmd_inspect_trace)

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        return args.func(args)
    except ProofTaskError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
