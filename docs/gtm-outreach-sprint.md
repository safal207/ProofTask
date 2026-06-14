# ProofTask GTM Outreach Sprint

## Purpose

This document turns the ProofTask go-to-market plan into a focused outreach sprint.

The goal is to find one real pilot candidate for ProofTask.

Primary offer:

> AI Agent QA Proof Audit: structured human proof for one AI-generated PR or feature before merge, release, or payment.

## Sprint goal

```text
30 target accounts
20 targeted messages
3 discovery calls attempted
1 concrete pilot candidate
```

## What counts as a qualified prospect

A prospect is qualified if at least three of these are true:

- they use AI coding tools or AI agents;
- AI-generated work reaches pull requests, releases, or customer-facing features;
- they have QA or code review bottlenecks;
- they ship frequently;
- a founder, CTO, QA lead, or devtool lead can approve a pilot;
- their product has user-facing flows where regressions matter;
- they already care about evidence, review, trust, or auditability.

## Priority segments

| Segment | Why it matters | ProofTask angle |
| --- | --- | --- |
| AI coding agent builders | Their users need trust and review around agent-created work | Add human proof layer for agent outputs |
| AI-heavy devtool teams | They live inside PR and CI workflows | Turn verification trace into GitHub-native artifact |
| AI code review tools | They already sell review confidence | Add human proof after automated / AI review |
| QA and crowdtesting teams | They already sell human testing | Package AI-agent QA into structured proof reports |
| Open-source AI tool maintainers | They may receive many AI-assisted PRs | Request proof before accepting risky changes |
| Regulated / high-risk SaaS teams | Evidence matters more than speed alone | Preserve human verification trace before release |

## First 30 target accounts

These are target accounts, not confirmed contacts. The next step is to find the right founder, CTO, QA lead, developer advocate, or partnerships contact for each account.

| # | Target account | Segment | Fit hypothesis | Message angle | Priority |
| ---: | --- | --- | --- | --- | --- |
| 1 | Cursor / Anysphere | AI coding tool | Users create AI-assisted code that still needs human validation | Proof layer for AI-generated PRs | High |
| 2 | Cognition / Devin | AI coding agent | Agent-created work needs trust before merge | Human proof before accepting autonomous work | High |
| 3 | GitHub Copilot | AI coding platform | Copilot already lives in PR workflows | Verification trace as PR review artifact | High |
| 4 | OpenAI Codex | AI coding agent | Codex-generated work can become review workload | Human QA proof for Codex-created changes | High |
| 5 | Anthropic Claude Code | AI coding agent | Claude Code users need review and release confidence | Structured human proof after agent work | High |
| 6 | Replit Agent | AI app builder | Users ship AI-generated apps quickly | Human QA proof before publishing | Medium |
| 7 | Sourcegraph | Devtool / code intelligence | Code intelligence plus review context | Verification evidence connected to code changes | Medium |
| 8 | Continue | Open-source AI coding assistant | Open-source dev workflow and AI coding adoption | Proof checks for AI-assisted PRs | Medium |
| 9 | OpenHands | Open-source coding agent | Agentic coding project with PR-oriented workflows | Human verification layer for agent tasks | Medium |
| 10 | Aider | Open-source coding assistant | AI-assisted code changes need review confidence | Lightweight proof flow for AI-authored changes | Medium |
| 11 | CodeRabbit | AI code review | AI review already targets PR confidence | Add human proof package for high-risk PRs | High |
| 12 | Qodo | AI code quality / review | AI review and code quality positioning | Human proof after automated review | High |
| 13 | Graphite | PR review / dev workflow | Optimizes review flow and PR stacks | ProofTask as extra human verification signal | Medium |
| 14 | Greptile | AI code review | AI code review context and PR feedback | Add human validation artifact to review loop | Medium |
| 15 | Snyk | Security / dev workflow | AI code may raise security and quality concerns | Human proof for high-risk AI-generated changes | Medium |
| 16 | Codacy | Code quality | Automated quality gates already exist | Add human proof as release confidence artifact | Medium |
| 17 | DeepSource | Code quality | Static analysis and review workflows | ProofTask as manual evidence layer | Medium |
| 18 | SonarSource | Code quality | Developers already use quality gates | Human verification for AI-created UI / workflow changes | Medium |
| 19 | Testlio | Managed QA / crowdtesting | Human testers already produce QA evidence | Package AI-agent QA as structured proof | High |
| 20 | Applause / uTest | Crowdtesting | Large human testing network | AI-agent work verification as new use case | High |
| 21 | Test IO | Crowdtesting | Human exploratory testing network | Proof packages for AI-generated features | Medium |
| 22 | QA Wolf | QA automation / QA service | QA outcome and web app testing focus | Human proof report for AI-generated UI PRs | High |
| 23 | Rainforest QA | QA platform | Human-in-the-loop testing positioning | Traceable proof for agent-generated changes | Medium |
| 24 | BrowserStack | Browser testing | Real browser/device validation | ProofTask layer for human-confirmed browser checks | Medium |
| 25 | LambdaTest | Browser testing | Cross-browser verification and QA workflows | Human proof for AI-generated UI changes | Medium |
| 26 | Sauce Labs | Testing platform | Release confidence and device testing | ProofTask trace as verification artifact | Medium |
| 27 | LangChain | Open-source AI framework | Active OSS ecosystem and many integrations | Proof gate for AI-assisted PRs / examples | Medium |
| 28 | CrewAI | Agent framework | Agents need task delegation and verification | Human proof layer for agent tasks | High |
| 29 | Microsoft AutoGen | Agent framework | Agentic workflows need evaluation and verification | ProofTask as human verification primitive | Medium |
| 30 | Supabase | Developer platform | Fast-shipping devtool with user-facing workflows | Pilot on AI-generated docs/UI/devtool PR | Medium |

