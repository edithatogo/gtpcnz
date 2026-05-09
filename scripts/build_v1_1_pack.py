from pathlib import Path
import csv, json, textwrap, os, subprocess
from datetime import date

ROOT = Path('/mnt/data/work/project/primary-care-funding-architecture')
VER = 'v1.1.0'
TODAY = '2026-05-08'

# Utility

def write(path, content):
    path = ROOT / path
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(textwrap.dedent(content).strip()+"\n", encoding='utf-8')


def write_csv(path, rows):
    path = ROOT / path
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        path.write_text('', encoding='utf-8')
        return
    with path.open('w', newline='', encoding='utf-8') as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader(); w.writerows(rows)

# Sources registry
sources = [
    {
        'source_id':'SRC01','name':'Ministry of Health capitation reweighting','url':'https://www.health.govt.nz/strategies-initiatives/programmes-and-initiatives/primary-and-community-health-care/capitation-reweighting','use':'Broad capitation context; 1 July 2026 reweighting; variables include age, sex, multimorbidity, rurality and deprivation.'
    },
    {
        'source_id':'SRC02','name':'Cabinet paper: Primary Health Care Funding Improvements','url':'https://www.health.govt.nz/system/files/2025-07/Cabinet%20paper%20-%20Primary%20Health%20Care%20Funding%20Improvements%20Redacted.pdf','use':'Reweighting implemented within available primary care funding; variable additions and constraints.'
    },
    {
        'source_id':'SRC03','name':'Health NZ National Primary Care Dataset and health target','url':'https://www.healthnz.govt.nz/about-us/what-we-do/planning-and-performance/primary-care-tactical-action-plan/national-primary-care-dataset-and-new-primary-care-health-target','use':'Primary care encounter and appointment dataset, 80% within-seven-days access target.'
    },
    {
        'source_id':'SRC04','name':'Ministry of Health PHO finances briefing H2025069314','url':'https://www.health.govt.nz/system/files/2025-11/H2025069314-Briefing-PHO-finances-a-summary-of-available-information.pdf','use':'PHO transparency, monitoring limitations, ownership/financial information issues.'
    },
    {
        'source_id':'SRC05','name':'NZ Health Survey 2024/25 annual update','url':'https://www.health.govt.nz/publications/annual-update-of-key-results-202425-new-zealand-health-survey','use':'Unmet need and GP cost barrier context.'
    },
    {
        'source_id':'SRC06','name':'Closed books study - PubMed abstract','url':'https://pubmed.ncbi.nlm.nih.gov/38452229/','use':'Evidence of closed/limited enrolment in Aotearoa New Zealand general practice.'
    },
    {
        'source_id':'SRC07','name':'ACC provider payment page','url':'https://www.acc.co.nz/for-providers/invoicing-us/paying-patient-treatment','use':'ACC contribution to treatment under contracts, regulations and agreements; provider-type payments.'
    },
    {
        'source_id':'SRC08','name':'Health NZ Ambulance Team','url':'https://www.healthnz.govt.nz/about-us/what-we-do/programmes-and-initiatives/the-ambulance-team','use':'Ambulance commissioning on behalf of Health NZ and ACC; performance data/KPI context.'
    },
    {
        'source_id':'SRC09','name':'Health NZ emergency ambulance national performance reports','url':'https://www.healthnz.govt.nz/publications/emergency-ambulance-service-national-performance-reports-2025','use':'Response times, call types, demand, contracted performance reporting.'
    },
    {
        'source_id':'SRC10','name':'Ministry of Health OIA requests page','url':'https://www.health.govt.nz/about-us/contact-us/oia-requests','use':'OIA process and request requirements.'
    },
    {
        'source_id':'SRC11','name':'PRISMA-ScR','url':'https://www.prisma-statement.org/scoping','use':'Scoping review reporting standard.'
    },
    {
        'source_id':'SRC12','name':'ISPOR MCDA introduction','url':'https://www.ispor.org/heor-resources/good-practices/article/multiple-criteria-decision-analysis-for-health-care-decision-making---an-introduction','use':'MCDA decision-support framing and healthcare use cases.'
    },
    {
        'source_id':'SRC13','name':'STRESS guidelines','url':'https://www.equator-network.org/reporting-guidelines/strengthening-the-reporting-of-empirical-simulation-studies-introducing-the-stress-guidelines/','use':'Simulation reporting framework if modelling is later empirically calibrated.'
    },
]
write_csv(f'docs/validation/source-registry-{VER}.csv', sources)
write_csv(f'outputs/source-registry-{VER}.csv', sources)

