import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CLI = [sys.executable, str(ROOT / "prooftask.py")]
TASK = ROOT / "examples" / "manual_qa_task.json"
PROOF = ROOT / "examples" / "manual_qa_proof.json"
INVALID_PROOF = ROOT / "examples" / "invalid_mismatched_proof.json"
INVALID_TRACE = ROOT / "examples" / "invalid_final_trace.json"


def run_cli(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [*CLI, *args],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )


def test_create_task_generates_valid_task(tmp_path: Path) -> None:
    generated_task = tmp_path / "generated_task.json"

    create_result = run_cli(
        "create-task",
        "--type",
        "manual_qa_check",
        "--created-by",
        "agent_demo_001",
        "--objective",
        "Verify signup flow on mobile Chrome",
        "--acceptance",
        "Open signup page",
        "--acceptance",
        "Submit valid test data",
        "--proof",
        "screenshot",
        "--proof",
        "short written report",
        "--payment-amount",
        "5",
        "--trace-reason",
        "AI coding agent changed signup flow before release.",
        "--trace-source",
        "pytest",
        "--out",
        str(generated_task),
    )
    assert create_result.returncode == 0, create_result.stderr
    assert "OK created task" in create_result.stdout

    validate_result = run_cli("validate-task", str(generated_task))
    assert validate_result.returncode == 0, validate_result.stderr

    task = json.loads(generated_task.read_text(encoding="utf-8"))
    assert task["task_id"].startswith("task_")
    assert task["created_by"] == "agent_demo_001"
    assert task["task_type"] == "manual_qa_check"
    assert task["status"] == "created"
    assert task["payment"]["amount"] == 5
    assert task["payment"]["currency"] == "USD"
    assert task["trace"]["source"] == "pytest"


def test_create_task_with_explicit_task_id_can_enter_full_flow(tmp_path: Path) -> None:
    generated_task = tmp_path / "generated_task.json"
    generated_proof = tmp_path / "generated_proof.json"
    submitted_trace = tmp_path / "submitted_trace.json"
    verified_trace = tmp_path / "verified_trace.json"

    create_result = run_cli(
        "create-task",
        "--task-id",
        "task_generated_001",
        "--type",
        "manual_qa_check",
        "--created-by",
        "agent_demo_001",
        "--objective",
        "Verify generated task flow",
        "--acceptance",
        "Open test page",
        "--proof",
        "screenshot",
        "--out",
        str(generated_task),
    )
    assert create_result.returncode == 0, create_result.stderr

    proof = json.loads(PROOF.read_text(encoding="utf-8"))
    proof["task_id"] = "task_generated_001"
    generated_proof.write_text(json.dumps(proof), encoding="utf-8")

    submit_result = run_cli(
        "submit-proof",
        "--task",
        str(generated_task),
        "--proof",
        str(generated_proof),
        "--out",
        str(submitted_trace),
    )
    assert submit_result.returncode == 0, submit_result.stderr

    verify_result = run_cli(
        "verify",
        "--trace",
        str(submitted_trace),
        "--decision",
        "verified",
        "--verifier",
        "pytest_verifier",
        "--out",
        str(verified_trace),
    )
    assert verify_result.returncode == 0, verify_result.stderr

    validate_result = run_cli("validate-trace", str(verified_trace))
    assert validate_result.returncode == 0, validate_result.stderr


def test_create_task_rejects_negative_payment(tmp_path: Path) -> None:
    out = tmp_path / "invalid_task.json"
    result = run_cli(
        "create-task",
        "--type",
        "manual_qa_check",
        "--created-by",
        "agent_demo_001",
        "--objective",
        "Invalid payment task",
        "--acceptance",
        "Do something",
        "--proof",
        "screenshot",
        "--payment-amount",
        "-1",
        "--out",
        str(out),
    )

    assert result.returncode == 2
    assert "task.payment.amount must be >= 0" in result.stderr
    assert not out.exists()


def test_validate_examples() -> None:
    task_result = run_cli("validate-task", str(TASK))
    assert task_result.returncode == 0, task_result.stderr
    assert "OK task" in task_result.stdout

    proof_result = run_cli("validate-proof", str(PROOF))
    assert proof_result.returncode == 0, proof_result.stderr
    assert "OK proof" in proof_result.stdout


def test_full_verification_flow(tmp_path: Path) -> None:
    submitted_trace = tmp_path / "submitted_trace.json"
    verified_trace = tmp_path / "verified_trace.json"

    submit_result = run_cli(
        "submit-proof",
        "--task",
        str(TASK),
        "--proof",
        str(PROOF),
        "--out",
        str(submitted_trace),
    )
    assert submit_result.returncode == 0, submit_result.stderr

    validate_submitted_result = run_cli("validate-trace", str(submitted_trace))
    assert validate_submitted_result.returncode == 0, validate_submitted_result.stderr

    verify_result = run_cli(
        "verify",
        "--trace",
        str(submitted_trace),
        "--decision",
        "verified",
        "--verifier",
        "pytest_verifier",
        "--reason",
        "All checks passed.",
        "--out",
        str(verified_trace),
    )
    assert verify_result.returncode == 0, verify_result.stderr

    validate_verified_result = run_cli("validate-trace", str(verified_trace))
    assert validate_verified_result.returncode == 0, validate_verified_result.stderr

    trace = json.loads(verified_trace.read_text(encoding="utf-8"))
    assert trace["status"] == "verified"
    assert trace["task"]["status"] == "verified"
    assert trace["verification"]["decision"] == "verified"
    assert len(trace["events"]) >= 3


def test_rejects_mismatched_proof(tmp_path: Path) -> None:
    out = tmp_path / "should_not_exist.json"
    result = run_cli(
        "submit-proof",
        "--task",
        str(TASK),
        "--proof",
        str(INVALID_PROOF),
        "--out",
        str(out),
    )

    assert result.returncode == 2
    assert "Task/proof mismatch" in result.stderr
    assert not out.exists()


def test_rejects_invalid_final_trace() -> None:
    result = run_cli("validate-trace", str(INVALID_TRACE))

    assert result.returncode == 2
    assert "Final traces must include trace.verification" in result.stderr
