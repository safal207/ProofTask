# ProofTask Positioning

## One-line description

ProofTask is the proof and verification layer for agentic work.

## Category

Agent-native human verification infrastructure.

ProofTask is not a generic freelance marketplace and not a social network for AI agents. It starts as a structured verification layer where AI agents can create small tasks, humans can submit evidence, and the system can preserve a traceable outcome.

## Initial wedge

The first wedge is human QA verification for AI coding agents.

```text
AI coding agent changes a feature
        ↓
ProofTask creates a QA verification task
        ↓
Human tester checks it in a real browser/device
        ↓
Human submits proof
        ↓
Verifier accepts or rejects
        ↓
Trace is saved
```

## Core user

Early users:

- AI coding agent builders
- QA engineers working with AI-generated code
- devtool teams
- small software teams shipping agent-created changes
- safety and audit teams that need human-in-the-loop verification records

## Pain

AI agents can increasingly create code and automate work, but many outputs still need real-world confirmation.

The current gap:

- agent outputs are often accepted without human evidence
- QA checks are not always traceable
- proof is scattered across screenshots, comments, tickets, and chats
- acceptance criteria are often implicit
- verification decisions are hard to audit later

ProofTask turns verification into a structured artifact.

## Why now

Agentic software development is moving from demo workflows into real engineering pipelines. As agents create more pull requests, tests, UI changes, and production-impacting actions, teams will need a reliable way to ask humans for evidence-backed confirmation.

The more agents act, the more valuable human proof becomes.

## What ProofTask is

ProofTask is:

- a task format for verifiable human work
- a proof submission format
- a verification trace format
- a minimal CLI for local demo flows
- a future API layer for agent-to-human task delegation

## What ProofTask is not

ProofTask is not yet:

- a full marketplace
- a payment processor
- a reputation system
- a replacement for QA platforms
- a general freelancer network
- a social network

Those can come later. The first goal is much smaller and stronger:

> Make one unit of agent-requested human verification traceable.

## Differentiation

### Compared with freelance marketplaces

Freelance marketplaces optimize for human-to-human hiring.

ProofTask optimizes for agent-to-human task delegation with explicit acceptance criteria, proof requirements, and verification traces.

### Compared with QA tools

QA tools usually manage tests, devices, sessions, and reports.

ProofTask focuses on the missing agent-native layer: why a human check was requested, what proof was required, who submitted it, and how the result was verified.

### Compared with data labeling platforms

Data labeling platforms optimize dataset creation.

ProofTask optimizes operational verification: did a specific action, feature, or real-world check actually pass?

## Strategic thesis

As AI agents perform more work, markets will need a trusted bridge between autonomous action and human confirmation.

ProofTask starts with QA verification because it is concrete, valuable, and close to existing buyer pain.

Long term, the same primitive can expand into:

- compliance review
- real-world confirmation tasks
- audit evidence collection
- human judgement tasks
- safety reviews
- agent-to-human microtask marketplaces

## Product sentence

Agents can request work. Humans can submit proof. Teams can audit the outcome.
