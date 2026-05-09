# Research audit dossier v0.5.0

## Audit purpose

This dossier documents whether the New Zealand primary care, ambulance and hospital funding game map is ready to move from conceptual mapping to empirical validation.

The answer is **yes, with explicit limits**. The mapping is now traceable, falsifiable and ready for review. It is not yet empirically proven.

## Core audit question

Can a reviewer follow the pathway from policy thesis to:

1. mapped policy games;
2. explicit claims;
3. source or theory basis;
4. assumptions requiring testing;
5. candidate data sources;
6. modelling parameters;
7. stakeholder validation questions;
8. policy outputs?

## Audit conclusion

The repo now supports an affirmative answer at the **conceptual and protocol stage**. It demonstrates:

- a defined policy thesis;
- a 14-game New Zealand policy-game atlas;
- a claim register with source links and evidence levels;
- formal game-theory and simulation specifications;
- an artefact manifest and lineage graph;
- a falsification register;
- a source-quality log;
- a stakeholder validation plan;
- review and modelling reporting-standard crosswalks.

The current work should be described as a **structured, source-traceable, falsifiable policy hypothesis**, not as a completed empirical study.

## What has been audited

| Domain | Artefact | Current status |
|---|---|---|
| Thesis | `docs/concepts/core-thesis-v0.1.0.md`; `docs/concepts/nz-policy-game-atlas-v0.4.0.md` | Stable enough for review |
| Game map | `docs/modelling/nz-policy-game-map-v0.4.0.md`; `docs/modelling/game-mapping-matrix-v0.4.0.csv` | Complete conceptual map |
| Formalisation | `docs/modelling/nz-game-theory-formalisation-v0.4.0.md`; `docs/modelling/formal-game-theory-model-nz-v0.4.0.md` | Structural model; not estimated |
| Policy translation | Briefs 01–06; Substack drafts | Usable as discussion documents |
| Review readiness | Review protocol, search strategy, PRISMA-ScR crosswalk | Protocol stage |
| Simulation readiness | STRESS crosswalk, ODD template, parameter inventory | Specification stage |
| Stakeholder validation | Interview guides, sampling frame | Ready to deploy after ethics/governance decision |
| Source traceability | Claim-to-source ledger and source registry | Usable, needs Zotero/BibTeX expansion |

## Claim maturity levels

| Level | Label | Meaning | How to handle in writing |
|---:|---|---|---|
| 1 | Publicly documented fact | Directly supported by official or peer-reviewed source | State directly with citation |
| 2 | Established theory | Supported by standard economic/game-theoretic theory | State as theory-based mechanism |
| 3 | Plausible mechanism | Supported by theory plus partial setting-specific evidence | Present as hypothesis requiring testing |
| 4 | Modelling assumption | Needed for simulation structure | State as assumption/sensitivity variable |
| 5 | Policy option | Normative or design proposal | Present as option, not conclusion |

## Audit-risk summary

The highest audit risks are not missing files; they are unresolved empirical questions:

1. **Materiality of ACC revenue** to general practice viability and non-injury supply.
2. **Magnitude of PHO transaction cost** and whether it deters market entry.
3. **Elasticity of multidisciplinary supply** if benefits are opened to scope-eligible providers.
4. **Price elasticity and equity effects** of co-payment settings by deprivation, rurality, ethnicity, age and multimorbidity.
5. **Conversion rate of unmet primary care need** into ambulance use, ED presentations, ambulatory-sensitive hospitalisation and avoidable admissions.
6. **Behavioural effect of KPI elevation** on management attention, resource allocation and gaming.
7. **Fiscal risk** if a demand-driven schedule expands low-value activity faster than it substitutes for hospital demand.

## Recommended audit statement for reports

> This mapping is a structured policy hypothesis derived from public documents, established economic theory and explicit modelling assumptions. Its purpose is to make the funding architecture problem testable. The map should not be read as empirical proof that any one reform will reduce hospital demand; that claim requires evidence synthesis, stakeholder validation, linked-data analysis and simulation calibration.

## Next-stage evidence products

The next version should produce:

1. a PRISMA-ScR evidence map;
2. an OIA response bundle;
3. a stakeholder validation summary;
4. a synthetic-parameter system dynamics model;
5. an ODD-described agent-based model prototype;
6. a scenario comparison brief distinguishing allocation reform from supply-architecture reform.