# Evidence threshold matrix
evidence_thresholds = [
    {'output':'Substack series','minimum_evidence_needed':'Public evidence + transparent theory + caveats','current_status':'Ready','do_not_claim':'Quantified forecast, fiscal savings, proven causation'},
    {'output':'RACMA discussion paper','minimum_evidence_needed':'Game map + audit trail + source-informed demonstrative model + validation plan','current_status':'Ready','do_not_claim':'Policy is proven or implementation-ready'},
    {'output':'Policy brief for sector/political audience','minimum_evidence_needed':'Public evidence + options analysis + model caveats + stakeholder validation plan','current_status':'Ready with caveats','do_not_claim':'Guaranteed hospital demand reduction'},
    {'output':'NZMJ Viewpoint','minimum_evidence_needed':'Conceptual/theoretical argument + policy context + transparent limitations','current_status':'Ready','do_not_claim':'Empirical predictive results'},
    {'output':'NZMJ methods/protocol article','minimum_evidence_needed':'Model structure + audit + standards crosswalk + validation pathway','current_status':'Ready','do_not_claim':'Empirically calibrated impact estimates'},
    {'output':'Government business case','minimum_evidence_needed':'Stakeholder validation + targeted empirical checks + fiscal modelling/pilot results','current_status':'Not ready','do_not_claim':'Budget-neutrality or savings'},
    {'output':'Implementation advice','minimum_evidence_needed':'Pilot/evaluation evidence + operational design + data governance + equity review','current_status':'Not ready','do_not_claim':'System can implement without unintended effects'},
]
write_csv(f'docs/validation/evidence-threshold-matrix-{VER}.csv', evidence_thresholds)
write_csv(f'outputs/evidence-threshold-matrix-{VER}.csv', evidence_thresholds)

priority_checks = [
    {'priority_rank':1,'parameter':'Marginal supply response to contact-based payment','game_ids':'G3,G8,G10','why_it_matters':'Determines whether a Primary Care Benefits Schedule expands safe upstream activity rather than simply redistributing existing demand.','proposed_method':'Practice-level panel analysis; before-after comparison where payment/activity settings vary; stakeholder validation of capacity response.','minimum_data':'Provider type, practice ID, appointment capacity, encounter counts, payments, co-payments, open/closed books.','initial_feasibility_1_5':3,'policy_criticality_1_5':5,'evidence_gap_1_5':5,'decision_use':'Whether to proceed with benefits schedule design and which contact types to include first.'},
    {'priority_rank':2,'parameter':'Unmet primary care to ED/ambulance/hospital conversion','game_ids':'G1,G2,G4,G7,G14','why_it_matters':'Tests the core wood-from-trees hypothesis that constrained upstream access channels demand into higher-cost hospital pathways.','proposed_method':'Linked longitudinal cohort; time-to-event or hazard models linking access delay/unmet need to ED, ambulance, admissions and re-presentations.','minimum_data':'NPCD booking/encounter data, NHI linkage, ED/NNPAC, NMDS, ambulance event data, demographics, rurality, deprivation.','initial_feasibility_1_5':2,'policy_criticality_1_5':5,'evidence_gap_1_5':5,'decision_use':'Whether upstream funding expansion plausibly deflects hospital demand.'},
    {'priority_rank':3,'parameter':'ACC activity funding stabilisation effect','game_ids':'G6,G3,G7','why_it_matters':'Tests whether ACC fee-for-service and treatment payments are mitigating wider primary care supply failure.','proposed_method':'Practice-level revenue-mix analysis; compare practices/regions with different ACC revenue shares; sensitivity to ACC payment changes.','minimum_data':'ACC primary care claims/payment volumes by provider/practice/region, non-ACC encounters, practice viability markers.','initial_feasibility_1_5':3,'policy_criticality_1_5':4,'evidence_gap_1_5':4,'decision_use':'Whether ACC treatment-payment policy should be assessed whole-of-system, not in isolation.'},
    {'priority_rank':4,'parameter':'PHO intermediation transaction-cost / entry-barrier effect','game_ids':'G5,G13,G14','why_it_matters':'Determines whether PHO reform should focus on function redesign, direct claims, transparency, or abolition/optionalisation.','proposed_method':'Mixed-methods analysis: PHO financial-flow audit, onboarding timelines, provider interviews, comparison of PHO pass-through and support functions.','minimum_data':'PHO financial statements, pass-through rules, service agreements, provider onboarding time, practice/provider interviews.','initial_feasibility_1_5':3,'policy_criticality_1_5':4,'evidence_gap_1_5':5,'decision_use':'Whether to separate PHO value-adding functions from payment-gateway functions.'},
    {'priority_rank':5,'parameter':'Scope-enabled provider supply and safety','game_ids':'G8,G10,G11,G12','why_it_matters':'Tests whether pharmacists, NPs, nurses, allied health and paramedics can safely generate additional contact activity under scope-based benefits.','proposed_method':'Pilot evaluation by contact type and provider type; safety audit; re-presentation and escalation analysis; patient experience.','minimum_data':'Provider scope, contact type, prescribing/clinical governance rules, re-presentations, adverse events, patient outcomes.','initial_feasibility_1_5':4,'policy_criticality_1_5':5,'evidence_gap_1_5':4,'decision_use':'Which contact types can be provider-neutral, which require GP/NP governance, and where patient choice is safe.'},
]
write_csv(f'docs/validation/priority-empirical-checks-{VER}.csv', priority_checks)
write_csv(f'outputs/priority-empirical-checks-{VER}.csv', priority_checks)

