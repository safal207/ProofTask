# ProofTask Pilot Report Template

## Purpose

This template is used after a ProofTask pilot to deliver a clear, client-ready report.

The report should show:

- what was verified;
- why it was verified;
- what proof was submitted;
- who verified the proof;
- what risks were found;
- whether the work should be merged, released, rejected, or rechecked;
- what the next step should be.

The goal is to make the buyer feel:

> This is not just a QA note. This is a traceable verification artifact.

## Report title

```text
ProofTask Pilot Report: {Feature / PR / Workflow Name}
```

## Executive summary

```text
Client:
Date:
Pilot type:
Verified item:
AI tool / agent involved:
Verification status:
Release recommendation:
Overall risk level:
```

### Example

```text
Client: Acme SaaS
Date: 2026-06-14
Pilot type: AI Agent QA Proof Audit
Verified item: PR #124 - Signup flow update
AI tool / agent involved: Cursor-assisted coding workflow
Verification status: Verified with minor issues
Release recommendation: Safe to merge after fixing one copy issue
Overall risk level: Medium-low
```

## 1. Pilot scope

Describe the exact scope.

```text
This pilot verified {specific AI-generated PR / feature / workflow}.

The purpose was to determine whether the change satisfied the agreed acceptance criteria and whether there was enough human proof to support a merge or release decision.
```

### In scope

- `{item 1}`
- `{item 2}`
- `{item 3}`

### Out of scope

- `{item 1}`
- `{item 2}`
- `{item 3}`

## 2. Verification context

```text
AI-generated work source:
Repository / project:
Pull request / feature link:
Environment tested:
Browser / device:
Tester:
Verifier:
Date tested:
```

## 3. Acceptance criteria

| # | Acceptance criterion | Result | Evidence |
| ---: | --- | --- | --- |
| 1 | `{criterion}` | Pass / Fail / Partial | `{proof reference}` |
| 2 | `{criterion}` | Pass / Fail / Partial | `{proof reference}` |
| 3 | `{criterion}` | Pass / Fail / Partial | `{proof reference}` |
| 4 | `{criterion}` | Pass / Fail / Partial | `{proof reference}` |
| 5 | `{criterion}` | Pass / Fail / Partial | `{proof reference}` |

## 4. Proof submitted

List the proof artifacts.

| Proof ID | Type | Description | Status |
| --- | --- | --- | --- |
| `{proof_001}` | Screenshot | `{description}` | Accepted / Rejected |
| `{proof_002}` | Written report | `{description}` | Accepted / Rejected |
| `{proof_003}` | Video / log / note | `{description}` | Accepted / Rejected |

## 5. Verification decision

```text
Decision: Verified / Rejected / Needs recheck
Verifier:
Reason:
Decision date:
Trace ID:
```

### Decision rationale

```text
The submitted proof was accepted because {reason}.

The main evidence supporting this decision was {evidence}.

Remaining uncertainty: {uncertainty}.
```

## 6. Findings

### Passed checks

- `{passed check 1}`
- `{passed check 2}`
- `{passed check 3}`

### Issues found

| Severity | Issue | Impact | Recommendation |
| --- | --- | --- | --- |
| High / Medium / Low | `{issue}` | `{impact}` | `{recommendation}` |
| High / Medium / Low | `{issue}` | `{impact}` | `{recommendation}` |

### Open questions

- `{question 1}`
- `{question 2}`

## 7. Risk assessment

| Risk area | Level | Notes |
| --- | --- | --- |
| Functional risk | High / Medium / Low | `{notes}` |
| UX risk | High / Medium / Low | `{notes}` |
| Regression risk | High / Medium / Low | `{notes}` |
| Release risk | High / Medium / Low | `{notes}` |
| Evidence quality | High / Medium / Low | `{notes}` |

## 8. Release recommendation

Choose one:

### Recommended: safe to merge

```text
The verified item satisfies the agreed acceptance criteria.
The proof package is sufficient.
Recommendation: safe to merge / release.
```

### Recommended: merge after fixes

```text
The verified item mostly satisfies the agreed acceptance criteria, but the following fixes should be completed before merge or release:

1. {fix 1}
2. {fix 2}

Recommendation: merge / release after fixes are confirmed.
```

### Recommended: recheck required

```text
The submitted proof is not sufficient to support a release decision.
The following areas need recheck:

1. {area 1}
2. {area 2}

Recommendation: do not merge / release until recheck is completed.
```

### Recommended: reject

```text
The verified item does not satisfy the agreed acceptance criteria.
Recommendation: reject and return to development.
```

## 9. Business value observed

Use this section to connect the pilot to buyer value.

```text
The pilot showed that ProofTask can help the team:

- make human verification evidence explicit;
- reduce uncertainty around AI-generated work;
- preserve QA proof outside scattered comments and chats;
- support merge and release decisions;
- create a repeatable verification workflow.
```

## 10. Suggested next step

Choose one:

### Next step: run another pilot

```text
Recommended next step:

Run a second ProofTask pilot on {next PR / feature / workflow}.

Goal:
Validate whether the workflow works across multiple AI-generated changes.
```

### Next step: lightweight GitHub workflow

```text
Recommended next step:

Create a lightweight GitHub workflow where AI-generated PRs can trigger ProofTask verification tasks.

Goal:
Move from manual pilot to repeatable team workflow.
```

### Next step: integration pilot

```text
Recommended next step:

Run a ProofTask Integration Pilot.

Scope:
- GitHub-based task creation;
- proof templates;
- reviewer decision flow;
- trace export;
- pilot dashboard or report package.
```

## 11. Appendix: raw trace summary

```text
Task ID:
Proof ID:
Trace ID:
Created by:
Submitted by:
Verified by:
Status:
Events:
- {event 1}
- {event 2}
- {event 3}
```

## 12. Appendix: client quote

Capture one strong quote if possible.

```text
"{client quote about the value of ProofTask}"
```

Good quote examples:

- "This would help us trust AI-generated PRs."
- "This makes QA evidence easier to share."
- "This could fit before merge."
- "This is better than screenshots lost in Slack."

## Report quality checklist

Before sending, confirm:

- the verified item is specific;
- acceptance criteria are explicit;
- proof artifacts are listed;
- verification decision is clear;
- risks are stated honestly;
- recommendation is actionable;
- next step is concrete;
- the report can be understood by a founder, CTO, QA lead, or product lead.

## Strategic reminder

A strong pilot report is a sales asset.

It should prove that ProofTask creates value before the full product exists.

The report should make the buyer think:

> We should not merge AI-generated work without this kind of proof.
