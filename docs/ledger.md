# ProofTask Local Ledger

The local ledger is a minimal file-based workspace for ProofTask tasks.

It is intentionally simple:

```text
.prooftask/
├── ledger.json
├── events.jsonl
├── tasks/
├── proofs/
└── traces/
```

The first ledger version stores tasks and records append-only events. It does not yet store submitted proof or final traces automatically.

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
- task files are stored by `task_id`
- duplicate task IDs are rejected unless `--overwrite` is used
- ledger events are appended as JSON Lines
- the ledger can be listed and inspected through CLI commands

## Non-goals for this version

This version does not yet provide:

- automatic proof storage
- automatic trace storage
- cryptographic hash chains
- concurrency controls
- remote sync
- payment state transitions

Those can be added after the task ledger is stable.