validation_workplan = [
    {'phase':1,'timeframe':'Weeks 1-2','workstream':'Policy synthesis','activities':'Finalize narrative, limitations, stakeholder-ready artefacts, evidence threshold matrix.','outputs':'Validation and translation report; one-page brief; Substack synthesis.'},
    {'phase':2,'timeframe':'Weeks 2-4','workstream':'Stakeholder MCDA preparation','activities':'Recruit groups; circulate game map; prepare workshop pack; test scoring instrument.','outputs':'Workshop pack; scoring workbook; participant briefing.'},
    {'phase':3,'timeframe':'Weeks 3-6','workstream':'OIA/data requests','activities':'Submit OIA requests for capitation formula, PHO advice, NPCD data elements, ambulance and ACC data.','outputs':'OIA tracker; source update log; request copies.'},
    {'phase':4,'timeframe':'Weeks 4-8','workstream':'Rapid scoping review','activities':'Register protocol internally; run searches; screen studies; extract mechanisms; evidence map.','outputs':'PRISMA-ScR evidence map; review memo; source matrix.'},
    {'phase':5,'timeframe':'Weeks 6-10','workstream':'Stakeholder validation','activities':'Run workshops/interviews; analyse agreement/disagreement; update game map and MCDA weights.','outputs':'Stakeholder validation report; revised MCDA.'},
    {'phase':6,'timeframe':'Weeks 8-12','workstream':'Targeted empirical checks','activities':'Assess feasibility of five priority parameters; negotiate data access; prepare pilot protocols.','outputs':'Data readiness report; empirical check protocols.'},
    {'phase':7,'timeframe':'Months 3-6','workstream':'Prospective pilot design','activities':'Choose pilot contact types and sites; define KPIs; governance; evaluation protocol.','outputs':'Pilot evaluation plan and implementation-ready measurement framework.'},
]
write_csv(f'docs/validation/validation-workplan-{VER}.csv', validation_workplan)
write_csv(f'outputs/validation-workplan-{VER}.csv', validation_workplan)

# Stakeholder validation survey template rows
stakeholder_games = [
    ('G1','Hospital-salience budget game','Hospital demand is visible, urgent and politically costly; upstream access failure is dispersed and delayed.'),
    ('G2','Health NZ internal allocation game','A single entity commissions hospital, primary and community services, but hospital operational risk is more immediate.'),
    ('G3','Capitation marginal-supply game','Capitation supports continuity but weakly funds additional clinically necessary contacts.'),
    ('G4','Consumer access pathway game','Patients choose among waiting, paying, delaying, telehealth, ambulance and ED.'),
    ('G5','PHO intermediation game','PHOs may add population-health value but payment-gateway functions may add friction or opacity.'),
    ('G6','ACC/Health NZ cross-funder game','ACC activity funding may stabilise primary care capacity and shift pressure across funders.'),
    ('G7','Ambulance conveyance game','Ambulance may default to ED conveyance unless safe alternatives are funded and accountable.'),
    ('G8','Scope-of-practice supply game','Funding eligibility may be narrower than safe clinical scope, creating artificial professional bottlenecks.'),
    ('G9','Telehealth/local-supply game','Telehealth extends access but may weaken local in-person supply if not integrated.'),
    ('G10','Co-payment calibration game','Co-payments can signal demand but can deter necessary care and worsen equity.'),
    ('G11','KPI salience game','What is elevated to top-tier reporting gets managed; upstream failures may otherwise remain residual.'),
    ('G12','Equity and trust game','Direct benefits can expand access but do not replace trust, outreach, kaupapa Maori/Pacific functions.'),
    ('G13','Political economy game','Reform can be framed as pro-market, anti-PHO, anti-GP, pro-patient or anti-equity.'),
    ('G14','Data observability game','Hidden unmet need remains less fundable if it is not measured and linked to downstream outcomes.'),
]
survey_rows=[]
for gid, name, desc in stakeholder_games:
    survey_rows.append({'game_id':gid,'game_name':name,'mechanism_to_validate':desc,'is_this_game_real_1_5':'','harm_if_unresolved_1_5':'','hospital_growth_contribution_1_5':'','equity_relevance_1_5':'','tractability_1_5':'','reform_risk_1_5':'','confidence_1_5':'','free_text_evidence_or_objections':''})
write_csv(f'data/templates/stakeholder-game-validation-survey-{VER}.csv', survey_rows)
write_csv(f'outputs/stakeholder-game-validation-survey-{VER}.csv', survey_rows)

# MCDA scoring template
criteria = [
    ('C1','Access and supply generation','Does the option increase safe upstream capacity?'),
    ('C2','Hospital deflection','Does it reduce avoidable ED, ambulance and hospital flow?'),
    ('C3','Equity and Te Tiriti legitimacy','Does access improve without worsening inequity?'),
    ('C4','Rural and in-person resilience','Does it protect local care, not just telehealth?'),
    ('C5','Fiscal sustainability','Is the model affordable and controllable?'),
    ('C6','Gaming and low-value activity risk','Does it avoid opportunistic or low-value activity?'),
    ('C7','Administrative simplicity and market entry','Does it lower transaction costs and entry barriers?'),
    ('C8','Governance and clinical safety','Are scope, prescribing, audit and safety controls strong?'),
    ('C9','Political feasibility','Can the option survive contestation?'),
    ('C10','Data and accountability readiness','Can outcomes be measured and managed?'),
]
options = [
    ('O1','Status quo tight control'),('O2','Capitation reweighting + access target'),('O3','National Primary Care Benefits Schedule'),('O4','Benefits schedule + scope-enabled eligibility'),('O5','Full upstream access architecture'),('O6','Loose benefits with weak controls'),('O7','ACC/ambulance alternatives only'),('O8','PHO reform/direct claims only')
]
mcda_rows=[]
for oid,oname in options:
    for cid,cname,cdesc in criteria:
        mcda_rows.append({'option_id':oid,'option_name':oname,'criterion_id':cid,'criterion_name':cname,'criterion_description':cdesc,'score_minus2_to_plus2':'','weight_0_to_100':'','confidence_0_to_1':'','risk_penalty_0_to_2':'','notes':''})
