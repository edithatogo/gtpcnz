# Project Workflow

---
title: "Workflow"
version: "0.2.0"
status: "reviewed"
last_updated: "2026-05-26"
owner: "Dylan A Mordaunt"
---

## Guiding principles

1. Per-track plans (`conductor/tracks/*/plan.md`) are the source of truth for implementation tasks.
2. All major claims must be traceable to a source, a theory, a model assumption or a stakeholder quote.
3. Documents are versioned; do not silently overwrite released drafts.
4. Modelling must distinguish mechanism, assumption, parameter and empirical result.
5. Policy outputs must remain non-partisan and defensible.
6. Substack can be sharper in tone, but should still separate evidence from hypothesis.

## Task workflow

1. Select the next task from a track `plan.md`.
2. Mark it `[~]` before working.
3. Draft or implement the work.
4. Check against product guidelines.
5. Update document version or changelog if substantial.
6. Commit with conventional commit message.
7. Mark the task `[x]` and record commit SHA.

## Quality gates for documents

A document can move from v0.1 to v0.2 only when it has:

- clear thesis;
- evidence status labels;
- source list;
- risks and counterarguments;
- equity section;
- implementation considerations;
- next-step question.

## Quality gates for models

A model can move from specification to prototype only when it has:

- actors or stocks defined;
- parameter list;
- data source register;
- scenario library;
- validation plan;
- model limitations section.

## Session history and traceability

To maintain traceability of agent actions and track execution history, session logs are stored at:
`C:\Users\60217257\.cline\data\sessions\` (resolved from `%USERPROFILE%\.cline\data\sessions\`). 
Each session (conversation) is archived as a separate directory/file in this location and can be referenced for commit auditing and task verification.
