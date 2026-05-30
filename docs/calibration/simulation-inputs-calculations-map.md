# Simulation Inputs and Calculations Map

This document defines the mathematical, algorithmic, and data contracts for integrating the simulation suite: `kairos`, `voiage`, `mars`, and `innovate` into the primary care funding architecture benchmark.

---

## 1. Core Simulation Engine: `kairos` (Discrete Event / ABM)

`kairos` provides the high-performance Rust execution core for simulating patient-level demand, practice capacity, scope rules, and acute deflection.

### Inputs (Entity Component System State)
* **Patient Entities (`PatientComponent`):**
  * `patient_id`: Unique identifier (UUID).
  * `demographics`: Age group, sex, socio-economic deprivation quintile (NZDep).
  * `clinical_need`: Base morbidity rate, acute risk index.
  * `state`: Enrolled / Unenrolled.
* **Provider Entities (`ProviderComponent`):**
  * `provider_id`: Unique identifier.
  * `scope`: GP, Nurse Practitioner (NP), Registered Nurse (RN), Clinical Pharmacist.
  * `capacity`: Available hours per week, maximum appointment throughput.
  * `financials`: Marginal cost per consultation type, fixed overhead index.
* **Funding Context (`FundingComponent`):**
  * `marginal_activity_payment`: $0..X$ contribution per consult.
  * `capitation_base_rate`: Stable subscription income per enrolled patient.
  * `co_payment_protection`: Copay caps and subsidy eligibility flags.

### Calculations
* **Triage & Routing Logic:**
  $$\text{EncounterDemand}(t) \sim \text{Poisson}(\lambda_i(t))$$
  Where $\lambda_i(t)$ is the baseline encounter frequency adjusted for patient deprivation and acute severity.
* **Access Resolution:**
  $$\text{Resolved}(t) = \min(\text{EncounterDemand}(t), \text{ProviderCapacity}(t))$$
* **Deflection to Emergency Department (ED):**
  $$\text{Deflected}(t) = \text{EncounterDemand}(t) - \text{Resolved}(t)$$
  $$\text{EDPresentation}(t) = \text{Deflected}(t) \times \text{DeflectionProbability}(\text{Deprivation}, \text{CoPaymentLevel})$$

---

## 2. Value of Information (VOI) Analysis: `voiage`

`voiage` calculates the economic value of reducing uncertainty around key load-bearing model parameters (e.g., GP/NP scope substitution rates or patient deflection factors).

### Calculations
* **Expected Value of Perfect Information (EVPI):**
  $$\text{EVPI} = \mathbb{E}_{\theta} \left[ \max_{d \in D} U(d, \theta) \right] - \max_{d \in D} \mathbb{E}_{\theta} \left[ U(d, \theta) \right]$$
  Where $d$ is the policy decision (e.g., hybrid vs. status quo), $\theta$ represents the uncertain parameters, and $U(d, \theta)$ is the system welfare utility.
* **Expected Value of Sample Information (EVSI):**
  $$\text{EVSI} = \mathbb{E}_{X} \left[ \max_{d \in D} \mathbb{E}_{\theta \mid X} [U(d, \theta)] \right] - \max_{d \in D} \mathbb{E}_{\theta} \left[ U(d, \theta) \right]$$
  Where $X$ is a simulated sample data point (e.g., from an upcoming OIA response or practice costing study).
* **Expected Net Benefit of Sampling (ENBS):**
  $$\text{ENBS}(N) = \text{EVSI}(N) - \text{CostOfSampling}(N)$$

---

## 3. Metamodeling Emulator: `mars` (Regression Splines)

`mars` constructs a scikit-learn compatible Multivariate Adaptive Regression Splines emulator over the output of the computationally heavy `kairos` simulation.

### Calculations
* **MARS Basis Functions:**
  $$\hat{f}(x) = \beta_0 + \sum_{m=1}^M \beta_m B_m(x)$$
  Where each $B_m(x)$ is a basis function of the form:
  $$B_m(x) = \max(0, x - c) \quad \text{or} \quad B_m(x) = \max(0, c - x)$$
* **GCV (Generalized Cross-Validation) Pruning:**
  $$\text{GCV} = \frac{\frac{1}{N} \sum_{i=1}^N (y_i - \hat{f}(x_i))^2}{(1 - \frac{C(M)}{N})^2}$$
  Where $C(M)$ is the penalty for the number of basis functions in the model. This emulator runs in milliseconds inside the Streamlit dashboard app.

---

## 4. Policy and Scope Diffusion: `innovate`

`innovate` models how quickly primary care clinics transition to direct claiming, remote consult triage, and advanced scopes of practice.

### Calculations
* **Bass Diffusion Model for Adoption:**
  $$\frac{df(t)}{dt} = \left( p + q \frac{A(t)}{M} \right) (M - A(t))$$
  Where:
  * $A(t)$ is the cumulative number of adopting clinics.
  * $M$ is the total potential adopting population.
  * $p$ is the coefficient of innovation (external influence).
  * $q$ is the coefficient of imitation (internal network/peer influence).
