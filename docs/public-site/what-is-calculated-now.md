# What this model calculates (and what it doesn't)

*Last updated: v1.7.2 — A plain-language guide for Streamlit users and public readers.*

---

## The short version

This model is a **public-data benchmark**, not a crystal ball. It compares different ways of funding primary care in Aotearoa New Zealand and shows the **logic** of each approach. It does not predict what will happen to real patients, real hospitals, or real budgets.

Think of it like a **flight simulator for policy ideas**: you can adjust the controls (sliders), see how the numbers change, and learn which settings matter most — but the simulator is not flying a real plane.

---

## What does the model calculate at runtime?

When you open the Streamlit app and start adjusting sliders, the model runs formulas to produce **five index scores**, each on a 0–100 scale:

| Score | What it means | A high score means... |
|---|---|---|
| **Access index** | How well people can get timely primary care | More access |
| **Supply generation** | Whether the funding settings attract and keep GPs and nurses | More workforce |
| **Hospital pressure** | How much hospital demand is avoided because upstream care is working | Less hospital pressure (lower is better) |
| **Gaming risk** | Risk of over-servicing, upcoding or claim manipulation | More risk (lower is better) |
| **Hybrid viability** | An overall score combining the above four | More viable hybrid model |

The formulas that turn your slider settings into these scores are **deterministic** — if you and a friend set the same sliders to the same positions, you get exactly the same numbers. No randomness, no guessing.

---

## Three ways to use the model

The app has three different modes, shown by a coloured badge at the top of each result.

### 🧪 Public-data anchored (blue badge)

**What happens**: You see pre-calculated tables using the default settings from the model's YAML registry. No sliders were moved.

**What it means**: Every number comes from published government data (capitation rates, population counts, fee schedules) or from research papers. This is the safest mode for public documents.

**Use it when**: You want to see the baseline comparison without changing anything.

### 📐 Deterministic — live calculation (green badge)

**What happens**: You move a slider — say, raise the capitation rate — and the model recalculates all five scores instantly.

**What it means**: The same slider position always gives the same result. The model is showing you the logical consequence of your assumptions, not a random simulation.

**Use it when**: You want to ask "what if" questions: *What if capitation were higher? What if governance were stronger?*

### 🎲 Stochastic demo (purple badge)

**What happens**: You enable one of the simulation engines (Monte Carlo, agent-based model, diffusion model). The model runs many times with small random variations and shows a range of possible outcomes (p05, p50, p95).

**What it means**: The *shape* of the distribution is a public-data anchored benchmark — it shows which direction the numbers tend to move — but the exact percentages are **demonstrative, not calibrated**. Think "the model leans toward this outcome" rather than "this outcome is 73% likely."

**Use it when**: You want to explore which assumptions have the widest range of possible consequences, or when testing the sensitivity of your preferred settings.

### 📚 Educational (orange badge)

**What happens**: You use simplified teaching levers with plain-language labels like "Shift more work to nurses" or "Raise the capitation rate a lot."

**What it means**: The formulas are deliberately simplified for teaching. The results show the general direction of an effect (e.g., "more funding to general practice reduces hospital pressure"), but the exact numbers should not be used for policy decisions.

**Use it when**: You are learning about primary care funding concepts for the first time, or explaining them to someone else.

---

## What is assumed vs. what is calculated

It helps to separate the **knobs you can turn** from the **numbers that come out**:

| You set these (assumptions) | The model calculates these (results) |
|---|---|
| Capitation rate per person | Access index |
| FFS consultation fee | Supply generation score |
| Copayment cap and waiver thresholds | Hospital pressure score |
| Governance and audit strength | Gaming risk score |
| Workforce participation rate | Hybrid viability score |
| Population size | Monte Carlo uncertainty ranges |
| Data visibility and transparency | ABM diffusion traces |
| Equity protection settings | Scenario rankings |

**Everything in the left column** has a default value from a public source (government website, published research, workforce survey). You can override any of them with the sliders.

**Everything in the right column** is calculated fresh each time you move a slider, using the same formulas the model always uses.

---

## The important caveat

This model is **public-data anchored and demonstrative**. It is **not**:

- A patient-level forecast
- Calibrated against linked hospital records
- A replacement for proper economic evaluation or clinical trials
- An endorsement by any government agency or health organisation

The model helps answer the question: **"Does this funding architecture make logical sense given what we know from public data?"**

It does not answer: **"How much money will this save?"** or **"How many hospital admissions will this prevent?"**

Those questions need real-world linked data, empirical calibration, and stakeholder validation — which is exactly the pathway this model prepares.

---

## Where the numbers come from

Every default value in the model is stored in a YAML registry file with its source documented:

| Registry file | What it contains | Source examples |
|---|---|---|
| `parameters.v1.yaml` | Capitation rates, FFS fees, copayment thresholds, workforce data | Ministry of Health GP capitation schedule, PHO Services Agreement, Statistics NZ |
| `inputs.v1.yaml` | Dataset definitions and privacy classifications | Ministry of Health data dictionaries |
| `scenarios.v1.yaml` | Pre-built scenario bundles for comparison | Defined by the model team |
| `educational_levers.v1.yaml` | Simplified teaching sliders with explanations | Defined by the model team |

The full details, including which evidence tier each parameter belongs to (public data, stakeholder input, linked-data calibration), are in the [model card](../calibration/model-card-v1.7.2.md).

---

## Want to learn more?

- **[Model card (detailed technical description)](../calibration/model-card-v1.7.2.md)** — Full specification of inputs, outputs, validation status, and what is calculated vs. assumed.
- **[Claim boundaries and public wording](../launch/claim-boundaries-v1.7.2.md)** — Rules for what to say (and not say) about model outputs.
- **[Architecture and strict validation](../design/concern-extraction-architecture-v1.8.3.md)** — How the model is built to prevent mistakes, with diagrams and layer descriptions.


