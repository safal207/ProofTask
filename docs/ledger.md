# ProofTask Local Ledger

The local ledger is a minimal file-based workspace for ProofTask tasks, proofs, traces, and append-only events.

It is intentionally simple:

```text
.prooftask/
├── ledger.json
├── events.jsonl
├── tasks/
├── proofs/
└── traces/
```

The ledger turns the standalone ProofTask flow into a local proof machine:

```text
task → proof → submitted trace → verified/rejected trace
```

## Initialize a ledger

```bash
prooftask init-ledger --ledger .prooftask
```

This creates:

- `.prooftask/ledger.json`
- `.prooftask/events.jsonl`
- `.prooftask/tasks/`
- `.prooftask/proofs/`
- `.prooftask/traces/`

## Add a task

```bash
prooftask ledger-add-task \
  --ledger .prooftask \
  --task examples/manual_qa_task.json
```

The task is copied into:

```text
.prooftask/tasks/<task_id>.json
```

An event is appended to:

```text
.prooftask/events.jsonl
```

## Submit proof for a ledger task

```bash
prooftask ledger-submit-proof \
  --ledger .prooftask \
  --task-id task_001 \
  --proof examples/manual_qa_proof.json
```

This does four things:

1. validates the task from the ledger
2. validates the proof file
3. stores the proof in `.prooftask/proofs/<proof_id>.json`
4. creates a submitted trace in `.prooftask/traces/<trace_id>.json`

It also updates the ledger task status from `created` to `submitted`.

## List traces

```bash
prooftask list-traces --ledger .prooftask
```

JSON output:

```bash
prooftask list-traces --ledger .prooftask --json
```

Filter by status:

```bash
prooftask list-traces --ledger .prooftask --status submitted
prooftask list-traces --ledger .prooftask --status verified
prooftask list-traces --ledger .prooftask --status rejected
```

## Inspect a trace

```bash
prooftask inspect-trace \
  --ledger .prooftask \
  --trace-id trace_abc123
```

## Verify or reject a ledger trace

```bash
prooftask ledger-verify \
  --ledger .prooftask \
  --trace-id trace_abc123 \
  --decision verified \
  --verifier verifier_demo_001 \
  --reason "All acceptance criteria passed."
```

This updates:

- `.prooftask/traces/<trace_id>.json`
- `.prooftask/tasks/<task_id>.json`
- `.prooftask/events.jsonl`

The task and trace move to `verified` or `rejected` together.

## List tasks

```bash
prooftask list-tasks --ledger .prooftask
```

JSON output:

```bash
prooftask list-tasks --ledger .prooftask --json
```

Filter by status:

```bash
prooftask list-tasks --ledger .prooftask --status created
prooftask list-tasks --ledger .prooftask --status submitted
prooftask list-tasks --ledger .prooftask --status verified
```

## Inspect a task

```bash
prooftask inspect-task \
  --ledger .prooftask \
  --task-id task_001
```

## Current ledger guarantees

The local ledger currently guarantees:

- tasks are validated before being added
- proof is validated before submission
- proof must match the ledger task by `task_id`
- task files are stored by `task_id`
- proof files are stored by `proof_id`
- trace files are stored by `trace_id`
- duplicate task IDs are rejected unless `--overwrite` is used
- duplicate proof IDs are rejected unless `--overwrite` is used
- ledger events are appended as JSON Lines
- submitted proof creates a submitted trace
- ledger verification updates both task and trace status
- tasks and traces can be listed and inspected through CLI commands

## Non-goals for this version

This version does not yet provide:

- cryptographic hash chains
- concurrency controls
- remote sync
- payment state transitions
- multiple proof submissions per task with adjudication
- user authentication or worker reputation

Those can be added after the local proof lifecycle is stable.
