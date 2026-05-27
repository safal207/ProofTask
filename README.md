# ProofTask

**ProofTask is a human verification layer for AI agents.**

AI agents can create small, verifiable tasks for humans — such as QA checks, UI validation, screenshot proof, real-world confirmation, compliance review, or human judgement — and receive structured proof back.

The goal is simple:

> Agents can act. Humans can verify. The system keeps the proof.

## Why ProofTask exists

AI agents are becoming good at planning, coding, researching, and automating work.

But many tasks still require human confirmation:

- Did the website actually work in a real browser?
- Did the button behave correctly on mobile?
- Is the screenshot real?
- Was the requested action completed?
- Can a human verify that the result matches the intention?

ProofTask turns those checks into structured tasks with proof, status, and traceability.

## Core flow

```text
Agent creates task
        ↓
Human accepts task
        ↓
Human submits proof
        ↓
Verifier accepts or rejects
        ↓
Trace is saved
        ↓
Payment can be released
```

## Install locally

ProofTask can be run directly as a script or installed as a local CLI.

```bash
python -m pip install -e .
prooftask --help
```

Run tests:

```bash
python -m pip install -e . pytest
pytest -q
```

## Quickstart

Run the local MVP CLI with the built-in examples:

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

prooftask validate-task examples/manual_qa_task.json
prooftask validate-proof examples/manual_qa_proof.json

prooftask submit-proof \
  --task examples/manual_qa_task.json \
  --proof examples/manual_qa_proof.json \
  --out examples/submitted_trace.json

prooftask validate-trace examples/submitted_trace.json

prooftask verify \
  --trace examples/submitted_trace.json \
  --decision verified \
  --verifier verifier_demo_001 \
  --reason "All acceptance criteria passed." \
  --out examples/verified_trace.json

prooftask validate-trace examples/verified_trace.json
```

Expected result:

```text
OK created task: task_generated_001 -> examples/generated_task.json
OK task: task_001 status=created
OK proof: proof_001 task=task_001 result=pass
OK submitted: trace_<id> -> examples/submitted_trace.json
OK trace: trace_<id> task=task_001 status=submitted
OK verified: trace_<id> -> examples/verified_trace.json
OK trace: trace_<id> task=task_001 status=verified
```

For a full walkthrough, see [`docs/demo.md`](docs/demo.md).

## CLI commands

```text
prooftask create-task      Create a structured task JSON file
prooftask validate-task    Validate a task JSON file
prooftask validate-proof   Validate a human proof JSON file
prooftask submit-proof     Create a submitted trace from task + proof
prooftask validate-trace   Validate a trace JSON file
prooftask verify           Verify or reject a submitted trace
```

## Schemas

ProofTask currently defines three MVP artifacts:

- `schemas/task.schema.json` — structured task request
- `schemas/proof.schema.json` — human proof submission
- `schemas/trace.schema.json` — verification trace containing task, proof, decision, and events

## Example task

```json
{
  "task_id": "task_001",
  "created_by": "ai_agent",
  "task_type": "manual_qa_check",
  "objective": "Verify that the signup form works on mobile Chrome",
  "acceptance_criteria": [
    "Open the signup page",
    "Enter valid test data",
    "Submit the form",
    "Confirm success screen is shown"
  ],
  "proof_required": [
    "screenshot",
    "short written report",
    "pass_or_fail result"
  ],
  "payment": {
    "amount": 5,
    "currency": "USD",
    "status": "pending"
  },
  "status": "created"
}
```

## Initial use cases

- Human QA checks for AI-generated code
- Browser/device verification
- Screenshot-based proof
- Human-in-the-loop review
- Real-world confirmation tasks
- Compliance and audit review
- Agent-to-human microtask delegation

## What makes ProofTask different

ProofTask is not just a freelance marketplace.

It is designed for agent-native work:

- structured task creation
- explicit acceptance criteria
- proof requirements
- traceable execution
- human verification
- future payment integration
- safety and audit hooks

## MVP scope

The first version focuses on one narrow use case:

> AI coding agents can create QA microtasks, and human testers can submit proof of verification.

## Roadmap

See [`docs/roadmap.md`](docs/roadmap.md).

## Repository structure

```text
prooftask.py  Dependency-free MVP CLI
tests/        CLI regression tests
schemas/      JSON schemas for tasks, proof, and trace records
examples/     Example agent-created tasks, proof submissions, and invalid fixtures
docs/         MVP notes, positioning, demo walkthrough, and roadmap
.github/      CI smoke test for the full verification flow
```

## Project status

Early concept / MVP design.

## License

Apache-2.0
