# Release Engineering

Release artifacts must include source snapshot hash, parameter hash, model hash, output hash, test status, visual-regression status, and accessibility status.

## Release-note handling

Forward release notes are handled through GitHub Releases and `CHANGELOG.md`, not new root-level `RELEASE-NOTES-v*.md` files.

- Policy: [bleeding-edge-sota-release-handling.md](bleeding-edge-sota-release-handling.md)
- Historical archive: [archive/README.md](archive/README.md)
- GitHub generated-release configuration: [.github/release.yml](../../.github/release.yml)

SOTA/bleeding-edge release language must remain claim-gated and public-only. It cannot imply linked-data calibration, patient-level forecasts, private administrative inputs, or precise causal/fiscal/workforce/hospital impacts unless the relevant release gates pass.
