# ProofTask Demo Walkthrough

This demo shows the smallest useful ProofTask lifecycle:

```text
agent task → human proof → submitted trace → verified trace
```

The demo uses the local dependency-free CLI in `prooftask.py`.

## 1. Validate the task

```bash
python prooftask.py validate-task examples/manual_qa_task.json
```

Expected output:

```text
OK task: task_001 status=created
```

## 2. Validate the human proof

```bash
python prooftask.py validate-proof examples/manual_qa_proof.json
```

Expected output:

```text
OK proof: proof_001 task=task_001 result=pass
```

## 3. Submit proof and create a trace

```bash
python prooftask.py submit-proof \
  --task examples/manual_qa_task.json \
  --proof examples/manual_qa_proof.json \
  --out examples/submitted_trace.json
```

This creates a submitted trace containing:

- embedded task snapshot
- embedded proof snapshot
- trace status: `submitted`
- initial event log

## 4. Validate the submitted trace

```bash
python prooftask.py validate-trace examples/submitted_trace.json
```

Expected output:

```text
OK trace: trace_<id> task=task_001 status=submitted
```

## 5. Verify the trace

```bash
python prooftask.py verify \
  --trace examples/submitted_trace.json \
  --decision verified \
  --verifier verifier_demo_001 \
  --reason "All acceptance criteria passed." \
  --out examples/verified_trace.json
```

This creates a final trace containing:

- trace status: `verified`
- task status: `verified`
- verification decision
- verifier identifier
- verification reason
- appended verification event

## 6. Validate the final trace

```bash
python prooftask.py validate-trace examples/verified_trace.json
```

Expected output:

```text
OK trace: trace_<id> task=task_001 status=verified
```

## Negative fixtures

ProofTask also includes intentionally invalid fixtures.

### Mismatched proof

This proof references the wrong `task_id`:

```bash
python prooftask.py submit-proof \
  --task examples/manual_qa_task.json \
  --proof examples/invalid_mismatched_proof.json \
  --out examples/should_not_exist.json
```

Expected behavior: command fails with exit code `2`.

### Invalid final trace

This final trace is marked `verified` but does not include a `verification` object:

```bash
python prooftask.py validate-trace examples/invalid_final_trace.json
```

Expected behavior: command fails with exit code `2`.

## What this proves

This demo proves the first ProofTask primitive:

> An agent-created task and a human proof submission can be converted into a traceable verification artifact.

That artifact can be accepted, rejected, stored, inspected, and later used by a larger agentic workflow.
