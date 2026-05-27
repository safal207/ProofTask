# ProofTask MVP

## Product thesis

AI agents are becoming capable of creating code, plans, research, and automated workflows. However, many agent outputs still need human verification before they can be trusted in the real world.

ProofTask starts as a narrow human verification layer for AI agents.

## First use case

The first MVP focuses on QA verification tasks:

> An AI coding agent creates or changes a feature, then asks a human tester to verify it and submit proof.

## MVP flow

```text
Agent creates QA task
        ↓
Human tester accepts task
        ↓
Human tester performs check
        ↓
Human submits proof
        ↓
Verifier accepts or rejects
        ↓
Task trace is saved
```

## Minimal entities

### Task

A structured request created by an agent or human.

Required fields:

- task_id
- created_by
- task_type
- objective
- acceptance_criteria
- proof_required
- status

### Proof

Evidence submitted by a human worker.

Examples:

- screenshot
- short written report
- pass/fail result
- device/browser details
- reproduction steps

### Trace

Audit metadata describing why the task was created, who acted on it, and how its status changed.

## Definition of Done for the first demo

- A task schema exists
- A sample QA task exists
- A human proof submission format exists
- A task can move through statuses: created → submitted → verified/rejected
- A final trace can be exported as JSON

## Non-goals for the first MVP

- Full freelance marketplace
- Complex reputation system
- Automatic crypto or fiat payments
- Large social network features
- General-purpose task marketplace

## Success criterion

A developer or AI coding agent can create a QA task, a human can submit proof, and the system can show a traceable verification result.
