"""Full parameterisation scaffold for the primary care funding architecture model, v1.7.0.

This module moves the project from a small source-informed parameterised model to a
fully specified parameterisation framework. It is still not a real-data calibrated
predictive model: the parameter values remain priors/placeholders until linked NZ data,
OIA releases, provider payment data and stakeholder-scored inputs are available.

What is new in v1.7.0:
- a broader parameter register covering demand, supply, funding, governance, ambulance,
  hospital, equity, risk and implementation;
- a data-input contract linking each parameter family to real-world data needed later;
- scenario override matrices for the current reform path and alternative hybrid options;
- a monthly dynamic model with all levers explicitly parameterised;
- sensitivity analysis and calibration-target matrices for future empirical work.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass, replace
from typing import Dict, Iterable, Mapping, Sequence
import math

import numpy as np
import pandas as pd


def clamp(value: float, lower: float = 0.0, upper: float = 1.0) -> float:
    return float(max(lower, min(upper, value)))


@dataclass(frozen=True)
class ParameterSpec:
    parameter_id: str
    name: str
    domain: str
    description: str
    unit: str
    current_value: float
    lower_bound: float
    upper_bound: float
    source_status: str
    source_or_basis: str
    real_data_needed: str
    estimation_strategy: str
    priority: str


@dataclass(frozen=True)
class DataInputSpec:
    input_id: str
    table_name: str
    level: str
    required_fields: str
    model_use: str
    likely_source: str
    access_route: str
    sensitivity_if_missing: str


@dataclass(frozen=True)
class ScenarioSpec:
    scenario_id: str
    name: str
    description: str
    overrides: Mapping[str, float]


PARAMETER_SPECS: tuple[ParameterSpec, ...] = (
    # Demand and need
    ParameterSpec("D01", "base_need_per_1000", "demand", "Underlying monthly primary-care-relevant need per 1,000 population before access constraints.", "contacts/1000/month", 62.0, 35.0, 100.0, "placeholder prior", "Needs NPCD/NZ Health Survey/encounter data", "Monthly encounters, unmet need, population denominators", "Estimate from encounter data plus unmet-need surveys by locality", "high"),
    ParameterSpec("D02", "urgent_need_share", "demand", "Share of primary-care-relevant need that is urgent/same-day or after-hours sensitive.", "proportion", 0.28, 0.10, 0.50, "placeholder prior", "Needs urgent-care/appointment data", "Booking urgency, after-hours encounters, ED substitutable care", "Multinomial demand model by urgency and patient group", "high"),
    ParameterSpec("D03", "routine_need_share", "demand", "Share of need that is routine or planned rather than urgent.", "proportion", 0.42, 0.25, 0.70, "derived prior", "Complements urgent/chronic shares", "Appointment type and reason-for-visit coding", "Estimate from appointment/encounter coding", "medium"),
    ParameterSpec("D04", "chronic_need_index", "demand", "Relative chronic and multimorbidity demand load.", "0-1 index", 0.55, 0.10, 0.95, "source-informed prior", "Capitation reweighting identifies multimorbidity as relevant", "Multimorbidity counts, LTC registers, medication/diagnosis proxies", "Hierarchical need model", "high"),
    ParameterSpec("D05", "rurality_demand_modifier", "demand/equity", "Additional access load or complexity caused by rurality and travel constraints.", "0-1 index", 0.45, 0.05, 0.95, "source-informed prior", "Rurality included in reweighting", "Rurality classification, travel time, provider proximity", "Geospatial access model", "high"),
    ParameterSpec("D06", "deprivation_demand_modifier", "demand/equity", "Additional need/access burden related to socioeconomic deprivation.", "0-1 index", 0.55, 0.05, 0.95, "source-informed prior", "Deprivation included in reweighting", "NZDep, unmet need, ED and admission outcomes", "Stratified demand and outcome model", "high"),
    ParameterSpec("D07", "multimorbidity_demand_modifier", "demand/equity", "Extra contact intensity required for multimorbidity beyond average need.", "0-1 index", 0.55, 0.05, 0.95, "source-informed prior", "Multimorbidity included in reweighting", "Condition counts, polypharmacy, hospital risk", "Regression/latent risk model", "high"),
    ParameterSpec("D08", "price_elasticity_general", "demand/price", "How strongly general patients reduce primary care use when co-payments increase.", "elasticity index", 0.24, 0.01, 0.80, "placeholder prior", "Needs fee/utilisation variation", "Practice fees, CSC/VLCA status, utilisation changes", "Discrete-choice or panel utilisation model", "high"),
    ParameterSpec("D09", "price_elasticity_high_need", "demand/equity", "How strongly high-need groups reduce or delay care when co-payments increase.", "elasticity index", 0.34, 0.01, 0.90, "placeholder prior", "NZ Health Survey reports cost barriers by group", "Fees and utilisation by ethnicity/deprivation/rurality/morbidity", "Stratified elasticity model", "high"),
    ParameterSpec("D10", "telehealth_acceptability", "demand/digital", "Share of demand that can realistically be met by telehealth without undermining care quality.", "0-1 index", 0.42, 0.05, 0.90, "placeholder prior", "Needs digital primary care data", "Mode of consultation, outcome, re-presentation", "Substitution/complementarity model", "medium"),
    ParameterSpec("D11", "unmet_need_persistence", "demand dynamics", "Persistence of unmet need from one month to the next.", "0-1 index", 0.68, 0.10, 0.95, "placeholder prior", "Needs longitudinal access data", "Delayed care, repeat attempts, ED conversion", "Dynamic panel/hazard model", "high"),
    ParameterSpec("D12", "delay_complexity_growth", "demand dynamics", "Rate at which delayed care becomes more complex or costly.", "0-1 index", 0.22, 0.01, 0.70, "placeholder prior", "Needs linked access-to-hospital data", "Waiting time to ED/admission/acuity", "Hazard/competing risk model", "high"),

    # Supply and workforce
    ParameterSpec("S01", "gp_capacity_index", "supply", "General practitioner capacity relative to population need.", "0-1 index", 0.48, 0.05, 0.95, "placeholder prior", "Needs workforce/FTE/open-book data", "GP FTE, sessions, appointment slots", "Workforce supply model", "high"),
    ParameterSpec("S02", "nurse_np_capacity_index", "supply", "Nurse and nurse practitioner capacity available for claimable primary activity.", "0-1 index", 0.42, 0.05, 0.95, "placeholder prior", "Needs workforce/FTE data", "NP/nurse FTE and scope of activity", "Workforce/scope supply model", "high"),
    ParameterSpec("S03", "pharmacist_capacity_index", "supply/scope", "Pharmacist capacity for eligible primary medical or protocolised contacts.", "0-1 index", 0.36, 0.00, 0.90, "placeholder prior", "Needs pharmacy workforce/scope data", "Pharmacy locations, FTE, prescribing services", "Scope-enabled supply model", "medium"),
    ParameterSpec("S04", "allied_health_capacity_index", "supply/scope", "Allied health capacity for eligible musculoskeletal, mental health or chronic-care contacts.", "0-1 index", 0.36, 0.00, 0.90, "placeholder prior", "Needs allied workforce data", "Physio, psychology, counselling, other FTE/activity", "Scope-enabled supply model", "medium"),
    ParameterSpec("S05", "paramedic_alt_capacity_index", "supply/ambulance", "Paramedic or extended-care paramedic capacity for alternative disposition/treat-and-refer pathways.", "0-1 index", 0.28, 0.00, 0.90, "placeholder prior", "Needs ambulance workforce and pathway data", "Paramedic workforce, alternative pathway activity", "Ambulance pathway capacity model", "high"),
    ParameterSpec("S06", "medical_productivity_per_fte", "supply", "Relative monthly contacts generated per medical FTE under current settings.", "0-1 index", 0.56, 0.10, 0.95, "placeholder prior", "Needs FTE/contact linkage", "Appointments per FTE, session templates", "Productivity regression by practice type", "high"),
    ParameterSpec("S07", "np_nurse_productivity_per_fte", "supply", "Relative contacts generated per nurse/NP FTE when claimable and governed.", "0-1 index", 0.48, 0.10, 0.95, "placeholder prior", "Needs FTE/contact linkage", "NP/nurse consultations, protocol care", "Productivity/scope model", "high"),
    ParameterSpec("S08", "scope_substitution_rate", "supply/scope", "Proportion of GP-bottlenecked contacts that can be safely shifted to other providers within scope.", "0-1 index", 0.30, 0.00, 0.80, "placeholder prior", "Needs clinical pathway/safety evidence", "Contact type, provider type, safety outcomes", "Classification + safety validation", "high"),
    ParameterSpec("S09", "workforce_exit_rate", "supply dynamics", "Monthly risk of provider/practice capacity exit under financial/workload stress.", "0-1 index", 0.12, 0.00, 0.60, "placeholder prior", "Needs workforce/practice exit data", "Closures, reduced sessions, retirement/exit", "Discrete-time hazard model", "medium"),
    ParameterSpec("S10", "market_entry_response", "supply dynamics", "Provider/practice entry or expansion response to clear activity-sensitive payment rules.", "0-1 index", 0.22, 0.00, 0.85, "placeholder prior", "Needs new entrant/PHO/provider data", "New practices, new PHOs, direct claim onboarding", "Entry/expansion model", "medium"),
    ParameterSpec("S11", "local_inperson_constraint", "rural/supply", "Constraint on local in-person capacity, especially rural or under-served settings.", "0-1 index", 0.68, 0.00, 0.95, "source-informed prior", "Rurality/access issues recognised in policy", "Rural session availability, travel time, closures", "Geospatial supply model", "high"),
    ParameterSpec("S12", "rural_loading_response", "rural/supply", "Supply response to rural/local in-person loading or higher scheduled benefits.", "0-1 index", 0.24, 0.00, 0.85, "placeholder prior", "Needs payment variation/pilot", "Rural payment changes and sessions/appointments", "Difference-in-differences/pilot evaluation", "high"),

    # Funding and payment architecture
    ParameterSpec("F01", "capitation_base_strength", "funding", "Strength of baseline capitation for continuity/population accountability.", "0-1 index", 0.70, 0.00, 0.95, "public architecture prior", "Capitation is core GP funding", "Capitation amounts and enrolments", "Payment-flow model", "high"),
    ParameterSpec("F02", "capitation_weighting_adequacy", "funding/equity", "Adequacy of capitation weightings for current population need.", "0-1 index", 0.38, 0.00, 0.95, "source-informed prior", "Current reweighting work recognises formula limitations", "Current/proposed rate tables and practice impacts", "Formula/revenue modelling", "high"),
    ParameterSpec("F03", "scheduled_medical_benefit_strength", "funding/FFS", "Strength of uncapped scheduled fee-for-service benefit for eligible primary medical contacts.", "0-1 index", 0.08, 0.00, 0.95, "policy option prior", "No general MBS-equivalent stream currently assumed", "Item schedule, contact categories and public contribution", "Policy schedule + claims modelling", "high"),
    ParameterSpec("F04", "scheduled_benefit_price_adequacy", "funding/FFS", "Adequacy of item prices/public contribution relative to marginal cost.", "0-1 index", 0.10, 0.00, 0.95, "policy option prior", "Needs service costing", "Consult costs, provider time, overhead, co-payment", "Costing and provider supply model", "high"),
    ParameterSpec("F05", "activity_signal_strength", "funding/FFS", "Marginal revenue signal attached to providing the next clinically necessary contact.", "0-1 index", 0.20, 0.00, 0.95, "source-informed prior", "ACC/programmes/co-payments create partial signals", "Marginal payment by contact type", "Payment elasticity model", "high"),
    ParameterSpec("F06", "patient_copayment_level", "funding/price", "Average private co-payment burden affecting demand.", "0-1 index", 0.58, 0.00, 0.95, "source-informed prior", "Cost barriers publicly reported", "Practice fee schedules and patient payment data", "Price elasticity model", "high"),
    ParameterSpec("F07", "copayment_protection_strength", "equity/price", "Strength of fee caps/subsidies/exemptions for children, high-need and low-income groups.", "0-1 index", 0.44, 0.00, 0.95, "source-informed prior", "CSC/VLCA/subsidy architecture exists", "Eligibility, fees, utilisation by group", "Equity-weighted price model", "high"),
    ParameterSpec("F08", "acc_activity_strength", "ACC/funding", "Extent to which ACC activity/contract payments sustain upstream provider capacity.", "0-1 index", 0.55, 0.00, 0.95, "hypothesis prior", "ACC treatment payment architecture exists", "ACC claims/payments by provider/practice", "Cross-funder revenue model", "high"),
    ParameterSpec("F09", "acc_constraint_intensity", "ACC/funding", "Degree of constraint or tightening in ACC activity funding.", "0-1 index", 0.12, 0.00, 0.95, "hypothesis prior", "Potential future policy lever", "Pricing changes, contract changes, claim acceptance", "Policy-shock model", "medium"),
    ParameterSpec("F10", "pho_transaction_cost", "PHO/admin", "Administrative friction or pass-through opacity from PHO-mediated streams.", "0-1 index", 0.52, 0.00, 0.95, "source-informed hypothesis", "PHO transparency issues identified as source target", "PHO financials, pass-through, onboarding delay", "Transaction-cost analysis", "high"),
    ParameterSpec("F11", "direct_claiming_strength", "admin/payment", "Strength of direct provider claims platform/rules-based payment architecture.", "0-1 index", 0.12, 0.00, 0.95, "policy option prior", "Current system lacks broad direct primary medical claims platform", "Claims infrastructure, processing cost, provider uptake", "Administrative cost-effectiveness model", "high"),
    ParameterSpec("F12", "place_based_accountability_strength", "commissioning", "Population/geographic accountability that prevents cherry-picking under demand-led benefits.", "0-1 index", 0.42, 0.00, 0.95, "source-informed policy prior", "Place-based commissioning raised as important guardrail", "Locality responsibility, outreach, hard-to-reach service targets", "Commissioning/accountability model", "high"),
    ParameterSpec("F13", "budget_tightness", "fiscal", "Constraint imposed by fixed envelopes/baselines/deficit pressure on upstream care.", "0-1 index", 0.76, 0.00, 0.95, "source-informed prior", "Separate appropriations exist but fiscal pressure remains", "Vote/baseline movements and budget decisions", "Fiscal-flow model", "high"),
    ParameterSpec("F14", "global_cap_constraint", "fiscal", "Strength of global cap/fixed envelope on eligible primary medical activity.", "0-1 index", 0.82, 0.00, 0.95, "policy hypothesis prior", "Capitation/fixed pools constrain marginal activity", "Funding envelope, claims cap rules, waiting/rationing outcomes", "Supply response + fiscal model", "high"),
    ParameterSpec("F15", "item_rules_strength", "fiscal/governance", "Strength of item definitions, documentation, duration/frequency and clinical necessity rules.", "0-1 index", 0.42, 0.00, 0.95, "policy option prior", "ACC-style analogy", "Item schedule rules and audit results", "Claims audit/rule evaluation", "high"),

    # Governance, visibility, and equity
    ParameterSpec("G01", "safety_governance", "governance", "Credentialing, prescribing, scope and clinical governance for claimable activity.", "0-1 index", 0.66, 0.00, 0.95, "source-informed prior", "Scope and ACC-style provider rules are relevant", "Credentialing/audit/adverse events", "Safety governance evaluation", "high"),
    ParameterSpec("G02", "gaming_controls", "governance", "Audit, anomaly detection, coding rules and balancing measures.", "0-1 index", 0.54, 0.00, 0.95, "placeholder prior", "Needs claims/data architecture", "Claims patterns, outliers, re-presentations", "Outlier/fraud/waste model", "high"),
    ParameterSpec("G03", "audit_intensity", "governance", "Operational intensity and credibility of claims audit.", "0-1 index", 0.42, 0.00, 0.95, "placeholder prior", "Needs audit design", "Audit rates, recovery, quality flags", "Audit-effect model", "medium"),
    ParameterSpec("G04", "data_observability_primary", "data", "Visibility of appointment, encounter and outcome data.", "0-1 index", 0.44, 0.00, 0.95, "source-informed prior", "NPCD implementation pending", "NPCD completeness/timeliness", "Data completeness model", "high"),
    ParameterSpec("G05", "data_observability_ambulance", "data", "Visibility of ambulance demand, conveyance and alternative disposition data.", "0-1 index", 0.48, 0.00, 0.95, "source-informed prior", "Ambulance KPIs exist", "Ambulance event/disposition data", "Data linkage model", "high"),
    ParameterSpec("G06", "data_observability_hospital", "data", "Visibility and linkage of ED/admission outcomes to upstream access.", "0-1 index", 0.60, 0.00, 0.95, "source-informed prior", "Hospital data collections exist", "ED/NMDS/NHI linkage", "Linked outcomes model", "high"),
    ParameterSpec("G07", "primary_kpi_salience", "accountability", "Top-tier visibility of primary care access and outcomes.", "0-1 index", 0.42, 0.00, 0.95, "source-informed prior", "Primary care target implementation pending", "Target reporting, consequences, balancing measures", "KPI salience evaluation", "high"),
    ParameterSpec("G08", "ambulance_kpi_salience", "accountability", "Top-tier visibility of ambulance response, non-conveyance and offload outcomes.", "0-1 index", 0.45, 0.00, 0.95, "source-informed prior", "Ambulance KPIs reported but not top-tier equivalent", "KPIs and governance escalation", "KPI salience evaluation", "medium"),
    ParameterSpec("G09", "hospital_salience", "political economy", "Political/managerial salience of hospital failure relative to upstream failure.", "0-1 index", 0.88, 0.00, 0.95, "strategic hypothesis", "Hospitals highly visible", "Media/budget/escalation patterns", "Political-economy analysis", "medium"),
    ParameterSpec("G10", "equity_program_strength", "equity", "Strength of outreach, kaupapa Māori/Pacific/community programmes protecting equity.", "0-1 index", 0.46, 0.00, 0.95, "placeholder prior", "Needs equity review", "Programme funding, uptake, outcomes", "Equity impact evaluation", "high"),
    ParameterSpec("G11", "te_tiriti_governance_strength", "equity/governance", "Strength of Te Tiriti and Māori data/governance arrangements in design and monitoring.", "0-1 index", 0.42, 0.00, 0.95, "placeholder prior", "Needs Māori governance review", "Governance terms, data sovereignty processes", "Qualitative/governance assessment", "high"),
    ParameterSpec("G12", "consumer_trust", "legitimacy", "Trust that patients and communities have in the service model.", "0-1 index", 0.50, 0.00, 0.95, "placeholder prior", "Needs consumer validation", "Patient experience, trust, uptake", "Survey/interview model", "medium"),
    ParameterSpec("G13", "stakeholder_alignment", "political economy", "Alignment among providers, PHOs, officials, funders and communities.", "0-1 index", 0.36, 0.00, 0.95, "placeholder prior", "Needs MCDA/stakeholder scoring", "Workshop scores, submissions, interviews", "Deliberative MCDA/qualitative analysis", "medium"),
    ParameterSpec("G14", "narrative_coherence", "political economy", "Whether the reform can be explained without being misread as uncontrolled FFS or anti-equity.", "0-1 index", 0.46, 0.00, 0.95, "author judgement prior", "Publication strategy matters", "Stakeholder response, public feedback", "Qualitative/narrative evaluation", "medium"),

    # Hospital, ambulance, urgent care and cost
    ParameterSpec("H01", "baseline_hospital_pressure", "hospital", "Baseline relative hospital pressure in the absence of additional upstream deflection.", "0-1 index", 0.72, 0.00, 0.95, "source-informed prior", "Hospital pressure is central context", "ED/admission/bed/deficit data", "Baseline calibration", "high"),
    ParameterSpec("H02", "ed_conversion_rate", "hospital", "Rate at which unmet primary care need converts to ED presentation.", "0-1 index", 0.32, 0.01, 0.90, "placeholder prior", "Needs linked data", "Unmet care/waiting time to ED", "Hazard/transition model", "high"),
    ParameterSpec("H03", "admission_conversion_rate", "hospital", "Rate at which ED/ambulance/unmet need converts to hospital admission.", "0-1 index", 0.18, 0.01, 0.70, "placeholder prior", "Needs ED/NMDS linkage", "ED disposition, admissions, diagnosis", "Transition model", "high"),
    ParameterSpec("H04", "ambulance_conveyance_default", "ambulance", "Default tendency for ambulance pathways to convey to ED when alternatives are weak.", "0-1 index", 0.72, 0.05, 0.95, "placeholder prior", "Needs ambulance disposition data", "Conveyance, treat-and-refer, destination", "Multinomial disposition model", "high"),
    ParameterSpec("H05", "ambulance_deflection_rate", "ambulance", "Effectiveness of funded alternative disposition/hear-and-treat/treat-and-refer pathways.", "0-1 index", 0.22, 0.00, 0.90, "placeholder prior", "Needs pilots/ambulance data", "Non-conveyance safety, re-presentation", "Pathway evaluation", "high"),
    ParameterSpec("H06", "urgent_care_effectiveness", "urgent care", "Effectiveness of urgent and after-hours care in substituting for ED without unsafe delay.", "0-1 index", 0.42, 0.00, 0.95, "source-informed prior", "Urgent care policy is current comparator", "Urgent visits, ED substitution, fees, outcomes", "Synthetic control/DID/pilot evaluation", "high"),
    ParameterSpec("H07", "telehealth_substitution_rate", "digital", "Share of telehealth activity that substitutes for, rather than adds to, in-person/local supply.", "0-1 index", 0.42, 0.00, 0.95, "placeholder prior", "Needs mode/outcomes data", "Telehealth visits, follow-up, re-presentation", "Substitution/complementarity model", "medium"),
    ParameterSpec("H08", "hospital_cost_per_event_index", "cost", "Relative public cost of ED/admission events versus primary care contacts.", "0-1 index", 0.82, 0.05, 0.95, "placeholder prior", "Needs cost weights", "ED/inpatient cost weights", "Costing model", "high"),
    ParameterSpec("H09", "primary_contact_cost_index", "cost", "Relative public cost of claimable primary medical contact.", "0-1 index", 0.28, 0.05, 0.70, "placeholder prior", "Needs item schedule/costing", "Service cost and schedule price", "Activity costing", "high"),
    ParameterSpec("H10", "ambulance_event_cost_index", "cost", "Relative public cost of ambulance event and alternative disposition pathways.", "0-1 index", 0.46, 0.05, 0.85, "placeholder prior", "Needs ambulance costing", "Call/response/conveyance pathway cost", "Pathway costing", "medium"),

    # Risks and implementation
    ParameterSpec("R01", "cherry_picking_risk", "risk", "Risk that providers select easy/profitable contacts while hard-to-reach patients remain under-served.", "0-1 index", 0.58, 0.00, 0.95, "stakeholder-informed hypothesis", "Place-based accountability needed", "Patient mix, complexity, outreach, non-attenders", "Equity/selection model", "high"),
    ParameterSpec("R02", "low_value_activity_risk", "risk", "Risk of claimable low-value or unnecessary contacts under fee-for-service.", "0-1 index", 0.45, 0.00, 0.95, "theory prior", "FFS can incentivise volume", "Claims outliers, coding, outcomes", "Audit/utilisation model", "high"),
    ParameterSpec("R03", "fiscal_leakage_risk", "risk", "Risk that funding leaks to volume or margin without improving access/equity/outcomes.", "0-1 index", 0.42, 0.00, 0.95, "theory prior", "Demand-led models require controls", "Public spend, outcomes, claim patterns", "Value-for-money model", "high"),
    ParameterSpec("R04", "provider_moral_hazard_risk", "risk", "Risk that providers alter coding/contact patterns to maximise payment.", "0-1 index", 0.38, 0.00, 0.95, "theory prior", "Payment incentives create coding risk", "Billing patterns and audit outcomes", "Anomaly detection", "medium"),
    ParameterSpec("R05", "cream_skimming_penalty", "risk/equity", "Penalty for reform options that expand easy supply but leave complex demand unmet.", "0-1 index", 0.50, 0.00, 0.95, "policy hypothesis", "Place accountability guardrail", "Patient mix, enrolment/open books, complexity", "Selection/equity analysis", "high"),
    ParameterSpec("R06", "political_contestation", "implementation", "Likelihood that the reform is framed as ideological, anti-equity, anti-GP or anti-PHO.", "0-1 index", 0.58, 0.00, 0.95, "author judgement prior", "Email trail and sector politics", "Stakeholder responses, media framing", "Political-economy analysis", "medium"),
    ParameterSpec("R07", "implementation_complexity", "implementation", "Operational complexity of designing, paying, auditing and governing the architecture.", "0-1 index", 0.60, 0.00, 0.95, "policy judgement prior", "Multi-actor reform complexity", "Implementation plan, cost, timeline", "Implementation risk assessment", "medium"),
)

# Fast name lookup.
PARAMETER_BY_NAME: Dict[str, ParameterSpec] = {p.name: p for p in PARAMETER_SPECS}


DATA_INPUT_SPECS: tuple[DataInputSpec, ...] = (
    DataInputSpec("I01", "ncpd_appointments", "patient-practice-month", "NHI, practice_id, booked_date, seen_date, mode, urgency, provider_type, outcome", "Estimate access, wait time, demand, provider-scope activity and unmet need proxies", "National Primary Care Dataset", "Health NZ data access framework / research agreement", "High"),
    DataInputSpec("I02", "primary_encounters", "patient-practice-encounter", "NHI, date, reason/contact_type, provider_type, mode, diagnosis/proxy, outcome", "Estimate contact demand, provider type substitution, follow-up and safety", "NPCD / practice management systems", "Health NZ/research agreement/practice collaboration", "High"),
    DataInputSpec("I03", "capitation_payment_flows", "practice/PHO-month", "practice_id, PHO_id, capitation stream, rate, enrolments, top-ups, pass-through", "Estimate capitation adequacy, PHO pass-through and baseline viability", "MoH/HNZ/PHO Services Agreement/OIA/PHO collaboration", "OIA + data-sharing", "High"),
    DataInputSpec("I04", "fee_schedule_and_copayments", "practice/service", "contact_type, public subsidy, patient fee, fee caps, CSC/VLCA status", "Estimate price elasticity, equity burden and item price adequacy", "Practice fees, HNZ, sector surveys", "Survey/OIA/practice sample", "High"),
    DataInputSpec("I05", "acc_claims_and_payments", "claim-provider-month", "claim_id, provider_id/practice_id, service type, payment route, cost, date, outcome", "Estimate ACC stabilisation and cross-funder substitution", "ACC claims/provider payments", "ACC data request / ethics if identifiable", "High"),
    DataInputSpec("I06", "ambulance_events", "event", "NHI if available, time, acuity, response, disposition, conveyance, handover delay, funding source", "Estimate conveyance/default, deflection and ambulance-hospital interface", "Ambulance providers/HNZ/ACC", "Data-sharing/OIA/ethics", "High"),
    DataInputSpec("I07", "ed_and_hospital_linkage", "patient-event", "NHI, ED arrival, triage, diagnosis, disposition, admission, LOS, cost weight", "Estimate ED/admission conversion and hospital pressure", "NNPAC/NMDS/HNZ", "Health data access/ethics", "High"),
    DataInputSpec("I08", "workforce_and_scope", "provider-practice-month", "provider_id, profession, FTE, scope, prescribing authority, sessions, vacancy", "Estimate capacity, productivity, substitution and exit/entry", "Workforce data, practices, regulatory bodies", "Data-sharing/survey", "High"),
    DataInputSpec("I09", "practice_market_entry_exit", "practice-month", "practice_id, opening/closure, enrolment status, open books, new entrant, ownership", "Estimate market entry response, closed books and cherry-picking", "HNZ primary care data, sector survey", "Data-sharing/OIA/survey", "Medium"),
    DataInputSpec("I10", "equity_and_consumer_experience", "patient/group", "ethnicity, NZDep, rurality, age, sex, multimorbidity, unmet need, trust/experience", "Estimate equity modifiers, price response and trust legitimacy", "NZ Health Survey/NES/NPCD/patient survey", "Public data + linked data + survey", "High"),
    DataInputSpec("I11", "urgent_after_hours_activity", "service-month", "service type, in-person/digital, fees, wait, outcome, ED substitution, rurality", "Estimate urgent-care effectiveness and opportunity cost", "HNZ urgent care programme/providers", "OIA/data-sharing", "High"),
    DataInputSpec("I12", "policy_and_budget_flows", "appropriation/year", "Vote, appropriation, baseline, transfer, spend, initiative, service class", "Estimate budget tightness, hospital salience and fiscal exposure", "Treasury/MoH/HNZ budget documents", "Public/OIA", "Medium"),
)


SCENARIOS: tuple[ScenarioSpec, ...] = (
    ScenarioSpec("F0", "Current reform pathway", "Capitation reweighting, access target, digital/urgent care and PHO accountability, without uncapped primary medical FFS.", {
        "capitation_weighting_adequacy": 0.72, "primary_kpi_salience": 0.62, "data_observability_primary": 0.62,
        "urgent_care_effectiveness": 0.58, "scheduled_medical_benefit_strength": 0.12, "global_cap_constraint": 0.70,
        "item_rules_strength": 0.50, "narrative_coherence": 0.55,
    }),
    ScenarioSpec("F1", "Capitation reweighting only", "Formula improves allocation but marginal activity remains weakly funded.", {
        "capitation_weighting_adequacy": 0.78, "scheduled_medical_benefit_strength": 0.10, "activity_signal_strength": 0.22,
        "global_cap_constraint": 0.78, "data_observability_primary": 0.50,
    }),
    ScenarioSpec("F2", "Uncapped scheduled medical FFS", "Eligible primary medical activity becomes demand-led through scheduled benefits, but place accountability remains weak.", {
        "scheduled_medical_benefit_strength": 0.78, "scheduled_benefit_price_adequacy": 0.72, "activity_signal_strength": 0.78,
        "global_cap_constraint": 0.15, "direct_claiming_strength": 0.72, "place_based_accountability_strength": 0.38,
        "item_rules_strength": 0.70, "gaming_controls": 0.66, "audit_intensity": 0.62,
        "cherry_picking_risk": 0.64, "fiscal_leakage_risk": 0.50,
    }),
    ScenarioSpec("F3", "Uncapped medical FFS + place accountability", "Demand-led eligible medical activity plus capitation and explicit place/population responsibility.", {
        "scheduled_medical_benefit_strength": 0.76, "scheduled_benefit_price_adequacy": 0.72, "activity_signal_strength": 0.76,
        "global_cap_constraint": 0.15, "direct_claiming_strength": 0.70, "place_based_accountability_strength": 0.78,
        "capitation_weighting_adequacy": 0.78, "item_rules_strength": 0.76, "gaming_controls": 0.74,
        "audit_intensity": 0.70, "cherry_picking_risk": 0.35, "cream_skimming_penalty": 0.30,
        "copayment_protection_strength": 0.70, "equity_program_strength": 0.70,
    }),
    ScenarioSpec("F4", "Full hybrid upstream architecture", "Capitation + uncapped scheduled primary medical FFS + place accountability + urgent/ambulance alternatives + scope-enabled supply + strong data/audit/KPIs.", {
        "capitation_weighting_adequacy": 0.82, "scheduled_medical_benefit_strength": 0.78, "scheduled_benefit_price_adequacy": 0.74,
        "activity_signal_strength": 0.78, "global_cap_constraint": 0.10, "direct_claiming_strength": 0.76,
        "place_based_accountability_strength": 0.82, "scope_substitution_rate": 0.62, "gp_capacity_index": 0.58,
        "nurse_np_capacity_index": 0.66, "pharmacist_capacity_index": 0.58, "allied_health_capacity_index": 0.54,
        "paramedic_alt_capacity_index": 0.62, "rural_loading_response": 0.62, "local_inperson_constraint": 0.35,
        "urgent_care_effectiveness": 0.72, "ambulance_deflection_rate": 0.65, "ambulance_conveyance_default": 0.45,
        "data_observability_primary": 0.85, "data_observability_ambulance": 0.78, "data_observability_hospital": 0.82,
        "primary_kpi_salience": 0.82, "ambulance_kpi_salience": 0.76, "safety_governance": 0.86,
        "gaming_controls": 0.82, "audit_intensity": 0.78, "copayment_protection_strength": 0.76,
        "equity_program_strength": 0.78, "te_tiriti_governance_strength": 0.76, "stakeholder_alignment": 0.68,
        "narrative_coherence": 0.72, "cherry_picking_risk": 0.26, "low_value_activity_risk": 0.28,
        "fiscal_leakage_risk": 0.28, "implementation_complexity": 0.72,
    }),
    ScenarioSpec("F5", "Uncapped weak-control model", "Activity becomes demand-led but controls, place accountability and equity protections are weak.", {
        "scheduled_medical_benefit_strength": 0.82, "scheduled_benefit_price_adequacy": 0.78, "activity_signal_strength": 0.82,
        "global_cap_constraint": 0.08, "item_rules_strength": 0.25, "gaming_controls": 0.22, "audit_intensity": 0.18,
        "place_based_accountability_strength": 0.20, "copayment_protection_strength": 0.30, "equity_program_strength": 0.28,
        "cherry_picking_risk": 0.78, "low_value_activity_risk": 0.78, "fiscal_leakage_risk": 0.76,
        "provider_moral_hazard_risk": 0.70, "cream_skimming_penalty": 0.72,
    }),
    ScenarioSpec("F6", "ACC activity constraint shock", "ACC activity payments are constrained without compensating Health NZ-funded upstream supply.", {
        "acc_activity_strength": 0.25, "acc_constraint_intensity": 0.70, "activity_signal_strength": 0.12,
        "global_cap_constraint": 0.82, "budget_tightness": 0.86, "hospital_salience": 0.90,
    }),
    ScenarioSpec("F7", "Ambulance and urgent alternatives only", "Urgent/ambulance alternatives are strengthened but the primary medical marginal payment signal remains weak.", {
        "urgent_care_effectiveness": 0.74, "ambulance_deflection_rate": 0.72, "ambulance_kpi_salience": 0.72,
        "data_observability_ambulance": 0.76, "scheduled_medical_benefit_strength": 0.12, "global_cap_constraint": 0.74,
    }),
    ScenarioSpec("F8", "Scope-enabled supply only", "Broader providers can generate some activity, but payment architecture and place accountability are not fully reformed.", {
        "scope_substitution_rate": 0.68, "nurse_np_capacity_index": 0.68, "pharmacist_capacity_index": 0.62,
        "allied_health_capacity_index": 0.62, "safety_governance": 0.82, "scheduled_medical_benefit_strength": 0.22,
        "activity_signal_strength": 0.35, "global_cap_constraint": 0.68,
    }),
    ScenarioSpec("F9", "Place-based commissioning only", "Population accountability and outreach improve, but marginal activity funding is not materially uncapped.", {
        "place_based_accountability_strength": 0.78, "equity_program_strength": 0.74, "te_tiriti_governance_strength": 0.72,
        "cherry_picking_risk": 0.28, "cream_skimming_penalty": 0.28, "scheduled_medical_benefit_strength": 0.12,
        "global_cap_constraint": 0.74,
    }),
)


def parameter_register() -> pd.DataFrame:
    return pd.DataFrame([asdict(p) for p in PARAMETER_SPECS])


def data_input_contract() -> pd.DataFrame:
    return pd.DataFrame([asdict(i) for i in DATA_INPUT_SPECS])


def scenario_matrix() -> pd.DataFrame:
    base = {p.name: p.current_value for p in PARAMETER_SPECS}
    rows = []
    for s in SCENARIOS:
        row = {"scenario_id": s.scenario_id, "scenario_name": s.name, "description": s.description}
        values = base.copy()
        values.update(s.overrides)
        row.update(values)
        rows.append(row)
    return pd.DataFrame(rows)


def scenario_parameters(scenario_id: str) -> Dict[str, float]:
    base = {p.name: p.current_value for p in PARAMETER_SPECS}
    spec = next((s for s in SCENARIOS if s.scenario_id == scenario_id), None)
    if spec is None:
        raise KeyError(f"Unknown scenario_id: {scenario_id}")
    base.update(spec.overrides)
    return base


def compute_architecture_indices(params: Mapping[str, float]) -> Dict[str, float]:
    # Demand burden and equity burden
    demand_burden = clamp(0.35 + 0.18*params["chronic_need_index"] + 0.18*params["rurality_demand_modifier"] + 0.18*params["deprivation_demand_modifier"] + 0.16*params["multimorbidity_demand_modifier"])
    copay_burden = clamp(params["patient_copayment_level"] * (1 - 0.70*params["copayment_protection_strength"]) * (0.85 + 0.45*params["price_elasticity_high_need"]))
    scope_capacity = clamp(0.25*params["gp_capacity_index"] + 0.22*params["nurse_np_capacity_index"] + 0.16*params["pharmacist_capacity_index"] + 0.14*params["allied_health_capacity_index"] + 0.13*params["paramedic_alt_capacity_index"] + 0.10*params["scope_substitution_rate"])
    marginal_payment = clamp(0.35*params["scheduled_medical_benefit_strength"] + 0.25*params["scheduled_benefit_price_adequacy"] + 0.25*params["activity_signal_strength"] + 0.15*params["acc_activity_strength"] - 0.25*params["global_cap_constraint"])
    administration = clamp(0.40*params["direct_claiming_strength"] + 0.25*params["item_rules_strength"] + 0.20*params["data_observability_primary"] + 0.15*(1 - params["pho_transaction_cost"]))
    place = clamp(0.45*params["place_based_accountability_strength"] + 0.25*params["equity_program_strength"] + 0.15*params["te_tiriti_governance_strength"] + 0.15*params["copayment_protection_strength"])
    governance = clamp(0.28*params["safety_governance"] + 0.24*params["gaming_controls"] + 0.20*params["audit_intensity"] + 0.14*params["data_observability_primary"] + 0.14*params["item_rules_strength"])
    urgent_ambulance = clamp(0.35*params["urgent_care_effectiveness"] + 0.30*params["ambulance_deflection_rate"] + 0.15*(1 - params["ambulance_conveyance_default"]) + 0.10*params["ambulance_kpi_salience"] + 0.10*params["data_observability_ambulance"])
    kpi_data = clamp(0.28*params["primary_kpi_salience"] + 0.22*params["ambulance_kpi_salience"] + 0.24*params["data_observability_primary"] + 0.14*params["data_observability_hospital"] + 0.12*params["data_observability_ambulance"])
    supply_generation = clamp(0.32*marginal_payment + 0.24*scope_capacity + 0.14*administration + 0.12*params["rural_loading_response"] + 0.10*params["market_entry_response"] + 0.08*params["capitation_base_strength"] - 0.14*params["local_inperson_constraint"] - 0.08*params["workforce_exit_rate"])
    access = clamp(0.20 + 0.55*supply_generation + 0.15*urgent_ambulance + 0.12*params["telehealth_acceptability"] - 0.22*copay_burden - 0.10*demand_burden)
    equity_legitimacy = clamp(0.34*place + 0.22*params["copayment_protection_strength"] + 0.18*params["consumer_trust"] + 0.16*params["equity_program_strength"] + 0.10*params["te_tiriti_governance_strength"] - 0.18*params["cherry_picking_risk"] - 0.12*copay_burden)
    hospital_deflection = clamp(0.34*access + 0.25*urgent_ambulance + 0.16*kpi_data + 0.12*place + 0.13*scope_capacity - 0.22*demand_burden)
    gaming_risk = clamp(0.22*params["low_value_activity_risk"] + 0.20*params["provider_moral_hazard_risk"] + 0.18*params["fiscal_leakage_risk"] + 0.18*params["cherry_picking_risk"] + 0.12*(1-governance) + 0.10*params["scheduled_medical_benefit_strength"] - 0.16*params["item_rules_strength"])
    fiscal_risk = clamp(0.24*params["fiscal_leakage_risk"] + 0.18*params["scheduled_medical_benefit_strength"] + 0.14*(1 - params["global_cap_constraint"]) + 0.16*gaming_risk + 0.12*params["implementation_complexity"] + 0.10*params["hospital_cost_per_event_index"] - 0.18*hospital_deflection - 0.10*governance)
    hospital_pressure = clamp(0.16 + 0.45*params["baseline_hospital_pressure"] + 0.26*(1 - hospital_deflection) + 0.14*demand_burden + 0.10*params["hospital_salience"] - 0.20*access - 0.12*urgent_ambulance)
    implementation_feasibility = clamp(0.40*params["stakeholder_alignment"] + 0.25*params["narrative_coherence"] + 0.20*params["data_observability_primary"] + 0.15*params["safety_governance"] - 0.22*params["implementation_complexity"] - 0.18*params["political_contestation"])
    viability = clamp(0.18 + 0.16*supply_generation + 0.16*access + 0.14*equity_legitimacy + 0.12*governance + 0.16*hospital_deflection + 0.10*implementation_feasibility + 0.08*(1 - fiscal_risk) + 0.08*(1 - gaming_risk))
    return {
        "demand_burden": demand_burden,
        "copayment_burden": copay_burden,
        "scope_capacity": scope_capacity,
        "marginal_payment_signal": marginal_payment,
        "administrative_readiness": administration,
        "place_accountability": place,
        "governance_resilience": governance,
        "urgent_ambulance_deflection": urgent_ambulance,
        "kpi_data_salience": kpi_data,
        "supply_generation": supply_generation,
        "access_index": access,
        "equity_legitimacy": equity_legitimacy,
        "hospital_deflection": hospital_deflection,
        "gaming_risk": gaming_risk,
        "fiscal_risk": fiscal_risk,
        "hospital_pressure": hospital_pressure,
        "implementation_feasibility": implementation_feasibility,
        "hybrid_viability": viability,
    }


def run_monthly_simulation(params: Mapping[str, float], months: int = 60) -> pd.DataFrame:
    idx = compute_architecture_indices(params)
    rows = []
    unmet = 55.0 + 30.0*idx["demand_burden"] - 25.0*idx["access_index"]
    capacity_stock = 50.0 + 38.0*idx["supply_generation"]
    for month in range(1, months + 1):
        seasonal = 1.0 + 0.045 * math.sin(2 * math.pi * month / 12)
        # Capacity increases gradually under stronger supply settings and declines under exit/tightness.
        capacity_stock = max(5.0, capacity_stock + 1.1*idx["supply_generation"] - 0.65*params["workforce_exit_rate"] - 0.38*params["budget_tightness"] + 0.42*params["market_entry_response"])
        effective_access = clamp(idx["access_index"] + 0.003*(capacity_stock-50) - 0.08*idx["copayment_burden"])
        monthly_need = params["base_need_per_1000"] * seasonal * (0.80 + 0.44*idx["demand_burden"])
        primary_contacts = max(0.0, monthly_need * effective_access * (0.90 + 0.16*idx["supply_generation"]))
        # Unmet need persists and grows under access/cost constraints; place/governance reduces persistence.
        unmet = max(0.0, params["unmet_need_persistence"] * unmet + monthly_need * (1-effective_access) * 0.46 + 18*idx["copayment_burden"] + 9*params["global_cap_constraint"] - 16*idx["place_accountability"] - 10*idx["urgent_ambulance_deflection"])
        ed_events = 58 * seasonal + 0.78 * unmet * params["ed_conversion_rate"] * (1.18 - 0.45*idx["urgent_ambulance_deflection"])
        admissions = 13 * seasonal + ed_events * params["admission_conversion_rate"] * (0.75 + 0.60*params["delay_complexity_growth"])
        ambulance = 21 * seasonal + 0.55 * unmet * params["ambulance_conveyance_default"] * (1.05 - 0.55*params["ambulance_deflection_rate"])
        hospital_pressure = clamp(0.18 + 0.0038*ed_events + 0.010*admissions + 0.0038*ambulance + 0.20*params["hospital_salience"] - 0.20*idx["hospital_deflection"])
        primary_public_cost = primary_contacts * (55 + 105*params["scheduled_benefit_price_adequacy"] + 36*params["capitation_base_strength"])
        ed_hosp_cost = ed_events * (430 + 990*params["hospital_cost_per_event_index"]) + admissions * (2900 + 4800*params["hospital_cost_per_event_index"])
        ambulance_cost = ambulance * (420 + 720*params["ambulance_event_cost_index"])
        leakage_cost = 1000 * (idx["gaming_risk"] + idx["fiscal_risk"]) * max(0.0, params["scheduled_medical_benefit_strength"] - params["gaming_controls"])
        public_cost_index = (primary_public_cost + ed_hosp_cost + ambulance_cost + leakage_cost) / 100000.0
        rows.append({
            "month": month,
            "primary_contacts_per_1000": primary_contacts,
            "effective_access_index": effective_access,
            "unmet_need_index": unmet,
            "ed_events_per_100k": ed_events,
            "admissions_per_100k": admissions,
            "ambulance_conveyances_per_100k": ambulance,
            "hospital_pressure_index": hospital_pressure,
            "public_cost_index": public_cost_index,
            "capacity_stock_index": capacity_stock,
            **{k: v for k, v in idx.items() if k not in {"access_index"}},
            "access_index": idx["access_index"],
        })
    return pd.DataFrame(rows)


def run_all_scenarios(months: int = 60) -> tuple[pd.DataFrame, pd.DataFrame]:
    monthly_frames = []
    summary_rows = []
    for spec in SCENARIOS:
        params = scenario_parameters(spec.scenario_id)
        monthly = run_monthly_simulation(params, months)
        monthly.insert(0, "scenario_id", spec.scenario_id)
        monthly.insert(1, "scenario_name", spec.name)
        monthly_frames.append(monthly)
        idx = compute_architecture_indices(params)
        final = monthly.iloc[-12:].mean(numeric_only=True)
        summary_rows.append({
            "scenario_id": spec.scenario_id,
            "scenario_name": spec.name,
            "description": spec.description,
            "hybrid_viability_score": round(100*idx["hybrid_viability"], 2),
            "access_score": round(100*idx["access_index"], 2),
            "supply_generation_score": round(100*idx["supply_generation"], 2),
            "equity_legitimacy_score": round(100*idx["equity_legitimacy"], 2),
            "governance_resilience_score": round(100*idx["governance_resilience"], 2),
            "hospital_deflection_score": round(100*idx["hospital_deflection"], 2),
            "fiscal_risk_score": round(100*idx["fiscal_risk"], 2),
            "gaming_risk_score": round(100*idx["gaming_risk"], 2),
            "hospital_pressure_score": round(100*idx["hospital_pressure"], 2),
            "mean_last12_primary_contacts_per_1000": round(float(final["primary_contacts_per_1000"]), 2),
            "mean_last12_unmet_need_index": round(float(final["unmet_need_index"]), 2),
            "mean_last12_ed_events_per_100k": round(float(final["ed_events_per_100k"]), 2),
            "mean_last12_admissions_per_100k": round(float(final["admissions_per_100k"]), 2),
            "mean_last12_ambulance_conveyances_per_100k": round(float(final["ambulance_conveyances_per_100k"]), 2),
            "mean_last12_hospital_pressure_index": round(float(final["hospital_pressure_index"]), 3),
            "mean_last12_public_cost_index": round(float(final["public_cost_index"]), 2),
        })
    summary = pd.DataFrame(summary_rows)
    summary["rank_by_hybrid_viability"] = summary["hybrid_viability_score"].rank(ascending=False, method="min").astype(int)
    return pd.concat(monthly_frames, ignore_index=True), summary.sort_values("rank_by_hybrid_viability")


def sensitivity_analysis(base_scenario_id: str = "F4", delta: float = 0.08) -> pd.DataFrame:
    base_params = scenario_parameters(base_scenario_id)
    base_idx = compute_architecture_indices(base_params)
    rows = []
    for spec in PARAMETER_SPECS:
        p = spec.name
        for direction, label in [(-1, "down"), (1, "up")]:
            params = base_params.copy()
            params[p] = max(spec.lower_bound, min(spec.upper_bound, params[p] + direction*delta))
            idx = compute_architecture_indices(params)
            rows.append({
                "base_scenario_id": base_scenario_id,
                "parameter": p,
                "domain": spec.domain,
                "direction": label,
                "baseline_value": base_params[p],
                "perturbed_value": params[p],
                "hybrid_viability_change": 100*(idx["hybrid_viability"] - base_idx["hybrid_viability"]),
                "hospital_pressure_change": 100*(idx["hospital_pressure"] - base_idx["hospital_pressure"]),
                "access_change": 100*(idx["access_index"] - base_idx["access_index"]),
                "fiscal_risk_change": 100*(idx["fiscal_risk"] - base_idx["fiscal_risk"]),
            })
    out = pd.DataFrame(rows)
    # Absolute largest direction per parameter for compact tornado plots.
    out["abs_viability_change"] = out["hybrid_viability_change"].abs()
    return out.sort_values("abs_viability_change", ascending=False)


def calibration_target_matrix() -> pd.DataFrame:
    rows = []
    mapping = {
        "marginal supply response": ["F03", "F04", "F05", "S10", "S12"],
        "price/demand response": ["D08", "D09", "F06", "F07"],
        "unmet need to ED/hospital": ["D11", "D12", "H02", "H03"],
        "ambulance alternatives": ["S05", "H04", "H05", "G05", "G08"],
        "ACC stabilisation": ["F08", "F09"],
        "PHO/direct claiming": ["F10", "F11"],
        "scope-enabled supply": ["S02", "S03", "S04", "S08", "G01"],
        "place/equity/cherry-picking": ["F12", "G10", "G11", "R01", "R05"],
        "audit/gaming/fiscal leakage": ["F15", "G02", "G03", "R02", "R03", "R04"],
    }
    by_id = {p.parameter_id: p for p in PARAMETER_SPECS}
    for target, ids in mapping.items():
        for pid in ids:
            p = by_id[pid]
            rows.append({
                "calibration_target": target,
                "parameter_id": p.parameter_id,
                "parameter": p.name,
                "domain": p.domain,
                "priority": p.priority,
                "real_data_needed": p.real_data_needed,
                "estimation_strategy": p.estimation_strategy,
            })
    return pd.DataFrame(rows)


if __name__ == "__main__":
    monthly, summary = run_all_scenarios()
    print(summary[["scenario_id", "scenario_name", "hybrid_viability_score", "hospital_pressure_score", "rank_by_hybrid_viability"]].to_string(index=False))
