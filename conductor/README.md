# Conductor Operations Kit

This directory contains reusable Conductor assets for GTPCNZ repo operations.
It is intentionally separate from model code and public dashboard content.

## Assets

- `templates/`: copyable track templates for repo hygiene, dashboard claims, dependency/runtime edge work, and release/publish work.
- `agents/`: role briefs for focused subagents or human reviewers.
- `skills/`: repeatable operating procedures that can be invoked during implementation.
- `workflows/`: step-by-step runbooks for common repo maintenance flows.

## Operating Rule

Every operational track should define:

- scope and non-goals;
- files allowed to change;
- verification commands;
- merge/publish policy;
- rollback or recovery path;
- explicit handling for dirty worktrees and nested repos.

The repo hygiene workflow is the default starting point before any broad change.