write_csv(f'data/templates/mcda-workshop-scoring-template-{VER}.csv', mcda_rows)
write_csv(f'outputs/mcda-workshop-scoring-template-{VER}.csv', mcda_rows)

# OIA/data tracker
requests = [
    {'request_id':'OIA01','agency':'Ministry of Health','request_title':'Current capitation formula, rate tables and implementation model','purpose':'Make the funding architecture reproducible and auditable.','core_items':'Full operational capitation formula; active rate tables; calculation workbook/code; FLS/VLCA/CSC/Care Plus/SIA components; PHOSA schedules; proposed 2026 reweighting implementation model.','status':'Draft','source_link':'https://www.health.govt.nz/about-us/contact-us/oia-requests'},
    {'request_id':'OIA02','agency':'Ministry of Health','request_title':'PHO roles, functions and options for change advice H2025067082','purpose':'Understand unreleased advice on PHO remit/function and options for change.','core_items':'Briefing H2025067082; attachments; related advice; any Cabinet/Ministerial decisions; reasons for withholding if not released.','status':'Draft','source_link':'https://www.health.govt.nz/system/files/2025-11/H2025069314-Briefing-PHO-finances-a-summary-of-available-information.pdf'},
    {'request_id':'OIA03','agency':'Health New Zealand','request_title':'Primary care payment flows, PHO pass-through and provider onboarding','purpose':'Test PHO intermediation and transaction-cost hypotheses.','core_items':'PHO payments and retained funds; pass-through rules; provider onboarding rules; performance payments; locality arrangements; contract templates.','status':'Draft','source_link':'https://www.healthnz.govt.nz/about-us/health-data/data-sets-and-collections/primary-care-data-and-statistics/primary-care-health-data'},
    {'request_id':'OIA04','agency':'Health New Zealand','request_title':'National Primary Care Dataset metadata and aggregate access data','purpose':'Prepare stakeholder validation and future empirical checks using NPCD fields.','core_items':'Data dictionary; appointment/encounter fields; governance; aggregate appointment waiting-time data; access target reporting methodology; privacy/data access process.','status':'Draft','source_link':'https://www.healthnz.govt.nz/about-us/what-we-do/planning-and-performance/primary-care-tactical-action-plan/national-primary-care-dataset-and-new-primary-care-health-target'},
    {'request_id':'OIA05','agency':'Health New Zealand / Ambulance Team','request_title':'Ambulance conveyance, alternative disposition and handover indicators','purpose':'Test ambulance as upstream access infrastructure and hospital-deflection lever.','core_items':'Conveyance/non-conveyance; hear-and-treat/treat-and-refer; ED handover delay; response times; call types; region/rurality; Health NZ/ACC split where available.','status':'Draft','source_link':'https://www.healthnz.govt.nz/about-us/what-we-do/programmes-and-initiatives/the-ambulance-team'},
    {'request_id':'OIA06','agency':'ACC','request_title':'ACC primary care treatment payments by provider type and region','purpose':'Test whether ACC activity payments stabilise primary care supply.','core_items':'Treatment payments by provider type/code/region; GP/nurse/NP/paramedic/physio/pharmacist where applicable; claim volumes; changes over time; aggregated de-identified data.','status':'Draft','source_link':'https://www.acc.co.nz/for-providers/invoicing-us/paying-patient-treatment'},
]
write_csv(f'docs/oia/oia-data-request-tracker-{VER}.csv', requests)
write_csv(f'outputs/oia-data-request-tracker-{VER}.csv', requests)

# Rapid review templates
review_screening = [
    {'record_id':'','title':'','authors':'','year':'','country':'','source_type':'journal / grey / policy / report','include_title_abstract_yes_no_unclear':'','reason_for_exclusion':'','full_text_needed_yes_no':'','mechanism_tags':'capitation; fee-for-service; blended; PHO; ambulance; ACC; scope; co-payment; hospital demand','notes':''}
]
write_csv(f'data/templates/rapid-review-screening-template-{VER}.csv', review_screening)
write_csv(f'outputs/rapid-review-screening-template-{VER}.csv', review_screening)

pilot_matrix = [
    {'pilot_domain':'Benefits schedule contact types','pilot_question':'Can defined contact benefits expand safe upstream care?','possible_sites':'Urban mixed practice, rural practice, kaupapa Maori provider, pharmacy-led site, urgent care/after-hours site','primary_outcomes':'Encounter volume, 7-day access, same-day urgent access, re-presentation, patient fee burden','design':'Stepped-wedge or matched comparison; prospective process evaluation'},
    {'pilot_domain':'Scope-enabled providers','pilot_question':'Which provider types safely generate additional activity within scope?','possible_sites':'NP-led, pharmacist, physiotherapy/MSK, mental health/HIP, paramedic alternative-care pathways','primary_outcomes':'Completed contacts, GP substitution, escalation, safety events, patient experience','design':'Contact-type pilot with clinical governance and safety audit'},
    {'pilot_domain':'Ambulance alternatives','pilot_question':'Do funded alternatives reduce ED conveyance without unsafe re-presentation?','possible_sites':'Regions with existing or planned extended care paramedic / treat-and-refer pathways','primary_outcomes':'Non-conveyance, ED presentation within 72h/7d, response times, patient satisfaction','design':'Interrupted time series or controlled before-after'},
    {'pilot_domain':'Direct claims / PHO optionality','pilot_question':'Do direct claims reduce transaction cost and entry barriers?','possible_sites':'New entrant providers, rural expansion providers, mixed PHO/direct model','primary_outcomes':'Onboarding time, payment lag, administrative cost, claim rejection, patient access','design':'Process evaluation plus comparative implementation study'},
]
write_csv(f'docs/pilot/pilot-evaluation-design-matrix-{VER}.csv', pilot_matrix)
write_csv(f'outputs/pilot-evaluation-design-matrix-{VER}.csv', pilot_matrix)

