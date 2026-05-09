# Remediation log — v1.2.1

## Issues found during contract-compliance audit

1. **README was stale.** It described v0.7.0 as the current release, even though the package had progressed to v1.2.0.
   - **Fix:** Rewrote README to describe v1.2.1, current package structure, Substack-ready layer, audit status and caveats.

2. **Conductor track index was stale.** It listed only early tracks in detail and did not clearly record later tracks.
   - **Fix:** Rewrote `conductor/tracks.md` to include tracks 001–018 and added track folders for Substack-ready publication and contract-compliance audit.

3. **Several local Markdown figure links were broken after files were copied into different folders.**
   - **Fix:** Repaired relative links in final report, MCDA report and complete Substack series. Automated local-link audit now reports zero broken local Markdown links.

4. **The v1.2.0 zip did not preserve `.git` history.**
   - **Fix:** v1.2.1 package is initialised as a git repository and packaged with `.git` included.

5. **Contract requirements were implicit rather than documented as acceptance criteria.**
   - **Fix:** Added `acceptance-criteria-matrix-v1.2.1.csv` and this audit report.

## Remaining limitations

- External URL live status was not exhaustively checked in this pass. The audit verifies hyperlink presence, format and local-reference integrity.
- Substack voice is close to the requested style, but still requires final Dylan sign-off.
- Modelling remains demonstrative and source-informed, not a fully calibrated predictive model.
- Stakeholder validation, OIA responses and rapid scoping review execution remain future work.
