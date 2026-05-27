#!/usr/bin/env python3
"""ProofTask CLI.

A tiny, dependency-free CLI for the first ProofTask MVP:

- validate a task JSON file
- validate a human proof JSON file
- validate a verification trace JSON file
- create a submitted trace from task + proof
- verify or reject the submitted trace

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


class ProofTaskError(ValueError):
    """Raised when an input file is not valid for the MVP flow."""


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z")


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


def validate_task(task: dict[str, Any]) -> dict[str, Any]:
    require_fields(
        task,
        [
            "task_id",
            "created_by",
            "task_type",
            "objective",
            "acceptance_criteria",
            "proof_required",
            "status",
        ],
        "task",
    )

    for field in ["task_id", "created_by", "task_type", "objective", "status"]:
        require_non_empty_string(task, field, "task")

    require_string_list(task, "acceptance_criteria", "task")
    require_string_list(task, "proof_required", "task")

    if task["status"] not in TASK_STATUSES:
        raise ProofTaskError(
            f"task.status must be one of: {', '.join(sorted(TASK_STATUSES))}"
        )

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

        if "status" in payment and payment["status"] not in PAYMENT_STATUSES:
            raise ProofTaskError(
                "task.payment.status must be one of: "
                + ", ".join(sorted(PAYMENT_STATUSES))
            )

    trace = task.get("trace")
    if trace is not None and not isinstance(trace, dict):
        raise ProofTaskError("task.trace must be an object when present")

    return task


def validate_proof(proof: dict[str, Any]) -> dict[str, Any]:
    require_fields(
        proof,
        ["proof_id", "task_id", "submitted_by", "result", "report", "submitted_at"],
        "proof",
    )

    for field in ["proof_id", "task_id", "submitted_by", "result", "report", "submitted_at"]:
        require_non_empty_string(proof, field, "proof")

    if proof["result"] not in PROOF_RESULTS:
        raise ProofTaskError(
            f"proof.result must be one of: {', '.join(sorted(PROOF_RESULTS))}"
        )

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
                raise ProofTaskError(
                    f"proof.evidence[{index}].type must be one of: "
                    + ", ".join(sorted(EVIDENCE_TYPES))
                )

    environment = proof.get("environment")
    if environment is not None and not isinstance(environment, dict):
        raise ProofTaskError("proof.environment must be an object when present")

    return proof


def ensure_task_proof_match(task: dict[str, Any], proof: dict[str, Any]) -> None:
    if task["task_id"] != proof["task_id"]:
        raise ProofTaskError(
            f"Task/proof mismatch: task_id {task['task_id']!r} != {proof['task_id']!r}"
        )


def create_submitted_trace(task: dict[str, Any], proof: dict[str, Any]) -> dict[str, Any]:
    ensure_task_proof_match(task, proof)

    if task["status"] not in SUBMIT_ALLOWED_STATUSES:
        raise ProofTaskError(
            "Task can be submitted only from status: "
            + ", ".join(sorted(SUBMIT_ALLOWED_STATUSES))
        )

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
            {
                "event_type": "task_loaded",
                "status": task["status"],
                "at": now,
                "actor": task["created_by"],
            },
            {
                "event_type": "proof_submitted",
                "status": "submitted",
                "at": now,
                "actor": proof["submitted_by"],
                "proof_id": proof["proof_id"],
                "result": proof["result"],
            },
        ],
    }


def validate_trace(trace: dict[str, Any]) -> dict[str, Any]:
    require_fields(
        trace,
        ["trace_id", "task_id", "status", "created_at", "updated_at", "task", "proof", "events"],
        "trace",
    )

    for field in ["trace_id", "task_id", "status", "created_at", "updated_at"]:
        require_non_empty_string(trace, field, "trace")

    if trace["status"] not in TRACE_STATUSES:
        raise ProofTaskError(
            f"trace.status must be one of: {', '.join(sorted(TRACE_STATUSES))}"
        )

    if not isinstance(trace["task"], dict):
        raise ProofTaskError("trace.task must be an object")

    if not isinstance(trace["proof"], dict):
        raise ProofTaskError("trace.proof must be an object")

    task = validate_task(trace["task"])
    proof = validate_proof(trace["proof"])
    ensure_task_proof_match(task, proof)

    if trace["task_id"] != task["task_id"]:
        raise ProofTaskError(
            f"Trace/task mismatch: trace.task_id {trace['task_id']!r} != {task['task_id']!r}"
        )

    if trace["status"] != task["status"]:
        raise ProofTaskError(
            f"Trace/task status mismatch: trace.status {trace['status']!r} != task.status {task['status']!r}"
        )

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
            raise ProofTaskError(
                f"Verification decision mismatch: {verification['decision']!r} != trace.status {trace['status']!r}"
            )
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


def verify_trace(
    trace: dict[str, Any],
    decision: str,
    verifier: str,
    reason: str | None = None,
) -> dict[str, Any]:
    if decision not in FINAL_STATUSES:
        raise ProofTaskError("decision must be either 'verified' or 'rejected'")

    if not verifier.strip():
        raise ProofTaskError("verifier must be a non-empty string")

    verified_trace = deepcopy(validate_submitted_trace(trace))
    now = utc_now()

    verified_trace["status"] = decision
    verified_trace["updated_at"] = now
    verified_trace["task"]["status"] = decision
    verified_trace["verification"] = {
        "decision": decision,
        "verifier": verifier,
        "reason": reason or "",
        "verified_at": now,
    }
    verified_trace["events"].append(
        {
            "event_type": "task_verified" if decision == "verified" else "task_rejected",
            "status": decision,
            "at": now,
            "actor": verifier,
            "reason": reason or "",
        }
    )

    return verified_trace


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


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="prooftask",
        description="ProofTask MVP CLI for task/proof validation and verification traces.",
    )
    subcommands = parser.add_subparsers(dest="command", required=True)

    validate_task_parser = subcommands.add_parser("validate-task", help="Validate a task JSON file")
    validate_task_parser.add_argument("path", help="Path to task JSON")
    validate_task_parser.set_defaults(func=cmd_validate_task)

    validate_proof_parser = subcommands.add_parser("validate-proof", help="Validate a proof JSON file")
    validate_proof_parser.add_argument("path", help="Path to proof JSON")
    validate_proof_parser.set_defaults(func=cmd_validate_proof)

    validate_trace_parser = subcommands.add_parser("validate-trace", help="Validate a trace JSON file")
    validate_trace_parser.add_argument("path", help="Path to trace JSON")
    validate_trace_parser.set_defaults(func=cmd_validate_trace)

    submit_parser = subcommands.add_parser(
        "submit-proof",
        help="Create a submitted trace from a task JSON and proof JSON",
    )
    submit_parser.add_argument("--task", required=True, help="Path to task JSON")
    submit_parser.add_argument("--proof", required=True, help="Path to proof JSON")
    submit_parser.add_argument("--out", required=True, help="Output path for submitted trace JSON")
    submit_parser.set_defaults(func=cmd_submit_proof)

    verify_parser = subcommands.add_parser(
        "verify",
        help="Verify or reject a submitted trace",
    )
    verify_parser.add_argument("--trace", required=True, help="Path to submitted trace JSON")
    verify_parser.add_argument("--decision", required=True, choices=sorted(FINAL_STATUSES))
    verify_parser.add_argument("--verifier", required=True, help="Verifier identifier")
    verify_parser.add_argument("--reason", default="", help="Optional verification reason")
    verify_parser.add_argument("--out", required=True, help="Output path for final trace JSON")
    verify_parser.set_defaults(func=cmd_verify)

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
