# Report, Docs, and Public Website Report

## Findings

The report/docs/public-website layer is unusually complete for a public explainer. It has:
- a homepage reading map
- a static Quarto report
- dashboard contract and audit docs
- calibration-readiness and model-card docs
- launch boundary notes
- mirrored public content under `public/gtpcnz`

The main strength is consistency: the same caveat language and public-data anchor appears across the homepage, report, deployment docs, and dashboard contract. The main weakness is fragmentation. There are many companion docs, but no single canonical “what is the public site now?” index beyond the broader repo structure.

## Evidence

- `index.qmd:12-31` provides the public reading map and visual gallery.
- `reports/primary_care_architecture.qmd:28-348` contains the static report, figure captions, and launch caveats.
- `docs/REPORTS-AND-DASHBOARD.md:1-45` describes how the report and dashboard fit together.
- `docs/STREAMLIT-DEPLOYMENT.md:1-45` records the deployment and public-boundary language.
- `docs/public-site/streamlit-dashboard-contract-v1.8.1.md:1-114` defines the dashboard contract.
- `docs/public-site/streamlit-dashboard-audit-v1.8.1.md:1-35` records the pass/fail audit.
- `docs/public-site/post-surface-crosswalk-contract-v1.8.2.md:1-57` maps posts to public surfaces.
- `public/gtpcnz/` mirrors the public site bundle, including the same report/docs tree.

## Completion Assessment

Substantially complete as a public reading system. Not fully complete as a single, tightly governed release artifact.

What is finished:
- public report exists
- homepage exists
- deployment and contract docs exist
- public caveats are aligned

What is incomplete:
- the public mirror duplicates content without a clear canonicalization layer
- there is no single generated release manifest for the whole site bundle
- the docs are informative, but not yet machine-enforced end to end
- some contracts still read like a project handbook rather than a release gate

## Bleeding-edge Recommendations

1. Generate a single release manifest that enumerates every public surface and its status.
2. Add a site map page that is generated from the repo metadata instead of maintained manually.
3. Add a public “what changed in this release” page that summarizes all document deltas.
4. Turn the audit and contract docs into machine-checked gates rather than advisory prose.
5. Collapse the mirrored public bundle into a reproducible publish step with one source of truth.

## Risks

- Multiple contract docs can drift apart.
- Mirrored `public/gtpcnz` content can diverge from the root site if publishing is manual.
- Readers may assume the docs imply calibration when they mostly describe readiness and boundaries.
- A lot of documentation can create the appearance of maturity without eliminating underlying scaffolding.
