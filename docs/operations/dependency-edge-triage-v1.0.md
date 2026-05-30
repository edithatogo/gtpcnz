# Dependency Edge Triage

Version: v1.0  
Status: active operational note

## Purpose

This note records edge-only failures from the experimental edge lane without weakening the stable release gate.

## Triage Steps

1. Capture the edge workflow failure and the package/runtime combination that triggered it.
2. Decide whether the failure is a prerelease package issue, a Python runtime issue, or a repo issue.
3. Record the issue in the upgrade queue with enough detail to reproduce it locally.
4. Leave stable release CI unchanged unless the same defect is also present there.
5. Re-run the edge workflow after the dependency or runtime update lands.

## Escalation Rule

edge-only failures stay in the upgrade queue until either the dependency is updated or the issue is proven to affect stable release CI as well.