# Markdown documents
write('conductor/tracks/016-pragmatic-validation-without-calibration/metadata.json', json.dumps({
    'track':'016-pragmatic-validation-without-calibration','version':VER,'status':'complete','created':TODAY,
    'purpose':'Proceed without full predictive calibration by producing stakeholder validation, rapid review, OIA/data, priority empirical checks and pilot/evaluation artefacts.'
}, indent=2))
write('conductor/tracks/016-pragmatic-validation-without-calibration/spec.md', f'''
# Track 016 - Pragmatic validation without full calibration ({VER})

## Intent
Proceed with the recommended next phase without attempting a fully empirically calibrated predictive model.

## Deliverables
- Validation and translation report.
- Stakeholder MCDA/workshop pack.
- Evidence threshold matrix.
- Priority empirical checks register.
- OIA/data request tracker and draft request pack.
- Rapid scoping review protocol and screening templates.
- Prospective pilot/evaluation plan.
- Updated workbook, tables and figures.

## Boundary
This track does not claim predictive effect sizes, fiscal savings, or definitive causal estimates. It prepares the work for stakeholder validation and targeted empirical testing.
''')
write('conductor/tracks/016-pragmatic-validation-without-calibration/plan.md', f'''
# Plan - Track 016 ({VER})

1. Convert the conclusion "do not fully calibrate yet" into a defensible evidence threshold.
2. Identify the five most load-bearing empirical assumptions.
3. Prepare stakeholder validation and MCDA workshop materials.
4. Prepare OIA/data requests to make the funding architecture observable.
5. Prepare a PRISMA-ScR-aligned rapid scoping review protocol.
6. Prepare prospective pilot/evaluation options.
7. Generate an integrated report, workbook, figures and artefact index.
''')

# Core validation report markdown
source_refs = '\n'.join([f"- {s['source_id']}: {s['name']} - {s['url']}" for s in sources])
priority_md_rows = '\n'.join([f"| {r['priority_rank']} | {r['parameter']} | {r['policy_criticality_1_5']} | {r['initial_feasibility_1_5']} | {r['decision_use']} |" for r in priority_checks])
workplan_md_rows = '\n'.join([f"| {r['phase']} | {r['timeframe']} | {r['workstream']} | {r['outputs']} |" for r in validation_workplan])
threshold_rows = '\n'.join([f"| {r['output']} | {r['minimum_evidence_needed']} | {r['current_status']} |" for r in evidence_thresholds])
write(f'docs/validation/pragmatic-validation-plan-{VER}.md', f'''
# Pragmatic validation plan: proceed without a fully calibrated predictive model

Version: {VER}  
Date: {TODAY}

## Executive summary

The project should now proceed as a policy-synthesis and validation programme, not as a full national predictive modelling programme. The current artefacts provide a structured, source-informed and falsifiable policy hypothesis. They are enough for RACMA scoping, sector discussion, Substack publication, a policy brief and an NZMJ Viewpoint or methods/protocol article. They are not enough to make quantified claims about fiscal savings, ED reductions or exact supply effects.

The next phase should therefore focus on four practical outputs:

1. Stakeholder validation and game-informed MCDA.
2. A rapid scoping review/evidence map.
3. OIA and data requests to make the architecture observable.
4. Targeted empirical checks and a pilot/evaluation plan for the five most load-bearing assumptions.

## Position statement

A full empirically calibrated predictive model is not necessary now. It becomes necessary only if the work moves into an implementation business case or formal fiscal forecast. The appropriate immediate claim is:

> The current funding architecture may be strategically misaligned. The source-informed model demonstrates the mechanism and identifies what must be tested next; it does not estimate definitive effect sizes.

## Evidence threshold by output

| Output | Minimum evidence needed | Current status |
|---|---|---|
{threshold_rows}

## Five priority empirical checks

| Rank | Parameter | Criticality | Feasibility | Decision use |
|---:|---|---:|---:|---|
{priority_md_rows}

## Validation workplan

| Phase | Timeframe | Workstream | Output |
|---:|---|---|---|
{workplan_md_rows}

## What not to claim yet

Do not claim that the proposed architecture will reduce ED presentations by a specific percentage, save a specific amount of money, or definitively prove PHO intermediation causes market failure. Those claims require either empirical calibration, a pilot evaluation, or natural-experiment analysis.

## What can be claimed now

It is reasonable to claim that:

- the current public capitation reform is primarily an allocation/reweighting reform rather than a fundamental funding-architecture reform;
- a capitation-centred model can plausibly underfund marginal supply when workforce and access constraints bind;
- ambulance, ACC and scope-enabled providers are strategically relevant to upstream access;
- the games are structured, auditable and testable;
- stakeholder MCDA can expose where agreement and disagreement actually sit.

## Source anchors

{source_refs}
''')
write(f'outputs/pragmatic-validation-plan-{VER}.md', (ROOT/f'docs/validation/pragmatic-validation-plan-{VER}.md').read_text())

