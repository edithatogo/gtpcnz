# Local workspace artifact reconciliation

Date: 2026-06-15

Scope: current checkout at `primary-care-funding-architecture-v1.7.2` on branch `codex/clear-publication-followups-v1-8-1`.

## Current inventory

The transferred workspace-artifact issue described a larger May 2026 dirty tree with Conductor state, IASN2001657 copy artifacts, and a public mirror gitlink marker. The current checkout no longer shows that inventory. The current dirty state is limited to publication-readiness work and generated Substack visual assets.

## Reviewed categories and disposition

| Category | Files | Disposition |
|---|---|---|
| Publication readiness verifier | `scripts/check_substack_publication_readiness.py`, `tests/test_substack_publication_readiness.py` | Keep. These changes make the verifier handle current v1.8.1 publication contracts, mapped live drafts, standalone late-series Mermaid visuals, and local-only scoring when no live cache is available. |
| Applied Substack posts | `docs/substack-ready/posts-v1.8.1-applied/post-01...md` through `post-06...md`, plus `post-17...md` and `post-18...md` | Keep. These are intentional publication-quality edits for the applied v1.8.1 post set. |
| Mermaid preview sources | `docs/substack-ready/mermaid-preview-v1.7.2/pcf-v172-17-preview.mmd`, `docs/substack-ready/mermaid-preview-v1.7.2/pcf-v172-18-preview.mmd` | Keep. These align the late-series visual contract with the standalone post treatment. |
| Generated figures | `docs/substack-ready/figures/pcf-v172-sim-*.png` | Keep. These are generated visual assets referenced by the refreshed publication package. |
| Temporary browser screenshots | `codex-tmp/gtpcnz-streamlit-*.jpg` | Leave untracked. They are local verification evidence and are not source-of-truth repo content. |
| Conductor/IASN copy artifacts from the transferred issue | None visible in current `git status --short` | No action. Do not recreate or delete absent historical artifacts. |

## Completion rule

Commit intentional source-of-truth updates separately from local verification evidence. Do not commit `codex-tmp/` screenshots or processed-schema scratch directories. Repo-health and publication-readiness gates must pass after the source-of-truth changes are committed.
