# Spec: Post-to-Surface Crosswalk Contract

## Problem

The public visual contract maps themes to surfaces, but implementation needs a binding post-by-post map. Without it, Quarto, Streamlit and GitHub Pages can drift into different structures, and game-theory posts can remain implied rather than surfaced.

## Goal

Create and maintain a crosswalk that maps each public post or referenced game-theory appendix to:

- Quarto report section or anchor;
- Streamlit page, tab or module;
- GitHub Pages card, gallery item or report link;
- required static visual;
- required dynamic visual, toy module or simulation;
- status label and caveat;
- responsible implementation track.

## Scope

In scope:

- `docs/public-site/post-surface-crosswalk-contract-v1.8.2.md`;
- Track 029 cross-references;
- dashboard/report/site contract cross-references;
- tests or document checks that prove the crosswalk exists and contains required rows.

Out of scope:

- editing Substack post bodies;
- implementing the Quarto, Streamlit or GitHub Pages UI changes;
- adding private Substack drafts to the public repo.

## Requirements

1. The crosswalk must include posts 01-06.
2. It must include a game-theory extension table for later posts/appendices referenced by the public surfaces.
3. Post 04 must have a named game-theory Quarto destination and Streamlit game-theory lab destination.
4. Microeconomics posts must have both static and dynamic visual requirements.
5. The contract must state that public surfaces may use post titles/reading-guide references but must not copy private Substack working drafts into the public repo.
6. Each row must identify the implementation track that owns delivery.
7. The contract must be linked from Track 029 and the dashboard contract.

## Parallelisation

This track can run in parallel with Track 035 visual/simulation specification after the first crosswalk draft exists.

Suggested subagent split:

- Subagent A: verify first-six post titles and reader questions from repo-local post inventory.
- Subagent B: verify game-theory appendices/posts that need companion modules.
- Main agent: maintain the contract file and registration surfaces.

## Acceptance Criteria

1. `docs/public-site/post-surface-crosswalk-contract-v1.8.2.md` exists.
2. The contract contains posts 01-06.
3. The contract contains a game-theory extension table.
4. Track 029 references the contract.
5. Streamlit dashboard contract references the contract.
6. Validation confirms the required post rows, game-theory terms and implementation track references are present.