# Workshop pack
criteria_md = '\n'.join([f"| {cid} | {name} | {desc} |" for cid,name,desc in criteria])
games_md = '\n'.join([f"| {gid} | {name} | {desc} |" for gid,name,desc in stakeholder_games])
write(f'docs/validation/stakeholder-mcda-workshop-pack-{VER}.md', f'''
# Stakeholder MCDA and game-validation workshop pack

Version: {VER}  
Date: {TODAY}

## Purpose

The workshop is designed to test the policy-game map before any full predictive model is attempted. The aim is to determine whether informed stakeholders agree that the games are real, important, tractable and risky, and to compare policy options through an explicit MCDA process.

## Recommended participants

- General practice owners and salaried clinicians.
- Nurse practitioners, nurses, pharmacists, physiotherapists, mental health providers and paramedics.
- Rural providers and after-hours/urgent care providers.
- Kaupapa Maori and Pacific providers.
- PHO/locality representatives.
- Health NZ commissioning, hospital and ambulance leaders.
- ACC representatives.
- Treasury / fiscal-policy observers.
- Consumer and patient advocates.

## Workshop structure

1. Brief context and caveats: the model is source-informed and demonstrative, not predictive.
2. Game-position scoring: stakeholders rate each game.
3. Breakout discussion: disagreements and missing games.
4. Policy-option MCDA scoring.
5. Weight sensitivity: how rankings change for equity, fiscal, access and rural perspectives.
6. Agree top empirical checks and pilot options.

## The 14 games to validate

| Game | Name | Mechanism |
|---|---|---|
{games_md}

## Game-position scoring questions

For each game, participants score 1-5:

- Is this game real in New Zealand?
- How harmful is the current equilibrium if unresolved?
- How much does it contribute to hospital growth?
- How relevant is it to equity and Te Tiriti legitimacy?
- How tractable is reform?
- How risky is reform?
- How confident are you in your assessment?

## MCDA criteria

| Criterion | Name | Meaning |
|---|---|---|
{criteria_md}

## Interpretation

The workshop should not force consensus. Disagreement is useful. The key analytical outputs are:

- which games are accepted as real;
- which games are disputed;
- which assumptions require empirical testing;
- which policy options remain attractive under different stakeholder values;
- which risks need to be designed around before any pilot.

## Outputs

- Completed game-position scoring template.
- Completed policy-option MCDA template.
- Weighted and unweighted option ranking.
- Disagreement map by stakeholder group.
- Top five empirical checks and pilot priorities.
''')
write(f'outputs/stakeholder-mcda-workshop-pack-{VER}.md', (ROOT/f'docs/validation/stakeholder-mcda-workshop-pack-{VER}.md').read_text())

# Rapid review protocol
write(f'docs/review/rapid-scoping-review-protocol-{VER}.md', f'''
# Rapid scoping review protocol: primary care funding architecture, supply and hospital deflection

Version: {VER}  
Reporting standard: PRISMA-ScR

## Review question

What evidence exists that primary care payment and administrative architecture affects access, marginal supply, market entry, equity, ambulance/urgent-care pathways and hospital demand?

## Objectives

1. Identify evidence on fee-for-service, capitation, blended funding, direct claims and programme funding.
2. Map mechanisms linking funding architecture to supply and access.
3. Identify evidence on PHO/intermediary transaction costs and market entry.
4. Identify evidence on scope-enabled primary care supply.
5. Identify evidence linking unmet primary care need to ambulance, ED and hospital demand.
6. Identify evidence on co-payment effects and equity consequences.

## Inclusion criteria

- Primary care, urgent care, community care, ambulance/prehospital care or related upstream access models.
- Australia, New Zealand, comparable OECD systems, or transferable health economics/game-theory literature.
- Studies, reviews, policy reports, evaluations, modelling papers and grey literature.
- Outcomes: access, utilisation, supply, workforce, co-payments, equity, ED/hospital demand, safety, costs, market entry.

## Exclusion criteria

- Hospital-only payment models without upstream access relevance.
- Purely clinical studies without funding, access or system-design relevance.
- Opinion pieces without explicit policy mechanism, unless from major professional bodies or government.

## Databases and sources

Academic databases: MEDLINE, Embase, Scopus, Web of Science, EconLit, CINAHL, Cochrane, SSRN.  
Grey literature: Ministry of Health NZ, Health NZ, ACC, Treasury NZ, AIHW, Australian Department of Health, OECD, WHO, Commonwealth Fund, RACGP, ACRRM, RNZCGP, GPNZ, GenPro, RACMA.

## Core search concepts

- capitation OR fee-for-service OR blended payment OR pay-for-performance OR direct claims OR primary care benefits schedule;
- primary care OR general practice OR family medicine OR urgent care OR prehospital OR ambulance;
- supply OR access OR waiting time OR closed books OR market entry OR workforce;
- emergency department OR hospital admission OR potentially avoidable admission OR ambulatory sensitive hospitalisation;
- co-payment OR price elasticity OR patient charges OR equity.

## Extraction domains

- payment model;
- country/system;
- provider type;
- intermediary structure;
- access/supply outcome;
- hospital/ambulance outcome;
- equity outcome;
- fiscal outcome;
- mechanism;
- certainty and transferability to NZ/Australia.

## Deliverables

- Evidence map table.
- Mechanism matrix aligned to the 14 games.
- Short review memo for RACMA and policy audiences.
- Substack evidence explainer.
''')
write(f'outputs/rapid-scoping-review-protocol-{VER}.md', (ROOT/f'docs/review/rapid-scoping-review-protocol-{VER}.md').read_text())

