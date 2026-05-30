# ODD protocol template — primary care funding ABM v0.5.0

## 1. Overview

### Purpose

To simulate how patients, providers, PHOs/intermediaries, ambulance providers and funders respond to alternative primary care funding architectures.

### Entities, state variables and scales

**Patients**: age, sex, ethnicity, deprivation, rurality, multimorbidity, urgency, price sensitivity, digital access, enrolment status, trust/preference, ACC eligibility.

**Providers**: provider type, scope, clinical governance eligibility, contact capacity, cost structure, co-payment setting, benefit eligibility, rurality, telehealth capability, open-book status.

**Intermediaries/locality entities**: PHO/locality support, payment intermediation cost, quality-improvement function, data support, population-health outreach.

**Funders**: Health NZ, ACC, Ministry/Treasury rule-setter, optional payment platform.

**Hospitals/EDs**: ED congestion, admission threshold, ambulatory-sensitive admission rate, waiting pressure.

### Process overview and scheduling

Each period:

1. Patients generate need.
2. Patients choose pathway: primary care, telehealth, pharmacy/allied health, ambulance, ED, delay/no care.
3. Providers allocate capacity by contact type and payment margin.
4. Ambulance encounters resolve, convey or refer.
5. Unmet need evolves and may convert to ED/admission pressure.
6. Funders update payment, targets and auditing rules in scenario-specific ways.
7. Provider viability and market entry/exit update.

## 2. Design concepts

- **Basic principles**: marginal supply, congestion, price signal, principal-agent problems, transaction cost, hospital salience.
- **Emergence**: hospital pressure emerges from individual access choices, provider capacity and ambulance disposition.
- **Adaptation**: providers adjust capacity and enrolment/open-book status based on viability and workload.
- **Objectives**: patients maximise timely, affordable, trusted care; providers balance viability, workload and clinical obligations; funders balance fiscal control, access, equity and hospital pressure.
- **Learning**: optional in later versions; not included in MVP.
- **Prediction**: agents use current wait times, co-payments and availability.
- **Sensing**: patients observe price, availability, distance/travel and perceived urgency; funders observe measured KPIs.
- **Interaction**: patients compete for provider slots; providers respond to payment rules; ambulance interacts with ED.
- **Stochasticity**: need generation, pathway choice and conversion to hospital use.
- **Collectives**: practices/teams, PHOs/localities, rural communities.
- **Observation**: access, co-payment, unmet need, equity gradients, ambulance conveyance, ED demand, hospital pressure.

## 3. Details

### Initialisation

Initialise with baseline NZ population and provider distribution once data are available. Synthetic distributions may be used only for structural testing.

### Input data

See `docs/modelling/model-parameter-inventory-v0.5.0.csv`.

### Submodels

1. Need generation.
2. Contact-type eligibility.
3. Patient pathway choice.
4. Provider supply response.
5. Ambulance disposition.
6. Hospital pressure conversion.
7. Equity and affordability outcomes.
8. Funder/payment updates.
