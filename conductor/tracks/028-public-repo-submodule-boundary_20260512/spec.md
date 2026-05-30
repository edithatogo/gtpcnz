# Spec: Public Repo Submodule Boundary

## Problem

The public GitHub repository must not mirror the full parent research workspace. The public surface should contain only the Streamlit and Quarto dashboards plus explicitly selected supporting files needed for deployment, citation, contribution, security and reproducibility.

## Target State

- [x] `edithatogo/gtpcnz` is a public, minimal repository.
- [x] The parent workspace has no GitHub remote pointing at `edithatogo/gtpcnz`.
- [x] The parent workspace records `public/gtpcnz` as a Git submodule.
- [x] GitHub Pages serves the rendered Quarto website from the public repository.
- [x] Streamlit remains deployable from the public repository using `streamlit_app.py`.
- [x] GitHub Actions workflows remain in the public repository for CI and workflow-based Pages deployment when the GitHub account can run Actions.

## Public Repository Boundary

Allowed public files:

- GitHub workflows and Dependabot configuration.
- Streamlit configuration, entrypoint and dashboard model package.
- Quarto project files, public reports and rendered-site source documents.
- Public documentation: README, deployment notes, report notes, model card and claim-boundary notes.
- Small public output data required by the dashboard/report.
- Community and governance files: license, citation, security, contribution and code of conduct.

Excluded from the public repository:

- Parent research drafts and working notes.
- Full Conductor workspace.
- Non-public source material, local packaging artifacts and broad history.
- Any credentials, private datasets or unpublished working files not explicitly required for the public dashboard/site.

## Acceptance Criteria

- [x] Parent repo contains a `.gitmodules` entry for `public/gtpcnz`.
- [x] Parent repo status records `public/gtpcnz` as a submodule gitlink, not copied source.
- [x] `edithatogo/gtpcnz` contains only the minimal public file set on `main`.
- [x] Streamlit smoke test returns HTTP 200 locally.
- [x] Quarto renders successfully in a clean temp/cache environment.
- [x] GitHub Pages is configured for the public repo.
- [x] Any remote CI blocker is recorded with the concrete GitHub error.
