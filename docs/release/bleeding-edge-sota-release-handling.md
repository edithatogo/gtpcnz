# Bleeding-edge/SOTA release-note handling

GTPCNZ release notes are governed by the same public-only, claim-gated posture as the model surfaces.

## Current policy

- GitHub Releases are the public release-note surface for tagged releases.
- `CHANGELOG.md` is the durable repo history and should keep a concise, human-readable summary by version.
- `docs/release/` holds release evidence: model cards, release manifests, templates, readiness notes, and the historical release-note archive.
- Root-level `RELEASE-NOTES-v*.md` files are no longer the forward pattern.
- Historical release notes are retained under `docs/release/archive/` for traceability.

## Required release-note claims

Every forward release note should state:

- Claim level.
- Calibration status.
- Source snapshot or release manifest reference.
- Not-valid-for boundaries.
- Test and release-gate status.
- Whether SOTA/bleeding-edge status is controlled, partial, or not claimed.

## GitHub release categories

`.github/release.yml` maps PR labels into release-note sections:

- Public-only SOTA and calibration gates.
- Model, uncertainty, and VOI.
- Streamlit cockpit and visual grammar.
- Release engineering and reproducibility.
- Documentation and claim boundaries.
- Other changes.

## SOTA/bleeding-edge boundary

SOTA/bleeding-edge language is permitted only when it remains bounded by the scorecard and public-only gates. It must not imply linked-data calibration, patient-level forecasting, private administrative inputs, precise fiscal savings, ED reductions, hospital-demand reductions, workforce effects, implementation impacts, or causal effects unless the relevant release gates pass.
