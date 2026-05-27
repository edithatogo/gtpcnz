# Dependency Policy v1.8.3

GTPCNZ uses a three-lane dependency posture.

## Stable Release CI

The main CI workflow installs `requirements.txt`, runs the repo-health gate, runs concern-boundary checks, runs pytest, renders Quarto, and verifies the Streamlit entrypoint imports.

## Latest Canary CI

The dependency canary installs from `requirements.txt` with `--upgrade --upgrade-strategy eager -r requirements.txt`. It is scheduled and manually runnable. A failure in this lane means the next dependency refresh needs triage before release.

## Experimental Edge CI

The Conductor dependency-edge workflow defines the review process for trying newer library versions before they are promoted to `requirements.txt`.

## Streamlit

The public Streamlit app remains pinned to the stable release lane and must not depend on secrets or local-only assets.

## Quarto

The Quarto site must render in CI before Pages deployment.

## Dependabot

Dependabot watches GitHub Actions and pip dependencies weekly.
