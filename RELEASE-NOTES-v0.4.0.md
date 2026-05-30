# Release notes v0.4.0

## Release theme

v0.4.0 converts the high-level repeated-game concept into an explicit New Zealand policy-game map.

## Main additions

- `docs/concepts/nz-policy-game-atlas-v0.4.0.md`
- `docs/modelling/nz-game-theory-formalisation-v0.4.0.md`
- `docs/policy-briefs/brief-06-nz-game-theory-map-v0.4.0.md`
- `docs/nzmj/game-theory-methods-annex-v0.4.0.md`
- `docs/substack/post-09-the-nz-primary-care-funding-game-v0.4.0.md`
- `docs/source-notes-v0.4.0.md`
- `models/primarycare_model/nz_game_map.py`
- `models/tests/test_nz_game_map.py`
- `outputs/nz-policy-game-map-v0.4.0.docx`
- `outputs/nz-policy-game-map-v0.4.0.pdf`

## Summary

The release maps 14 component games:

1. Hospital-salience budget game.
2. Health NZ internal allocation game.
3. Capitation marginal-supply game.
4. Consumer access pathway game.
5. PHO intermediation game.
6. ACC/Health NZ cross-funder game.
7. Ambulance conveyance game.
8. Scope-of-practice supply game.
9. Telehealth/local-supply game.
10. Co-payment calibration game.
11. KPI salience game.
12. Equity and trust game.
13. Political economy game.
14. Data observability game.

The central claim is that New Zealand may be optimising allocation within tightly controlled upstream sectors while inadvertently channeling growth into hospitals. This is framed as a testable hypothesis for system dynamics, agent-based modelling, qualitative validation and policy analysis.

## Verification

- `PYTHONPATH=models pytest -q models/tests --disable-warnings` returned `18 passed`.
- The v0.4.0 DOCX was rendered using the DOCX render workflow and page images were visually checked.
- The v0.4.0 PDF was rendered using the PDF render workflow and page images were visually checked.
