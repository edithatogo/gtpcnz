# Formula Appendix v1.8.5

Cross-reference of all model formulae with code links.

---

## Index Formulae

Computed in `calculate_indices()` at [runtime_lab.py:L110](../../models/primarycare_model/runtime_lab.py#L110).

### 1. Hybrid Viability Index
**Code:** [runtime_lab.py:L134-142](../../models/primarycare_model/runtime_lab.py#L134)
```
hybrid = 0.24*Supply + 0.18*Access + 0.18*Equity + 0.16*Governance
       + 0.14*Deflection + 0.06*(100-FiscalRisk) + 0.04*(100-GamingRisk)
```
**Components:** Supply (24%), Access (18%), Equity (18%), Governance (16%), Deflection (14%), Fiscal Risk inv (6%), Gaming Risk inv (4%)

### 2. Supply Generation Index
**Code:** [runtime_lab.py:L126](../../models/primarycare_model/runtime_lab.py#L126)
```
supply = 100 * (0.34*Activity + 0.18*Capitation + 0.24*Scope + 0.12*Urgent + 0.12*Place - 0.12*Budget)
```

### 3. Access Index
**Code:** [runtime_lab.py:L127](../../models/primarycare_model/runtime_lab.py#L127)
```
access = 100 * (0.42*(Supply/100) + 0.18*Urgent + 0.15*Equity + 0.12*Place + 0.10*Data - 0.16*Copay)
```

### 4. Equity Legitimacy Index
**Code:** [runtime_lab.py:L128](../../models/primarycare_model/runtime_lab.py#L128)
```
equity = 100 * (0.34*Equity + 0.24*Place + 0.16*Capitation + 0.14*Data - 0.16*Copay)
```

### 5. Governance Resilience Index
**Code:** [runtime_lab.py:L129](../../models/primarycare_model/runtime_lab.py#L129)
```
governance = 100 * (0.44*Governance + 0.20*Data + 0.18*Place + 0.10*Equity + 0.08*Capitation)
```

### 6. Hospital Deflection Index
**Code:** [runtime_lab.py:L130](../../models/primarycare_model/runtime_lab.py#L130)
```
deflection = 100 * (0.32*(Access/100) + 0.22*Urgent + 0.16*(Supply/100) + 0.16*Data + 0.14*Place - 0.10*Complexity)
```

### 7. Gaming Risk Index
**Code:** [runtime_lab.py:L131](../../models/primarycare_model/runtime_lab.py#L131)
```
gaming = 100 * (0.35*Activity + 0.18*Scope + 0.18*Complexity - 0.30*Governance - 0.18*Data - 0.16*Place)
```

### 8. Fiscal Risk Index
**Code:** [runtime_lab.py:L132](../../models/primarycare_model/runtime_lab.py#L132)
```
fiscal = 100 * (0.22*Activity + 0.18*(Gaming/100) + 0.16*Complexity + 0.14*(1-Budget) - 0.18*Governance - 0.14*(Deflection/100))
```

### 9. Hospital Pressure Index
**Code:** [runtime_lab.py:L133](../../models/primarycare_model/runtime_lab.py#L133)
```
hp = 100 * (0.34*HospSal + 0.26*(1-Deflection/100) + 0.16*Complexity + 0.14*Budget - 0.18*(Access/100) - 0.12*Urgent)
```

---

## Shared Helpers

**Code:** [runtime_lab.py:L28-38](../../models/primarycare_model/runtime_lab.py#L28)
```
clamp(v, lo=0, hi=100) -> max(lo, min(hi, v))
diminishing_return(v, rate=2.4) -> (1 - exp(-rate*v)) / (1 - exp(-rate))
strategic_response(v, threshold, s) -> 1 / (1 + exp(-s * (v - threshold)))
```

## Educational Explainer

**Code:** [scenario_service.py:L185-240](../../models/primarycare_model/scenario_service.py#L185)

Uses sigmoid activation: `100 * strategic_response(weighted_input, threshold, steepness)`

## Sensitivity Adapter

**Code:** [sensitivity_adapter.py:L77-116](../../models/primarycare_model/engines/sensitivity_adapter.py#L77)

Identical index formulae, replicated for engine isolation.

---

## Parameter Definitions (13 scenario parameters, 0-100)

**Code:** [contracts/scenarios.py:L14-35](../../models/primarycare_model/contracts/scenarios.py#L14)

| Parameter | Description | Effect |
|---|---|---|
| activity_signal | Marginal payment strength | Higher = more supply |
| capitation | Enrolled-population base funding | Higher = more stability |
| place_accountability | Whole-population responsibility | Higher = less cherry-picking |
| scope_capacity | Workforce scope flexibility | Higher = more supply channels |
| urgent_ambulance | Urgent/ambulance alternatives | Higher = less hospital pressure |
| data_visibility | Encounter/outcome data | Higher = better governance |
| governance | Audit, rules, clinical governance | Higher = less gaming |
| equity_protection | Equity and copayment protections | Higher = fairer access |
| copayment_burden | Patient out-of-pocket cost | Higher = more barriers |
| budget_tightness | Fiscal constraint | Higher = more pressure |
| hospital_salience | Hospital pressure visibility | Higher = more reactive |
| complexity | Clinical/demographic complexity | Higher = more demand |
