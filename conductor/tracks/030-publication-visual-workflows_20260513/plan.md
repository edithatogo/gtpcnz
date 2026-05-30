# Plan: Publication Visual Workflows and Reusable Skills

Status: Complete.

## Phase 1: Repo-local skills

1. Add `docs/skills/diagram-production-skill.md`.
2. Add `docs/skills/microeconomics-diagram-skill.md`.
3. Add `docs/skills/substack-thumbnail-skill.md`.
4. Add `docs/skills/figure-metadata-accessibility-skill.md`.
5. Add `docs/skills/hyperlink-placement-skill.md`.
6. Add `docs/skills/table-preservation-skill.md`.
7. Add `docs/skills/substack-rich-content-skill.md`.

## Phase 2: Workflows

1. Add `docs/workflows/visual-production-workflow.md`.
2. Add `docs/workflows/substack-post-packaging-workflow.md`.
3. Add `docs/workflows/public-visual-release-workflow.md`.
4. Link workflows from `conductor/workflow.md`.
5. Cross-link Track 029 and Track 030.

## Phase 3: Audits and checks

1. Define a figure manifest schema with:
   - image path;
   - source path;
   - alt text;
   - Substack caption;
   - Quarto caption;
   - status label;
   - post/report/dashboard target;
   - source-confidence label.
2. Define a hyperlink audit:
   - end-only links;
   - missing inline funding-type links;
   - repeated links that create clutter;
   - source-confidence mismatch.
3. Define a table audit:
   - preserved tables;
   - converted cards;
   - converted bullets;
   - rationale for conversion.

## Phase 4: Implementation handoff

1. Use these workflows when implementing Track 029.
2. Update Substack-ready QA reports to require:
   - thumbnails;
   - alt text;
   - proper image captions;
   - inline source links;
   - table conversion notes;
   - formula/LaTeX checks.
3. Add covering-note checks requiring each scheduled post to have a same-time scheduled Note, no more than three sentences, with the canonical post URL.
4. Add Substack settings checks requiring each post, including already published posts, to have series/topic tags plus SEO and social metadata.
5. Add automated checks where feasible after the first manual pass.

## Validation

This track is a workflow/design track. Validation is document-level:

```bash
rg -n "alt text|caption|thumbnail|inline link|table|LaTeX|formula|SEO|tag" docs/skills docs/workflows conductor/tracks/030-publication-visual-workflows_20260513
```

Implementation validation belongs to Track 029 and later public-site commits.
