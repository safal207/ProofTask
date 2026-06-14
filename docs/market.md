# ProofTask Market Thesis

## Core thesis

AI agents are moving from assistant tools into active software contributors.

They can now plan work, modify code, create branches, open pull requests, run checks, and automate parts of engineering workflows.

As agentic work increases, teams need a reliable way to answer one simple question:

> Was this agent-created work verified by a human, with evidence?

ProofTask exists to make that verification traceable.

## Initial beachhead

The first market is human QA verification for AI coding agents.

Initial workflow:

1. AI coding agent creates or changes a feature.
2. ProofTask creates a structured QA verification task.
3. Human tester checks the feature in a real browser or device.
4. Human submits proof.
5. Verifier accepts or rejects the result.
6. Trace is saved for audit and release decisions.

## Why now

AI coding agents are becoming part of real software workflows.

As the volume of agent-generated pull requests, UI changes, tests, and production-impacting actions grows, human review and QA capacity become bottlenecks.

The gap:

- agent outputs can look correct but still be wrong;
- screenshots, comments, and QA notes are scattered;
- acceptance criteria are often implicit;
- verification evidence is hard to audit later;
- teams need confidence before merge or release.

ProofTask turns human verification into a structured artifact.

## Target users

Early users:

- AI coding agent builders;
- small AI-heavy software teams;
- QA engineers validating agent-generated work;
- devtool teams;
- software agencies using AI coding tools;
- safety and audit teams;
- regulated teams that need evidence before release;
- open-source maintainers receiving AI-generated pull requests.

## Initial customer profile

The strongest early customer profile:

> Small AI-heavy development teams shipping agent-generated code, but afraid to merge without human verification evidence.

This customer already has the pain:

- AI tools increase output volume;
- review capacity does not scale at the same speed;
- QA evidence is not standardized;
- managers need confidence before shipping;
- developers do not want another heavy QA platform.

## Market category

ProofTask sits between:

- software testing;
- crowdsourced QA;
- human-in-the-loop AI;
- AI-agent governance;
- developer workflow automation;
- audit evidence collection.

ProofTask is not a generic freelance marketplace.

The first goal is much narrower:

> Make one unit of agent-requested human verification traceable.

## Expansion path

ProofTask should expand in layers:

1. Local CLI for traceable proof artifacts.
2. GitHub workflow for AI-generated pull request verification.
3. Hosted dashboard for teams.
4. API for AI agents to request human verification.
5. Enterprise audit and release-gate workflow.
6. Verification marketplace after demand is proven.

## Strategic wedge

The best wedge is not "tasks for humans."

The best wedge is:

> Human proof for AI-agent work before merge, release, or payment.

That wedge is narrow enough to build, painful enough to sell, and broad enough to expand.
