# ProofTask Demo Walkthrough

This demo shows the smallest useful ProofTask lifecycle:

```text
agent task → human proof → submitted trace → verified trace
```

The demo uses the local CLI. You can run it directly with `python prooftask.py` or install it locally and use `prooftask`.

```bash
python -m pip install -e .
```

## 1. Create an agent-facing QA task

```bash
prooftask create-task \
  --task-id task_generated_001 \
  --type manual_qa_check \
  --created-by agent_demo_001 \
  --objective "Verify signup flow on mobile Chrome" \
  --acceptance "Open signup page" \
  --acceptance "Submit valid test data" \
  --proof "screenshot" \
  --proof "short written report" \
  --payment-amount 5 \
  --trace-reason "AI coding agent changed signup flow before release." \
  --trace-source demo \
  --out examples/generated_task.json
```

Expected output:

```text
OK created task: task_generated_001 -> examples/generated_task.json
```

## 2. Validate the task

```bash
prooftask validate-task examples/manual_qa_task.json
```

Expected output:

```text
OK task: task_001 status=created
```

## 3. Validate the human proof

```bash
prooftask validate-proof examples/manual_qa_proof.json
```

Expected output:

```text
OK proof: proof_001 task=task_001 result=pass
```

## 4. Submit proof and create a trace

```bash
prooftask submit-proof \
  --task examples/manual_qa_task.json \
  --proof examples/manual_qa_proof.json \
  --out examples/submitted_trace.json
```

This creates a submitted trace containing:

- embedded task snapshot
- embedded proof snapshot
- trace status: `submitted`
- initial event log

## 5. Validate the submitted trace

```bash
prooftask validate-trace examples/submitted_trace.json
```

Expected output:

```text
OK trace: trace_<id> task=task_001 status=submitted
```

## 6. Verify the trace

```bash
prooftask verify \
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

## 7. Validate the final trace

```bash
prooftask validate-trace examples/verified_trace.json
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
prooftask submit-proof \
  --task examples/manual_qa_task.json \
  --proof examples/invalid_mismatched_proof.json \
  --out examples/should_not_exist.json
```

Expected behavior: command fails with exit code `2`.

### Invalid final trace

This final trace is marked `verified` but does not include a `verification` object:

```bash
prooftask validate-trace examples/invalid_final_trace.json
```

Expected behavior: command fails with exit code `2`.

### Invalid payment task

Task creation rejects negative payment amounts:

```bash
prooftask create-task \
  --type manual_qa_check \
  --created-by agent_demo_001 \
  --objective "Invalid payment task" \
  --acceptance "Do something" \
  --proof "screenshot" \
  --payment-amount -1 \
  --out examples/invalid_task.json
```

Expected behavior: command fails with exit code `2`.

## What this proves

This demo proves the first ProofTask primitive:

> An agent-created task and a human proof submission can be converted into a traceable verification artifact.

That artifact can be accepted, rejected, stored, inspected, and later used by a larger agentic workflow.