# OIA request pack
request_md = []
for r in requests:
    request_md.append(f"""
## {r['request_id']}: {r['request_title']}

**Agency:** {r['agency']}  
**Purpose:** {r['purpose']}  
**Draft request text:**

I request, under the Official Information Act, copies of documents and data sufficient to describe: {r['core_items']}

Please include any calculation workbooks, schedules, operational guidance, implementation models, data dictionaries, attachments and related briefings. If any material is withheld, please provide the grounds for withholding and consider releasing partial or redacted versions.

**Source/context link:** {r['source_link']}
""")
write(f'docs/oia/oia-request-pack-{VER}.md', f'''
# OIA and data request pack

Version: {VER}

## Purpose

The following draft requests are designed to make the primary care funding and upstream access architecture observable enough for stakeholder validation and targeted empirical checks. They are not intended to support a full calibrated predictive model at this stage.

The Ministry of Health OIA page says requests should include the requester's name, contact details, and clear and specific details of the information requested: https://www.health.govt.nz/about-us/contact-us/oia-requests

{''.join(request_md)}
''')
write(f'outputs/oia-request-pack-{VER}.md', (ROOT/f'docs/oia/oia-request-pack-{VER}.md').read_text())

# Pilot evaluation plan
pilot_rows_md = '\n'.join([f"| {r['pilot_domain']} | {r['pilot_question']} | {r['primary_outcomes']} | {r['design']} |" for r in pilot_matrix])
write(f'docs/pilot/prospective-pilot-evaluation-plan-{VER}.md', f'''
# Prospective pilot and evaluation plan

Version: {VER}

## Aim

Design a staged evaluation pathway that tests the most important assumptions before New Zealand considers a large-scale implementation of a Primary Care Benefits Schedule or related upstream access architecture.

## Evaluation principles

- Test contact types before whole-system implementation.
- Separate scope-enabled supply from uncontrolled demand growth.
- Measure equity effects, not just volume.
- Include safety, re-presentation and escalation outcomes.
- Include ambulance and urgent-care alternatives as access infrastructure.
- Preserve capitation and continuity functions while testing marginal activity funding.

## Pilot domains

| Domain | Question | Primary outcomes | Suggested design |
|---|---|---|---|
{pilot_rows_md}

## Minimum measurement set

- Appointment wait time and urgent access.
- Encounter volume by provider type and contact type.
- Patient co-payment and fee distribution.
- Repeat contact and low-value-contact signals.
- ED presentation within 72 hours and 7 days after upstream contact.
- Admission and re-presentation where relevant.
- Ambulance conveyance/non-conveyance and ED handover delay.
- Patient experience and trust.
- Equity by deprivation, ethnicity, rurality, age and multimorbidity.
- Provider workload, viability and retention.

## Recommended evaluation design

A stepped-wedge or matched comparison design is preferred where feasible. If political or operational constraints prevent formal randomisation, use a prospective controlled before-after design with pre-specified outcomes and synthetic-control or difference-in-differences analysis where appropriate.

## Decision gates

1. Safety gate: no unacceptable increase in re-presentation, adverse events or missed escalation.
2. Equity gate: no material worsening in access or cost burden for high-need groups.
3. Supply gate: measurable increase in upstream capacity or appointment availability.
4. Hospital-interface gate: evidence of reduced avoidable ED/ambulance/hospital flow or improved disposition.
5. Fiscal/gaming gate: no unacceptable low-value activity or uncontrolled fiscal leakage.
''')
write(f'outputs/prospective-pilot-evaluation-plan-{VER}.md', (ROOT/f'docs/pilot/prospective-pilot-evaluation-plan-{VER}.md').read_text())

# Policy brief and Substack
write(f'docs/policy-briefs/brief-09-validation-without-full-calibration-{VER}.md', f'''
# Policy brief 09: What should be tested before a full predictive model?

Version: {VER}

## Position

A fully empirically calibrated predictive model is not required before this work is used for policy scoping, stakeholder engagement and a public argument. It is required only when decision-makers want quantified forecasts of hospital effects, fiscal impact or implementation business-case outcomes.

## Recommendation

Proceed with a pragmatic validation pathway:

1. Use the current source-informed model and game map to frame the policy problem.
2. Run stakeholder validation and game-informed MCDA.
3. Submit OIA/data requests to make the architecture transparent.
4. Complete a rapid scoping review/evidence map.
5. Test five priority assumptions.
6. Design a staged pilot/evaluation rather than a national forecasting exercise.

## Priority empirical assumptions

1. Marginal supply response to contact-based payment.
2. Unmet primary care conversion to ambulance/ED/hospital demand.
3. ACC activity funding stabilisation of primary care capacity.
4. PHO intermediation transaction-cost and entry-barrier effect.
5. Scope-enabled provider supply and safety.

## Preferred language

> The current work is a structured, source-informed and falsifiable policy hypothesis. It is sufficient to open the policy conversation and design validation. It is not yet a calibrated estimate of effect size.
''')
write(f'outputs/brief-09-validation-without-full-calibration-{VER}.md', (ROOT/f'docs/policy-briefs/brief-09-validation-without-full-calibration-{VER}.md').read_text())

