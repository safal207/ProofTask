# ProofTask Discovery Call Script

## Goal

This script is for a focused 15-minute discovery call with a potential ProofTask pilot customer.

The goal is not to pitch the whole future platform.

The goal is to discover whether the prospect has a real pain around human verification of AI-generated work.

Primary question:

> Does this team need structured human proof before merging, releasing, or accepting AI-agent-created work?

## Call outcome

A successful call ends with one clear next step:

- run a small pilot on one AI-generated pull request or feature;
- schedule a technical workflow review;
- get introduced to the real buyer;
- mark the prospect as not qualified.

Do not end with a vague "let us stay in touch."

## 15-minute call structure

| Time | Section | Goal |
| ---: | --- | --- |
| 0:00-1:00 | Opening | Set context and permission |
| 1:00-4:00 | Current workflow | Understand how they use AI coding tools |
| 4:00-8:00 | Pain discovery | Find review, QA, proof, and release pain |
| 8:00-10:00 | ProofTask framing | Explain the narrow use case |
| 10:00-13:00 | Pilot fit | Test whether one PR or feature can be used |
| 13:00-15:00 | Next step | Confirm owner, scope, and decision path |

## Opening

```text
Thanks for taking the time.

I am building ProofTask, a lightweight human verification layer for AI-generated software work.

I would like to understand how your team uses AI coding tools today and whether structured human proof before merge or release would be useful.

If there is no fit, that is completely fine. My goal is to learn quickly.
```

## Current workflow questions

Ask these first:

1. What AI coding tools are you using today?
2. Are they mostly assistants, or do they create full PRs/features?
3. How often does AI-generated code reach GitHub or production?
4. Who reviews AI-generated changes?
5. What needs to happen before an AI-generated change can be merged?

Listen for:

- Cursor, Copilot, Codex, Claude Code, Devin, internal agents;
- AI-generated PRs;
- founder reviewing everything manually;
- QA not involved early enough;
- review overload;
- fear of regressions.

## Pain discovery questions

Ask:

1. Have you had bugs or regressions from AI-generated work?
2. Where does verification evidence live today?
3. Do you require screenshots, notes, test reports, or acceptance criteria?
4. Is QA proof structured, or is it scattered across comments and chats?
5. Who decides whether a PR is safe to merge?
6. What is the cost of merging something wrong?
7. What part of the review process feels most unreliable?

Good pain signals:

- "We rely on comments and screenshots."
- "The founder checks everything."
- "We move fast, but QA is informal."
- "AI code looks right but sometimes breaks edge cases."
- "We need better evidence before release."
- "Review is becoming the bottleneck."

Weak pain signals:

- "We do not use AI coding tools."
- "Automated tests are enough."
- "We rarely ship."
- "We have a very mature QA process already."
- "This is interesting, but not urgent."

## ProofTask framing

Keep this short:

```text
The narrow ProofTask workflow is simple:

AI agent creates or changes a feature.
ProofTask turns that into a structured QA verification task.
A human checks it in a real browser, device, or workflow.
The human submits proof.
A verifier accepts or rejects it.
The system saves a traceable artifact.

The initial value is not another task tracker.
It is human proof before merge, release, or payment.
```

## Pilot fit questions

Ask:

1. Do you have one recent AI-generated PR or feature we could use as a test case?
2. Could we define 3-5 acceptance criteria for it?
3. What proof would make you trust the result?
4. Who should verify the proof?
5. Would a traceable artifact be useful after the release?
6. If the pilot worked, who would decide whether to continue?

## Pilot proposal

Use this if fit is clear:

```text
A practical pilot would be small.

We pick one AI-generated PR or feature, define acceptance criteria, run human verification, collect proof, and produce a traceable verification package with a release recommendation.

This would show whether ProofTask creates useful evidence for your workflow.
```

## Pricing conversation

Do not force pricing too early.

If they ask:

```text
For early pilots, I am thinking in three levels:

- Starter: $2,500 for one AI-generated PR or feature.
- Standard: $5,000 for up to three PRs or features.
- Integration pilot: $10,000-$15,000 for a lightweight GitHub workflow.

For the first pilots, I care most about finding a real workflow and clear feedback.
```

## Qualification score after the call

Score the prospect from 0 to 10.

| Signal | Points |
| --- | ---: |
| Uses AI coding tools weekly | 2 |
| AI-generated work reaches PRs/features | 2 |
| Has QA/review uncertainty | 2 |
| Has one concrete test case | 1 |
| Buyer or strong champion was on the call | 1 |
| Clear cost of bad release | 1 |
| Asked about pilot/pricing/implementation | 1 |

Priority:

- 8-10: propose pilot immediately;
- 5-7: send recap and ask for a concrete PR;
- 0-4: nurture or drop.

## Close options

### If strong fit

```text
This sounds like a real fit.

The best next step is to pick one AI-generated PR or feature and run a small ProofTask verification pilot around it.

Who should be involved in choosing that first test case?
```

### If medium fit

```text
It sounds like the pain may be emerging but not fully urgent yet.

Would it make sense to identify one AI-generated change and use it as a lightweight test case?
```

### If weak fit

```text
It sounds like this may be too early for your team right now.

That is useful to know. If AI-generated PR review becomes more painful later, ProofTask may be more relevant then.
```

## Post-call follow-up: strong fit

```text
Hi {name},

Thanks for the call today.

My understanding:

- You are using {AI tool/workflow}.
- AI-generated work reaches {PRs/features/releases}.
- The current verification gap is {pain}.
- A useful pilot would verify {specific PR/feature/workflow}.

Suggested next step:

Run a small ProofTask pilot:

1. define acceptance criteria;
2. create a structured verification task;
3. collect human proof;
4. save a traceable verification artifact;
5. produce a release recommendation.

Could you send one candidate AI-generated PR or feature we can use as the test case?
```

## Post-call follow-up: medium fit

```text
Hi {name},

Thanks for the conversation.

It sounds like AI-generated code is becoming part of your workflow, but the verification pain may still be early.

The simplest next step would be to test ProofTask on one small AI-generated change and see whether the proof artifact is useful.

If you have a recent PR or feature that fits, I would be happy to use it as a lightweight test case.
```

## Post-call follow-up: no fit

```text
Hi {name},

Thanks for the call.

Based on what you shared, ProofTask may be too early for your current workflow because {reason}.

I appreciate the feedback. If AI-generated PR review or human proof becomes more important later, I would be glad to reconnect.
```

## Call notes template

```text
Date:
Company / project:
Contact:
Role:
Segment:
AI tools used:
AI work reaches PRs? yes/no
Current review workflow:
Current QA proof:
Pain level: low / medium / high
Concrete PR or feature available? yes/no
Buyer/champion:
Budget signal:
Pilot fit score:
Next step:
Follow-up date:
Key quote:
```

## Red flags during the call

Be careful if:

- they only want free consulting;
- they cannot name one concrete AI-generated PR or feature;
- they do not use AI coding tools;
- there is no owner for QA or release decisions;
- they want a full custom platform before a small pilot;
- they ask for compliance guarantees too early;
- they want a marketplace, not verification proof.

## Strong buying signals

Strong signals:

- "We are already using AI for PRs."
- "Review is becoming a bottleneck."
- "We need better proof before release."
- "This could fit our GitHub workflow."
- "Can this work with our QA process?"
- "What would a pilot cost?"
- "Can we try this on a real PR?"

## Strategic reminder

The discovery call is not about convincing everyone.

It is about finding the people who already feel the pain.

ProofTask should sell where the pain is sharp:

> AI made the work faster. Now teams need proof they can trust.