## First outreach batch

Start with 20 messages.

Recommended first batch:

1. Cursor / Anysphere
2. Cognition / Devin
3. OpenAI Codex
4. Anthropic Claude Code
5. GitHub Copilot
6. CodeRabbit
7. Qodo
8. Testlio
9. Applause / uTest
10. QA Wolf
11. CrewAI
12. OpenHands
13. Continue
14. Aider
15. Graphite
16. Greptile
17. BrowserStack
18. LambdaTest
19. LangChain
20. Replit Agent

## Prospect tracker fields

Use this table structure in a spreadsheet, Notion page, GitHub issue, or CRM.

| Field | Meaning |
| --- | --- |
| Account | Company / project name |
| Segment | ICP segment |
| Contact | Person or role to contact |
| Channel | LinkedIn, X, email, GitHub, community |
| Fit score | 0-10 |
| Pain hypothesis | Why ProofTask might matter |
| Message angle | Which message to send |
| Date contacted | First message date |
| Reply | Yes / no / interested / not now |
| Next step | Follow-up, call, pilot, drop |
| Notes | Useful context |

## Fit scoring

| Signal | Points |
| --- | ---: |
| Uses AI coding tools or agents | 2 |
| Work reaches PRs or releases | 2 |
| Review or QA bottleneck is likely | 2 |
| Buyer or strong champion can be identified | 1 |
| User-facing or high-risk product area | 1 |
| Clear GitHub / PR workflow | 1 |
| Likely to pay for pilot | 1 |

Priority:

```text
8-10 = send first
5-7 = send after first batch
0-4 = park for later
```

## Core message

```text
Hi {name},

I am building ProofTask — a lightweight human verification layer for AI-generated software work.

The narrow use case is simple: when an AI coding agent creates or changes a PR, ProofTask creates a structured QA verification task, collects human proof, and produces a traceable verification artifact before merge or release.

I am looking for 3-5 AI-heavy teams to test this on one real AI-generated PR or feature.

Would it be useful to try this on one change in your workflow?
```

## AI coding agent builder message

