# Primary care funding series scorecard v1.8.1

Use this scorecard before scheduling or rescheduling a post in the Primary Care Funding Architecture series.

## Executable readiness gate

Run the local preflight before scheduling or rescheduling:

```powershell
python scripts/check_substack_publication_readiness.py --post 07 --post 10
python scripts/check_substack_schedule_contract.py
```

Current local preflight result for the two disputed candidates:

| Post | Series argument | Substack use | Images |
|---|---:|---:|---:|
| Post 07 | 50 / 50 | 50 / 50 | 10 / 10 |
| Post 10 | 50 / 50 | 50 / 50 | 10 / 10 |

These are local preflight scores. Final live readiness still requires checking the actual Substack draft body, image upload state and scheduled time in the editor or live draft payload.

## Series argument score: 50 / 50

| Criterion | Points | Current score | Notes |
|---|---:|---:|---|
| Clear public thesis | 10 | 10 | Schedule title must match the Markdown H1 and the body must carry the public argument. |
| Post stands alone | 10 | 10 | The public Markdown must be in the current main-post directory, not an appendix path. |
| Appendix separation | 10 | 10 | The post must link to the optional appendix without opening as appendix text. |
| Evidence boundaries | 10 | 10 | v1.8.1 model terms and a claim boundary must be present. |
| Series continuity | 10 | 10 | The post must include falsifiability and useful-links sections. |

## Substack use score: 50 / 50

| Criterion | Points | Current score | Notes |
|---|---:|---:|---|
| Title and subtitle fit Substack | 10 | 10 | Title and subtitle must sit within the local Substack length band. |
| Opening hook | 10 | 10 | The opening must have multiple public-facing paragraphs before technical framing. |
| Reader navigation | 10 | 10 | The post must include the appendix link and useful links. |
| Formatting rhythm | 10 | 10 | The post must use public-facing H2 sections and avoid H3 appendix-like structure. |
| Scheduling and publication hygiene | 10 | 10 | The schedule row must be ready and timezone-specific. |

## Image score: 10 / 10

| Criterion | Points | Current score | Notes |
|---|---:|---:|---|
| Relevance | 3 | 3 | The schedule must point to an existing hero image. |
| Substack preview value | 3 | 3 | The Markdown must point to an existing in-post image. |
| In-post explanatory value | 2 | 2 | Image alt text must describe the visual, not repeat a filename. |
| Accessibility | 2 | 2 | The image package must include the current visual set. |

## Post 10 resolution record

Post 10 has been repaired as a main-post draft rather than an appendix-only draft. Current source of truth:

1. Main post file:
   `docs/substack-ready/posts-v1.8.1-applied/post-10-accident-compensation-corporation-ambulance-and-urgent-care-the-hidden-upstream-system-v1.8.1-applied.md`
2. Optional appendix link only:
   `docs/substack-ready/appendices-v1.6.0/appendix-10-accident-compensation-corporation-ambulance-and-urgent-care-the-hidden-upstream-system-v1.6.0.md`
3. Live draft id:
   `197171867`
4. Latest live verification:
   the scheduled draft contains the main post title, public opening, restored in-body preview image, optional appendix link, public companion links, and v1.8.1 claim boundary.

## Post 07 resolution record

Draft id `197171855` maps to Post 07:
`The hospital salience game and the Health New Zealand allocation game`.

1. Main post file:
   `docs/substack-ready/posts-v1.8.1-applied/post-07-the-hospital-salience-game-and-the-health-new-zealand-allocation-game-v1.8.1-applied.md`
2. Optional appendix link only:
   `docs/substack-ready/appendices-v1.6.0/appendix-07-the-hospital-salience-game-and-the-health-new-zealand-allocation-game-v1.6.0.md`
3. Latest live verification:
   the published post contains the main post title, public opening, in-body figure, optional appendix link, public companion links, and v1.8.1 claim boundary.
