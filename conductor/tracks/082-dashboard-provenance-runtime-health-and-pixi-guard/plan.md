# Plan

1. Define a chart/run provenance schema and add service helpers for provenance payloads.
2. Render provenance panels in Dash chart sections without overwhelming the main reading flow.
3. Add deployment/runtime health route or footer panel using safe environment variables only.
4. Add Pixi guard script/test that identifies Prefix.dev Pixi versus the Pixiv downloader.
5. Update deployment docs with the expected Pixi command and fallback behavior.
6. Run Dash, release-engineering, claim-boundary, public-only, and concern-boundary gates.

## Implementation Notes

- Prefer environment variables such as `GIT_SHA`, `APP_VERSION`, and `BUILD_TIME` when present.
- Never print or store tokens.
- Health status should be operational metadata, not evidence of model validity.
