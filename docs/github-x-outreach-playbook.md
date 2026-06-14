# GitHub + X Outreach Playbook

## Purpose

This playbook defines how to run the first ProofTask outreach sprint using GitHub and X.

The goal is not mass outreach.

The goal is to find one serious pilot candidate who has a real AI-generated PR or feature that needs human verification proof.

## Channel strategy

| Channel | Best use | Avoid |
| --- | --- | --- |
| GitHub | Relevant discussions, issues, PR workflow conversations, OSS maintainer relationships | Opening random sales issues |
| X | Public founder/devtool conversations, replies, short demo posts, lightweight DMs | Long pitch threads and cold spam |

## Core offer

```text
ProofTask helps teams add structured human proof to AI-generated software work before merge or release.

Demo loop:
AI-generated PR -> verification task -> human proof -> verifier decision -> PR-ready comment.
```

## GitHub outreach rules

GitHub should be used carefully.

Do:

- contribute to relevant conversations;
- comment only when ProofTask directly helps the issue or discussion;
- be transparent that ProofTask is early;
- ask for feedback on a narrow workflow;
- link to the demo walkthrough only when useful;
- prioritize maintainers and projects already discussing AI PRs, code review, QA, testing, agents, or human-in-the-loop workflows.

Do not:

- open sales issues in random repos;
- paste the same message across projects;
- ask maintainers to try ProofTask when there is no clear relevance;
- hijack bug reports;
- overclaim compliance, security, or production readiness.

## GitHub target contexts

Look for these contexts:

- repo discussions about AI coding agents;
- issues mentioning agent-generated PRs;
- issues about review overload;
- discussions about QA evidence;
- docs around contributor verification;
- PR templates asking for screenshots or manual test proof;
- tools that touch GitHub PR review, CI, QA, test evidence, or agents.

## GitHub comment template: discussion reply

```text
This is closely related to something I am building called ProofTask.

The narrow idea is: when an AI-generated PR changes a user-facing flow, the project can create a structured human verification task, collect proof, record a verifier decision, and attach a trace back to the PR.

I am testing this as a small workflow, not a marketplace:

AI PR -> task -> human proof -> verifier decision -> PR-ready comment.

If useful, I can share a 3-minute walkthrough and would be curious whether this would help your review flow.
```

## GitHub comment template: maintainer review overload

```text
One possible pattern here is to separate code review from human behavior verification.

For AI-generated PRs, the project could require a small proof artifact:

- what was checked;
- who checked it;
- what evidence was submitted;
- who accepted or rejected the proof;
- whether the PR can move forward.

I am prototyping this in ProofTask as a lightweight trace around AI-generated PRs. Happy to share the demo flow if this is relevant.
```

## GitHub comment template: screenshot/manual QA requirement

```text
This is exactly the kind of case where a structured proof artifact could help.

Instead of only asking for a screenshot, the PR could have a small verification task with acceptance criteria, required proof, tester notes, and a verifier decision.

I am testing this workflow in ProofTask for AI-generated PRs. The output is a PR-ready markdown comment that summarizes the proof and recommendation.
```

## GitHub profile / repo preparation

Before commenting on other projects, make the ProofTask repo easy to understand.

Checklist:

- README explains the product in one sentence.
- Demo walkthrough is linked.
- `examples/github_pr_verified_trace.json` exists.
- `examples/github_pr_comment_verified.md` exists.
- `examples/pilot_report_signup_flow.md` exists.
- PR #8 is merged or easy to review.
- GitHub profile bio points to ProofTask or human verification for AI agents.

## X outreach rules

X should be used to create signal before DMs.

Do:

- post short ProofTask ideas publicly;
- reply to founders and devtool builders discussing AI coding agents;
- show the demo loop visually in text;
- ask simple questions;
- DM only after a relevant interaction when possible.

Do not:

- send long cold DMs;
- pitch too many features;
- mention marketplace first;
- ask for a big call before proving relevance;
- argue with skeptics.

## X post sequence

### Post 1: core thesis

