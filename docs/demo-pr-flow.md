# ProofTask Demo PR Flow

## Purpose

This document describes a short demo flow for showing ProofTask to a founder, CTO, QA lead, devtool builder, or AI-agent team.

The demo should take about 3 minutes.

The goal is to show one simple idea:

> AI can create the pull request, but a human can provide structured proof before the team merges it.

## Demo story

A team uses an AI coding agent to update a signup flow.

The AI-generated pull request looks good, but the team is not fully confident that the UI works in a real mobile browser.

ProofTask creates a verification task, a human tester submits proof, a verifier accepts or rejects it, and the final trace is linked back to the PR.

## Cast

| Role | Demo identity |
| --- | --- |
| AI coding agent | `agent_demo_001` |
| Pull request | `PR #124 - Update signup flow` |
| Human tester | `tester_demo_001` |
| Verifier | `verifier_demo_001` |
| ProofTask task | `github_pr_124_mobile_signup_check` |
| ProofTask trace | `trace_pr_124_demo` |

## 3-minute demo script

### 0:00-0:30 — Set the context

Say:

```text
Imagine an AI coding agent created this pull request.
The code may look fine, and CI may pass, but the team still needs human proof that the signup flow works in a real browser.
```

Show:

```text
PR #124 - Update signup flow
Label: ai-generated
Label: prooftask:required
```

### 0:30-1:00 — Show the ProofTask task

Say:

```text
ProofTask turns the PR into a structured human verification task.
Instead of vague comments like "please check this", the task has explicit acceptance criteria and proof requirements.
```

Show:

```text
Task ID: github_pr_124_mobile_signup_check
Objective: Verify that signup works on mobile Chrome after AI-generated changes.
Acceptance criteria:
- Open signup page on mobile Chrome
- Enter valid test data
- Submit the form
- Confirm success screen is shown
- Confirm no obvious visual regression in the main CTA
Required proof:
- screenshot
- short written report
- pass/fail result
```

### 1:00-1:40 — Show human proof

Say:

```text
A human tester runs the check in the real environment and submits proof.
The proof is tied to the task, not lost in Slack or random PR comments.
```

Show:

```text
Proof ID: proof_pr_124_mobile_signup
Tester: tester_demo_001
Result: pass
Evidence:
- screenshot of success screen
- short note confirming the signup flow completed
- device/browser context: mobile Chrome
```

### 1:40-2:20 — Show verifier decision

Say:

```text
Now a verifier accepts or rejects the proof.
This creates a decision record that the team can trust later.
```

Show:

```text
Verifier: verifier_demo_001
Decision: verified
Reason: All acceptance criteria passed. Screenshot and written report are sufficient.
Trace ID: trace_pr_124_demo
```

### 2:20-3:00 — Show PR outcome

Say:

```text
The PR now has a verification trace.
The maintainer still reviews code and CI, but the human QA evidence is structured and visible.
```

Show:

```text
PR status: ProofTask verified
Recommendation: can be considered for merge after normal code review and CI
Trace: trace_pr_124_demo
```

Close with:

```text
ProofTask does not replace code review or automated tests.
It adds structured human proof for AI-generated work before merge, release, or payment.
```

## Demo artifact flow

```text
AI PR
  -> ProofTask task
  -> Human proof
  -> Verifier decision
  -> Trace
  -> PR recommendation
```

## Demo task example

```json
{
  "task_id": "github_pr_124_mobile_signup_check",
  "created_by": "github_pr_124",
  "task_type": "manual_qa_check",
  "objective": "Verify that the signup flow works on mobile Chrome after AI-generated changes.",
  "acceptance_criteria": [
    "Open the signup page on mobile Chrome",
    "Enter valid test data",
    "Submit the form",
    "Confirm success screen is shown",
    "Confirm no obvious visual regression in the main CTA"
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

## Demo proof example

```json
{
  "proof_id": "proof_pr_124_mobile_signup",
  "task_id": "github_pr_124_mobile_signup_check",
  "submitted_by": "tester_demo_001",
  "result": "pass",
  "evidence": [
    {
      "type": "screenshot",
      "description": "Signup success screen on mobile Chrome"
    },
    {
      "type": "written_report",
      "description": "Tester confirmed signup completed successfully with valid test data."
    }
  ]
}
```

## Demo PR comment: verified

```text
ProofTask verification result: verified

Trace ID: trace_pr_124_demo
Task ID: github_pr_124_mobile_signup_check
Proof ID: proof_pr_124_mobile_signup
Verifier: verifier_demo_001
Reason: All acceptance criteria passed.
Recommendation: PR can be considered for merge after normal code review and CI.
```

## What the buyer should understand

After the demo, the buyer should understand:

- ProofTask is not a generic task board;
- ProofTask connects AI-generated work to human verification;
- proof is structured and traceable;
- verification can support merge and release decisions;
- this can start as a small pilot on one PR.

## Best demo audience

This demo is best for:

- founders using AI coding tools;
- CTOs worried about AI-generated regressions;
- QA leads who need better evidence;
- devtool builders exploring agent workflows;
- open-source maintainers reviewing AI-generated PRs.

## Questions to ask after the demo

Ask:

1. Do you have AI-generated PRs or features today?
2. Who verifies them before merge?
3. Where does human proof live today?
4. Would this trace be useful in your workflow?
5. Can we test this on one real PR or feature?

## Demo success criteria

The demo works if the buyer says one of these:

- "This would help us trust AI-generated PRs."
- "We need this before merge."
- "This would make QA evidence cleaner."
- "Can we try it on one PR?"
- "How would this work with GitHub?"

## Strategic reminder

Do not demo everything.

Demo one clean loop:

> AI created work. Human verified work. ProofTask saved the trace.