```text
Hi {name},

Your users are already asking agents to create real software work.

I am building ProofTask, a small human verification layer for agent-created work: task -> human proof -> verifier decision -> trace.

The first use case is AI-generated PR verification before merge.

Would a structured human proof artifact be useful for your agent workflow or customer trust story?
```

## QA / crowdtesting message

```text
Hi {name},

I am building ProofTask for a narrow new QA workflow: human proof for AI-generated PRs and features.

Instead of a loose screenshot or Slack note, the tester submits structured proof, a verifier records a decision, and the team gets a traceable report before merge or release.

Could this be useful as a new pilot offer for AI-heavy software teams?
```

## Devtool / PR workflow message

```text
Hi {name},

I am exploring ProofTask as a human verification layer inside PR workflows.

The idea: AI-generated PR -> QA verification task -> human proof -> verifier decision -> PR-ready markdown comment.

Would this kind of human proof signal be useful around AI-generated changes?
```

## Follow-up 1

Send after 3-5 days.

```text
Quick follow-up, {name}.

The reason I am testing this: AI coding tools can create PRs faster than teams can confidently verify them.

ProofTask is focused on one small loop: human proof for one AI-generated change before merge.

Worth testing on one PR, or not relevant for your workflow right now?
```

## Follow-up 2

Send after 5-7 more days.

```text
Last ping from me.

I am looking for one real AI-generated PR or feature to run through a lightweight verification pilot.

If this is not relevant, no worries. If it is, I can send a 3-minute demo flow.
```

## Discovery call goal

The first call should answer:

```text
Does this team have enough pain around AI-generated work review to run one paid or serious pilot?
```

## Discovery call questions

1. What AI coding tools are you using today?
2. Do AI tools create PRs or only assist developers locally?
3. Who reviews AI-generated changes?
4. What makes an AI-generated PR safe to merge?
5. Do you require screenshots, QA notes, test evidence, or review artifacts?
6. Where does that proof live today?
7. Have AI-generated changes caused bugs, regressions, or review uncertainty?
8. Would a traceable proof artifact help before merge or release?
9. Who would own this workflow: founder, CTO, QA, devtools, or compliance?
10. Can we test this on one real PR or feature?

## Reply classification

| Reply type | Meaning | Action |
| --- | --- | --- |
| Interested | Wants demo or call | Book discovery call |
| Has pain | Mentions review/QA uncertainty | Ask for one PR example |
| Curious but vague | Likes idea but no pain yet | Send demo walkthrough |
| Not relevant | No AI PR workflow | Mark not qualified |
| No reply | No response | Send follow-up sequence |

## Weekly sprint schedule

### Day 1

- Find 30 accounts.
- Identify 1 contact per account.
- Score each account.

### Day 2

- Send first 10 messages.
- Track message angle and channel.

### Day 3

- Send next 10 messages.
- Improve message wording based on replies.

### Day 4

- Send follow-ups to early opens / reactions.
- Try to book discovery calls.

### Day 5

- Review replies.
- Update positioning.
- Pick best pilot candidate.

## Sprint success criteria

The sprint is successful if:

- 30 accounts are tracked;
- 20 messages are sent;
- 3 discovery calls are attempted;
- 1 real PR or feature is offered for a pilot;
- ProofTask positioning becomes sharper based on replies.

## Current execution status

| Item | Status |
| --- | --- |
| 30 target accounts listed | Done |
| First 20-account outreach batch selected | Done |
| Message templates prepared | Done |
| Messages sent | Not done |
| Replies tracked | Not done |
| Discovery calls booked | Not done |
| Pilot candidate identified | Not done |

## Next action

Pick one channel and send the first 10 messages.

Recommended channel order:

1. LinkedIn for founders, CTOs, QA leads, partnerships.
2. X/Twitter for devtool founders and OSS maintainers.
3. GitHub issues/discussions only when the message is clearly relevant and non-spammy.
4. Email only when a public business/contact address is available.

## Strategic reminder

The goal is not to convince everyone.

The goal is to find one buyer who says:

> Yes, we have AI-generated work and we need better human proof before merge or release.
