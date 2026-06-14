# ProofTask GitHub Workflow

## Purpose

This document describes a future GitHub-based workflow for ProofTask.

The goal is to connect ProofTask to the place where AI-generated software work already appears: pull requests.

Core idea:

> AI-generated pull requests should be able to request structured human verification before merge.

## Target workflow

```text
AI coding agent opens PR
        ↓
ProofTask creates verification task
        ↓
Human tester checks the change
        ↓
Human submits proof
        ↓
Verifier accepts or rejects proof
        ↓
ProofTask saves trace
        ↓
PR receives merge / recheck / reject recommendation
```

## Initial use case

The first GitHub workflow should focus on one narrow case:

> A pull request created or heavily modified by an AI coding agent needs human QA proof before merge.

Example:

```text
AI coding agent changes signup flow
        ↓
PR is opened on GitHub
        ↓
ProofTask asks a human to verify signup on mobile Chrome
        ↓
Human submits screenshot and written report
        ↓
Verifier accepts proof
        ↓
Trace is attached to PR
        ↓
Maintainer merges with evidence
```

## Actors

| Actor | Role |
| --- | --- |
| AI coding agent | Creates or modifies code and opens a PR |
| Developer | Reviews code and coordinates changes |
| Human tester | Performs the requested verification |
| Verifier | Accepts or rejects submitted proof |
| Maintainer / CTO / QA lead | Makes final merge or release decision |
| ProofTask | Stores task, proof, decision, and trace |

## Suggested PR labels

| Label | Meaning |
| --- | --- |
| `prooftask:required` | PR needs human verification before merge |
| `prooftask:task-created` | Verification task exists |
| `prooftask:proof-submitted` | Human proof has been submitted |
| `prooftask:verified` | Proof accepted; PR can be considered for merge |
| `prooftask:rejected` | Proof rejected; PR should not be merged yet |
| `prooftask:needs-recheck` | More evidence or another test pass is required |
| `ai-generated` | PR was created or materially changed by an AI coding workflow |

## PR comment states

### Task created

The PR should show:

```text
ProofTask verification required
Task ID: {task_id}
Objective: {objective}
Required proof: {proof_required}
Acceptance criteria: {criteria}
```

### Proof submitted

The PR should show:

```text
ProofTask proof submitted
Proof ID: {proof_id}
Submitted by: {tester}
Result: {pass/fail/partial}
Evidence summary: {summary}
```

### Verified

The PR should show:

```text
ProofTask verification result: verified
Trace ID: {trace_id}
Verifier: {verifier}
Reason: {reason}
Recommendation: PR can be considered for merge after normal review and CI.
```

### Rejected

The PR should show:

```text
ProofTask verification result: rejected
Trace ID: {trace_id}
Verifier: {verifier}
Reason: {reason}
Recommendation: do not merge until issues are fixed and verification is repeated.
```

## Task creation options

### Option 1: manual task creation

A maintainer or developer manually creates a ProofTask verification task for a PR.

Best for the MVP.

### Option 2: label-based task creation

When a PR receives `prooftask:required`, a script or future GitHub integration creates a verification task.

Best for an early GitHub workflow.

### Option 3: AI-agent metadata trigger

If a PR indicates agent-created work, ProofTask suggests a verification task.

Best for later automation.

### Option 4: release-gate trigger

Before merge or release, ProofTask checks whether required proof exists.

Best for teams that want ProofTask as a quality gate.

## Minimal MVP workflow

The first implementation should stay simple.

1. Developer labels PR with `prooftask:required`.
2. ProofTask task is created manually or through a small script.
3. Human tester runs the check.
4. Proof is submitted.
5. Verifier accepts or rejects proof.
6. Trace is posted back to the PR as a comment or linked artifact.
7. Maintainer decides merge, recheck, or reject.

## Verification status model

| Status | Meaning | PR recommendation |
| --- | --- | --- |
| `not_required` | No ProofTask check required | Normal review |
| `required` | Human verification required | Do not merge yet |
| `task_created` | Task exists | Waiting for proof |
| `proof_submitted` | Proof submitted | Waiting for verifier |
| `verified` | Proof accepted | Can consider merge |
| `rejected` | Proof rejected | Do not merge |
| `needs_recheck` | More evidence required | Re-run verification |

## Required PR metadata

A useful GitHub verification record should include:

```text
Repository:
Pull request number:
Pull request title:
AI tool / agent:
Task ID:
Proof ID:
Trace ID:
Tester:
Verifier:
Decision:
Reason:
Evidence summary:
Risk level:
Release recommendation:
```

## Acceptance criteria for the GitHub workflow MVP

The workflow is useful if:

- a PR can be linked to a ProofTask task;
- acceptance criteria are visible to humans;
- proof can be submitted against the PR task;
- verifier decision can be saved;
- trace can be referenced from the PR;
- maintainer can make a clearer merge decision.

## Non-goals for the first version

Do not build these first:

- full marketplace;
- automatic worker matching;
- full payment escrow;
- complex permissions;
- enterprise compliance controls;
- advanced GitHub App UI;
- automatic trust scoring;
- multi-tenant dashboard.

The first version should prove one thing:

> A GitHub PR can carry structured human verification proof before merge.

## Buyer value

For a founder:

> I can ship AI-assisted code faster without losing human verification.

For a CTO:

> I can see what was checked before merge.

For a QA lead:

> I can turn QA evidence into a traceable artifact.

For an open-source maintainer:

> I can ask for proof before accepting AI-generated contributions.

For a regulated team:

> I can preserve evidence around human review of AI-created changes.

## Strategic next step

The best next product step is a demo PR flow:

```text
Demo PR -> ProofTask task -> proof submission -> verifier decision -> trace comment on PR
```

This demo can become the center of:

- customer calls;
- pilot delivery;
- README examples;
- future GitHub integration design;
- investor or grant demos.