```text
AI coding agents are making PR creation faster.

But merge confidence still needs proof:

- what was checked
- who checked it
- what evidence exists
- who accepted it
- why it is safe to move forward

I am building ProofTask as a human verification layer for AI-generated work.
```

### Post 2: narrow demo loop

```text
ProofTask demo loop:

AI-generated PR
-> verification task
-> human proof
-> verifier decision
-> trace
-> PR-ready comment

Not replacing CI.
Not replacing code review.
Adding structured human proof where automated checks are not enough.
```

### Post 3: buyer question

```text
Question for teams using Cursor, Claude Code, Codex, Copilot, Devin, or other coding agents:

When AI-generated work reaches a PR, what proof do you need before merge?

Screenshots?
QA notes?
Manual test evidence?
Reviewer sign-off?
Something else?
```

### Post 4: pilot ask

```text
I am looking for 3-5 AI-heavy teams to test ProofTask on one real AI-generated PR or feature.

Output:
- acceptance criteria
- human proof package
- verifier decision
- trace artifact
- PR-ready recommendation

Small pilot, narrow workflow.
```

## X reply template: AI PR concern

```text
This is the exact gap I am exploring with ProofTask.

AI can create the PR, but the team still needs structured proof before merge:
what was checked, who checked it, what evidence exists, and who accepted it.

Would a trace like that help your workflow?
```

## X reply template: QA / review bottleneck

```text
I think this becomes a new QA/review primitive:

AI-generated PR -> human verification task -> proof -> verifier decision -> PR comment.

Tiny workflow, but it gives the maintainer something more concrete than "looks good".
```

## X DM template after interaction

```text
Hey {name}, saw your post about AI-generated code / PR review.

I am building ProofTask, a small human verification layer for AI-generated work.

The first workflow is narrow:
AI PR -> QA task -> human proof -> verifier decision -> PR-ready comment.

Would you be open to testing the demo flow on one AI-generated PR or giving blunt feedback?
```

## First 10 actions

### GitHub actions

1. Improve ProofTask repo landing page if needed.
2. Search for discussions about AI-generated PR review.
3. Search for OSS repos with PR templates requiring screenshots/manual testing.
4. Find 5 GitHub conversations where a ProofTask-style comment is genuinely relevant.
5. Leave 1-2 thoughtful comments, not mass messages.

### X actions

1. Post the core thesis.
2. Post the demo loop.
3. Reply to 5 relevant AI coding / devtool posts.
4. DM only people who interact or clearly match the ICP.
5. Track replies in the GTM sprint tracker.

## First 10 message targets by channel

| Target | Channel | Action |
| --- | --- | --- |
| CodeRabbit | X | Reply or DM around AI review confidence |
| Qodo | X | Reply or DM around code quality / AI review |
| CrewAI | GitHub / X | Ask about agent task verification use case |
| OpenHands | GitHub | Look for discussion around agent PR validation |
| Continue | GitHub | Look for AI coding assistant workflow discussions |
| Aider | GitHub | Look for AI-authored change review discussions |
| QA Wolf | X | Ask about AI-generated UI QA proof |
| Testlio | X | Ask about AI-agent QA as managed testing use case |
| Cursor / Anysphere | X | Reply to AI coding workflow conversation |
| Devin / Cognition | X | Reply to agent-created work trust conversation |

## Tracking table

| Date | Channel | Target | Contact | Message type | Status | Reply | Next step |
| --- | --- | --- | --- | --- | --- | --- | --- |
| TBD | GitHub | TBD | TBD | Discussion reply | Not sent | TBD | TBD |
| TBD | X | TBD | TBD | Public post | Not sent | TBD | TBD |

## Success criteria

The GitHub + X sprint is successful if:

- 4 public X posts are published;
- 5 relevant X replies are posted;
- 1-2 genuinely relevant GitHub comments are posted;
- 3 conversations start;
- 1 team offers a real AI-generated PR or feature for a pilot.

## Strategic reminder

Do not sell a giant platform.

Sell one proof loop:

> AI created work. Human verified work. ProofTask kept the proof.
