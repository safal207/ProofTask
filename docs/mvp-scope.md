# ProofTask MVP Scope

## Purpose

This document defines the first MVP scope for ProofTask.

The goal is to keep the product narrow enough to build, demo, sell, and validate.

ProofTask should not start as a marketplace, payment platform, or enterprise compliance suite.

The first MVP should prove one thing:

> AI-generated work can be linked to structured human proof before merge, release, or payment.

## MVP thesis

AI coding agents can create useful work, but teams still need human verification for real-world confidence.

ProofTask provides the missing verification loop:

```text
Agent-created work
  -> structured task
  -> human proof
  -> verifier decision
  -> trace
```

## Primary MVP use case

The first use case is:

> Human QA verification for AI-generated GitHub pull requests.

Example:

```text
AI changes signup flow
  -> PR is marked as needing ProofTask verification
  -> ProofTask task defines what to check
  -> human tester submits proof
  -> verifier accepts or rejects proof
  -> trace is linked to the PR
```

## In scope for MVP

### 1. Structured task creation

ProofTask must support creating a task with:

- task ID;
- creator;
- task type;
- objective;
- acceptance criteria;
- required proof;
- optional payment placeholder;
- status.

### 2. Human proof submission

ProofTask must support proof with:

- proof ID;
- task ID;
- submitter;
- pass/fail/partial result;
- evidence summary;
- optional artifact references.

### 3. Verification decision

ProofTask must support verifier decisions:

- verified;
- rejected;
- needs recheck.

Each decision should include:

- verifier;
- reason;
- timestamp;
- trace update.

### 4. Trace artifact

ProofTask must produce a trace that connects:

- task;
- proof;
- decision;
- event history.

The trace is the core product artifact.

### 5. Local CLI workflow

The MVP should continue supporting a local CLI workflow:

- create task;
- validate task;
- validate proof;
- submit proof;
- verify or reject proof;
- validate trace;
- inspect task;
- inspect trace.

### 6. Local ledger

The MVP can use a simple local file-based ledger to store:

- tasks;
- proofs;
- traces;
- events.

The ledger should stay simple and transparent.

### 7. GitHub PR demo flow

The MVP should support a demo flow where a GitHub PR can be linked to a ProofTask task.

This can be manual at first.

The goal is not full GitHub automation yet.

The goal is to show the buyer:

> This PR has human verification proof attached to it.

### 8. Pilot delivery docs

The MVP should include docs that make pilots sellable:

- pilot offer;
- outreach playbook;
- discovery call script;
- demo PR flow;
- pilot report template;
- first prospect map.

These docs help validate the market before overbuilding product features.

## Out of scope for MVP

Do not build these in the first MVP:

- full marketplace;
- automatic tester matching;
- worker reputation system;
- escrow payments;
- crypto payments;
- payout automation;
- enterprise SSO;
- multi-tenant SaaS dashboard;
- advanced RBAC;
- full GitHub App;
- complex GitHub Action automation;
- mobile app;
- browser extension;
- AI-generated acceptance criteria engine;
- compliance certification;
- cryptographic audit chain;
- large-scale task routing;
- dispute resolution system.

These may become useful later, but they are not needed to validate the first wedge.

## First product milestone

The first product milestone should be:

> A working demo where an AI-generated PR is converted into a ProofTask verification task, human proof is submitted, a verifier decision is recorded, and a trace can be shown back to the buyer.

## MVP success criteria

The MVP is successful if:

- a task can be created for an AI-generated change;
- acceptance criteria are explicit;
- human proof can be submitted;
- verifier decision is recorded;
- trace artifact is generated;
- buyer understands the value in under 3 minutes;
- one real prospect agrees to test it on a real PR or feature.

## Pilot success criteria

A pilot is successful if the buyer says at least one:

- this helps us trust AI-generated PRs;
- this makes QA evidence clearer;
- this could fit before merge;
- this would reduce founder or CTO review uncertainty;
- this should be part of our GitHub workflow;
- we would pay for another pilot.

## MVP user journey

```text
1. AI-generated work appears
2. Team decides it needs human proof
3. ProofTask task is created
4. Human tester performs check
5. Human tester submits proof
6. Verifier reviews proof
7. Trace is created
8. Maintainer uses trace to support merge/release decision
```

## MVP buyer journey

```text
1. Buyer sees AI-generated PR risk
2. Buyer watches 3-minute demo
3. Buyer provides one real PR or feature
4. ProofTask runs a small pilot
5. Buyer receives pilot report
6. Buyer decides whether to continue
```

## What to build first

Priority order:

1. Keep CLI and schemas stable.
2. Make GitHub PR demo flow easy to show.
3. Improve trace readability.
4. Add sample PR verification artifacts.
5. Create a repeatable pilot package.
6. Only then consider automation.

## What to sell first

Sell this first:

> AI Agent QA Proof Audit.

Do not sell:

- generic task marketplace;
- big SaaS dashboard;
- enterprise compliance platform;
- payment marketplace.

The first sale should be a focused pilot.

## Strategic constraint

Every MVP feature should answer this question:

> Does this help prove that teams will pay for human verification proof around AI-generated work?

If the answer is no, delay it.

## Strategic reminder

The MVP is not the final company.

The MVP is the smallest proof that the market wants the core verification primitive.

ProofTask should win by being clear:

> AI creates. Humans verify. ProofTask keeps the proof.
