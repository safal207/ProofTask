# AI PR Verification Walkthrough

## Purpose

This walkthrough shows the smallest end-to-end ProofTask demo for an AI-generated GitHub pull request.

It demonstrates the loop:

```text
AI-generated PR
  -> ProofTask task
  -> human proof
  -> verified trace
  -> PR-ready markdown comment
```

The goal is to make the demo repeatable for:

- customer calls;
- founder / CTO demos;
- QA lead conversations;
- devtool pitches;
- future GitHub workflow design.

## Demo scenario

An AI coding agent updates a signup flow.

The team wants human QA proof before merging because the change touches a user-facing conversion path.

Demo PR:

```text
Repository: demo/acme-saas
Pull request: #124 - Update signup flow
Source: AI coding agent
Changed area: signup flow
Risk area: signup conversion and mobile UX
Verification gate: pre-merge human QA
```

## Demo files

| File | Purpose |
| --- | --- |
| `examples/github_pr_task.json` | Task created for the AI-generated PR |
| `examples/github_pr_proof.json` | Human tester proof for the task |
| `examples/github_pr_verified_trace.json` | Final verified trace |
| `examples/github_pr_trace_summary.md` | Buyer-readable trace summary |
| `examples/github_pr_comment_verified.md` | Example PR-ready comment |

## Step 1: Validate the PR verification task

Run:

```bash
prooftask validate-task examples/github_pr_task.json
```

Expected output:

```text
OK task: github_pr_124_mobile_signup_check status=created
```

What to explain:

```text
This is the structured verification task.
It replaces a vague PR comment like "please check signup" with explicit acceptance criteria and proof requirements.
```

## Step 2: Validate the human proof

Run:

```bash
prooftask validate-proof examples/github_pr_proof.json
```

Expected output:

```text
OK proof: proof_pr_124_mobile_signup task=github_pr_124_mobile_signup_check result=pass
```

What to explain:

```text
The human tester submitted proof tied to the task.
The proof includes a result, written report, evidence references, and browser/device context.
```

## Step 3: Inspect the verified trace

Run:

```bash
prooftask validate-trace examples/github_pr_verified_trace.json
```

Expected output:

```text
OK trace: trace_pr_124_demo task=github_pr_124_mobile_signup_check status=verified
```

What to explain:

```text
The trace connects the original task, the submitted proof, the verifier decision, and the event history.
This is the core ProofTask artifact.
```

## Step 4: Render a PR-ready comment from the trace

Run:

```bash
prooftask render-pr-comment \
  --trace examples/github_pr_verified_trace.json
```

This prints a markdown comment that can be copied into a GitHub pull request.

To write it into a file:

```bash
prooftask render-pr-comment \
  --trace examples/github_pr_verified_trace.json \
  --out examples/generated_github_pr_comment.md
```

Expected output:

```text
OK PR comment: examples/generated_github_pr_comment.md
```

What to explain:

```text
ProofTask can turn a verified trace into a maintainer-readable PR comment.
This is the bridge from verification data to an actual GitHub review workflow.
```

## Step 5: Show the buyer-readable summary

Open:

```text
examples/github_pr_trace_summary.md
```

What to explain:

```text
This is the human-readable version of the trace.
It shows what was checked, who checked it, what proof was submitted, why the verifier accepted it, and whether the PR can move forward.
```

## Step 6: Show the PR-ready comment

Open:

```text
examples/github_pr_comment_verified.md
```

What to explain:

```text
This is what the team could paste back into the GitHub PR.
It gives the maintainer a clear verification status and recommendation.
```

## 3-minute talk track

Use this script when demoing live.

### 0:00-0:30 — Context

```text
Imagine an AI coding agent created a pull request that changes signup.
CI may pass, but the team still wants human proof that the flow works in a real browser.
```

### 0:30-1:00 — Task

```text
ProofTask creates a structured task with acceptance criteria and proof requirements.
The human tester knows exactly what to check.
```

### 1:00-1:30 — Proof

```text
The tester submits proof: result, report, screenshot reference, and browser/device context.
The proof is linked to the task.
```

### 1:30-2:15 — Trace

```text
The verifier accepts the proof.
ProofTask saves a trace that connects task, proof, decision, and events.
```

### 2:15-3:00 — GitHub comment

```text
ProofTask renders a PR-ready markdown comment.
The maintainer can now see the verification result directly in the GitHub workflow.
```

Close with:

```text
ProofTask does not replace code review or automated tests.
It adds structured human proof for AI-generated work before merge, release, or payment.
```

## What the customer should understand

After the walkthrough, the customer should understand:

- ProofTask is not a generic task board;
- ProofTask links AI-generated work to human verification;
- the proof is structured;
- the verifier decision is traceable;
- the result can be shown inside a GitHub PR;
- the first pilot can run on one real PR or feature.

## Good customer reactions

Strong signals:

- "Can we try this on one PR?"
- "This would help our QA review."
- "This would make AI-generated PRs easier to trust."
- "Can it post this comment automatically later?"
- "Could this become a required check before merge?"

Weak signals:

- "Interesting, but we do not use AI coding tools."
- "We do not have PR review pain."
- "We only want a marketplace."
- "We need enterprise compliance before any pilot."

## Demo success criteria

The walkthrough succeeds if:

- the loop is understandable in under 3 minutes;
- the buyer understands why the trace matters;
- the buyer asks about GitHub integration;
- the buyer offers one real AI-generated PR or feature to test;
- the buyer understands that the first pilot is small and focused.

## Next product step after demo

If the demo lands, the next product step is:

```text
GitHub PR -> ProofTask task -> human proof -> verifier decision -> rendered PR comment
```

The current CLI already supports the last step through:

```bash
prooftask render-pr-comment --trace <trace.json>
```

A future GitHub integration can automate comment posting later.

## Strategic reminder

Do not demo everything.

Demo one clean proof loop:

> AI created work. Human verified work. ProofTask saved the trace. GitHub got a clear recommendation.