write(f'docs/substack/post-11-what-we-need-to-test-next-{VER}.md', f'''
# What we need to test next

The question is not whether New Zealand needs a perfect predictive model before talking about primary care funding. It does not.

The better question is: which assumptions are so important that we should test them before implementing a major funding change?

Five matter most.

First, does a payment for defined primary care contacts actually increase supply, or does it simply change how existing work is labelled?

Second, when people cannot get timely primary care, how much of that need later appears as ambulance demand, emergency department presentations or hospital admissions?

Third, is ACC quietly stabilising general practice by providing an activity-based revenue stream that offsets the limits of capitation?

Fourth, do PHOs add population-health value, payment friction, or both?

Fifth, can a broader range of providers - pharmacists, nurse practitioners, nurses, physiotherapists, mental health providers and paramedics - safely generate primary care activity when funding follows contact type rather than professional guild boundaries?

A full predictive model can wait. The immediate task is to validate the games, make the hidden flows visible, and test the assumptions that would change the policy decision.
''')
write(f'outputs/post-11-what-we-need-to-test-next-{VER}.md', (ROOT/f'docs/substack/post-11-what-we-need-to-test-next-{VER}.md').read_text())

# Artefact index
artefacts = [
    {'artefact':'pragmatic-validation-plan','path':f'docs/validation/pragmatic-validation-plan-{VER}.md','purpose':'Main validation plan and evidence threshold.'},
    {'artefact':'stakeholder-workshop-pack','path':f'docs/validation/stakeholder-mcda-workshop-pack-{VER}.md','purpose':'Workshop guide and game validation structure.'},
    {'artefact':'rapid-review-protocol','path':f'docs/review/rapid-scoping-review-protocol-{VER}.md','purpose':'PRISMA-ScR aligned rapid review protocol.'},
    {'artefact':'OIA request pack','path':f'docs/oia/oia-request-pack-{VER}.md','purpose':'Draft information requests.'},
    {'artefact':'pilot evaluation plan','path':f'docs/pilot/prospective-pilot-evaluation-plan-{VER}.md','purpose':'Prospective evaluation design options.'},
    {'artefact':'priority empirical checks','path':f'docs/validation/priority-empirical-checks-{VER}.csv','purpose':'Five load-bearing assumptions.'},
    {'artefact':'stakeholder survey template','path':f'data/templates/stakeholder-game-validation-survey-{VER}.csv','purpose':'Scoring template for 14 games.'},
    {'artefact':'MCDA scoring template','path':f'data/templates/mcda-workshop-scoring-template-{VER}.csv','purpose':'Decision criteria and policy-option scoring.'},
]
write_csv(f'docs/validation/validation-artefact-index-{VER}.csv', artefacts)
write_csv(f'outputs/validation-artefact-index-{VER}.csv', artefacts)

# README/repo index and changelog/version updates
write(f'docs/repo-index-{VER}.md', f'''
# Repo index {VER}

This release proceeds with pragmatic validation rather than a fully calibrated predictive model. It adds stakeholder validation, MCDA workshop materials, OIA/data requests, a rapid scoping review protocol, priority empirical checks and prospective pilot/evaluation planning.

## Key folders

- `docs/validation/` - pragmatic validation plan, evidence thresholds, empirical checks, workshop pack.
- `docs/review/` - rapid scoping review protocol and screening materials.
- `docs/oia/` - draft data and OIA request pack.
- `docs/pilot/` - prospective pilot/evaluation plan.
- `outputs/` - standalone artefacts and final rendered documents.
- `data/templates/` - survey and MCDA templates.

## Status

The project remains source-informed and demonstrative. It is not yet a calibrated predictive model.
''')

# Update VERSION.md and CHANGELOG.md append
(ROOT/'VERSION.md').write_text(f"# Version\n\nCurrent version: {VER}\n\nRelease type: pragmatic validation without full predictive calibration.\n", encoding='utf-8')
changelog = (ROOT/'CHANGELOG.md').read_text(encoding='utf-8') if (ROOT/'CHANGELOG.md').exists() else ''
entry = f"""

## {VER} - Pragmatic validation without full calibration ({TODAY})

- Added validation and translation report artefacts.
- Added stakeholder game-validation and MCDA workshop pack.
- Added evidence threshold matrix and priority empirical checks.
- Added OIA/data request pack.
- Added rapid scoping review protocol and screening templates.
- Added prospective pilot/evaluation plan.
- Added validation workbook and figures.
- Did not attempt a fully empirically calibrated predictive model.
"""
(ROOT/'CHANGELOG.md').write_text(changelog.rstrip()+entry, encoding='utf-8')

print('v1.1.0 markdown/csv scaffold complete')
