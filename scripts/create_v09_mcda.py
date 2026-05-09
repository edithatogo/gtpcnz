from __future__ import annotations
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Mapping
import csv, json, os, subprocess, sys, zipfile, shutil
import pandas as pd
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT/'docs'
OUTPUTS = ROOT/'outputs'
FIGS = DOCS/'figures'
MCDA_DIR = DOCS/'mcda'
TEMPLATES = ROOT/'data/templates'
for p in [OUTPUTS, FIGS, MCDA_DIR, TEMPLATES, DOCS/'final', DOCS/'policy-briefs', DOCS/'substack', ROOT/'conductor/tracks/014-mcda-decision-support']:
    p.mkdir(parents=True, exist_ok=True)

@dataclass(frozen=True)
class Criterion:
    criterion_id: str
    criterion: str
    description: str
    default_weight: float
    related_games: str

@dataclass(frozen=True)
class PolicyOption:
    option_id: str
    option: str
    mapped_scenario: str
    description: str
    implementation_risk: float
    equity_risk_penalty: float
    fiscal_gaming_penalty: float

@dataclass(frozen=True)
class WeightSet:
    weight_set_id: str
    weight_set: str
    description: str
    weights: Mapping[str, float]

@dataclass(frozen=True)
class GamePosition:
    game_id: str
    game_name: str
    current_equilibrium: str
    better_equilibrium: str
    harm_if_unresolved: float
    hospital_growth_driver: float
    equity_relevance: float
    reform_tractability: float
    reform_risk: float
    confidence: float
    rationale: str

CRITERIA = (
    Criterion('C1','Access and supply generation','Whether the option increases safe upstream primary, urgent and ambulance capacity.',14,'G3, G4, G8'),
    Criterion('C2','Hospital deflection','Whether the option reduces avoidable ED, ambulance conveyance and hospital admission flow.',14,'G1, G2, G7'),
    Criterion('C3','Equity and Te Tiriti legitimacy','Whether access expands without worsening inequity, trust, Maori/Pacific provider legitimacy or co-payment barriers.',14,'G10, G12'),
    Criterion('C4','Rural and in-person resilience','Whether the option protects local in-person capacity rather than substituting telehealth only.',9,'G7, G8, G9'),
    Criterion('C5','Fiscal sustainability','Whether the model is affordable, controllable and transparent to central fiscal decision-makers.',12,'G1, G2, G6, G10'),
    Criterion('C6','Gaming and low-value activity risk','Whether it avoids avoidable churn, opportunistic claiming and provider-induced demand.',10,'G3, G5, G10, G13'),
    Criterion('C7','Administrative simplicity and market entry','Whether it lowers transaction costs and barriers to market entry or expansion.',9,'G5, G8, G14'),
    Criterion('C8','Governance and clinical safety','Whether scope, prescribing, referral, audit, clinical governance and accountability controls are strong.',10,'G8, G11, G14'),
    Criterion('C9','Political feasibility','Whether the option can survive institutional contestation and be framed coherently.',5,'G5, G12, G13'),
    Criterion('C10','Data and accountability readiness','Whether outcomes, contacts and downstream flows can be measured and reported at top-tier level.',8,'G11, G14'),
)

POLICY_OPTIONS = (
    PolicyOption('O0','Status quo tight control','S0','Existing dominant capitation/PHO/contracting architecture with constrained upstream expansion.',1.5,1.5,1.0),
    PolicyOption('O1','Capitation reweighting only','S1','Improve allocation of capitation without changing supply architecture.',1.3,0.7,0.8),
    PolicyOption('O2','Capitation reweighting plus access target','S1+target','Add top-level access target to reweighted capitation.',1.5,0.7,1.4),
    PolicyOption('O3','Primary Care Benefits Schedule','S2','Defined contact-type benefits, demand-driven within rules, retaining capitation for continuity.',2.4,1.0,2.2),
    PolicyOption('O4','Benefits schedule plus scope-enabled eligibility','S2+scope','Allow eligible activity by GPs, NPs, pharmacists, allied health, paramedics and other accredited providers within scope.',3.0,1.2,2.6),
    PolicyOption('O5','Full upstream access architecture','S3','Benefits schedule plus scope governance, equity protections, direct/optional claiming, ambulance alternatives, PHO-function reform, data, KPIs and audit.',2.75,0.7,2.3),
    PolicyOption('O6','Loose demand-driven benefits with weak controls','S4','High activity funding with weak scope, audit, equity, data and co-payment controls.',4.5,4.0,3.8333333333333),
    PolicyOption('O7','ACC/ambulance alternatives strengthened only','partial','Strengthen ambulance alternatives and ACC/prehospital funding, without primary care architecture reform.',2.0,1.2,1.2),
    PolicyOption('O8','PHO reform/direct claims only','partial','Reduce PHO payment intermediation and allow direct rules-based claiming, without comprehensive benefits/scope reform.',2.9,1.5,2.3),
    PolicyOption('O9','Hospital investment priority only','hospital','Prioritise hospital capacity and acute rescue while leaving upstream access constrained.',1.75,1.5,1.0),
)

# option, criterion, raw score -2/+2, confidence, rationale
POLICY_SCORE_ROWS = (
    # O0
    ('O0','C1',-1.2,0.85,'Constrained marginal supply and market entry.'),('O0','C2',-1.2,0.80,'Unmet need remains channelled into hospitals.'),('O0','C3',-0.8,0.70,'Equity barriers persist through waiting, co-payment and access friction.'),('O0','C4',-0.8,0.70,'Rural local supply remains fragile.'),('O0','C5',0.4,0.60,'Short-term fiscal containment, but downstream hospital risk.'),('O0','C6',0.5,0.75,'Low direct claiming risk, but hidden under-service risk.'),('O0','C7',-0.8,0.65,'PHO/intermediated pathways remain complex.'),('O0','C8',0.1,0.60,'Existing governance familiar but incomplete for upstream outcomes.'),('O0','C9',0.7,0.70,'Politically familiar.'),('O0','C10',-0.5,0.65,'Upstream unmet need remains poorly visible.'),
    # O1
    ('O1','C1',-0.1,0.80,'Better allocation but weak marginal supply signal.'),('O1','C2',-0.2,0.75,'Some access improvement but hospital-pressure mechanism remains.'),('O1','C3',0.6,0.80,'Better need weighting.'),('O1','C4',0.2,0.65,'Rurality weighting helps but does not guarantee local capacity.'),('O1','C5',0.2,0.70,'Contained and predictable.'),('O1','C6',0.4,0.75,'Low activity gaming risk.'),('O1','C7',-0.1,0.65,'Administrative structure mostly unchanged.'),('O1','C8',0.2,0.65,'Familiar governance.'),('O1','C9',0.3,0.70,'Politically safer than structural reform.'),('O1','C10',0.2,0.65,'Some measurement improvement only.'),
    # O2
    ('O2','C1',0.0,0.75,'Target may increase attention but not necessarily capacity.'),('O2','C2',0.1,0.70,'Potential deflection if target influences funding.'),('O2','C3',0.6,0.75,'Better allocation and visibility.'),('O2','C4',0.2,0.60,'May not protect in-person rural supply.'),('O2','C5',0.1,0.65,'Target can create pressure without matched funding.'),('O2','C6',0.4,0.70,'Low activity gaming risk.'),('O2','C7',0.0,0.60,'Market entry mostly unchanged.'),('O2','C8',0.3,0.65,'Accountability improves.'),('O2','C9',0.4,0.70,'Politically feasible.'),('O2','C10',0.6,0.75,'Access target and dataset improve observability.'),
    # O3
    ('O3','C1',1.45,0.70,'Adds marginal payment for defined contacts.'),('O3','C2',1.1,0.65,'More upstream activity may reduce avoidable hospital flow.'),('O3','C3',0.4,0.55,'Equity depends on co-payment design.'),('O3','C4',0.6,0.55,'Can include rural/in-person loadings.'),('O3','C5',-0.2,0.50,'Demand-driven exposure needs fiscal controls.'),('O3','C6',-0.1,0.50,'Gaming risk manageable if contact types are defined.'),('O3','C7',0.8,0.65,'Direct benefits improve portability.'),('O3','C8',0.4,0.55,'Needs scope and audit framework.'),('O3','C9',-0.1,0.50,'Contestable but patient-access framing helps.'),('O3','C10',0.8,0.65,'Claims platform improves observability.'),
    # O4
    ('O4','C1',1.9,0.65,'Scope-enabled claiming expands supply.'),('O4','C2',1.3,0.60,'More upstream access may deflect hospital flow.'),('O4','C3',0.5,0.55,'Potential equity gain if high-need providers are included.'),('O4','C4',1.0,0.60,'Can improve rural supply if local non-GP providers claim.'),('O4','C5',-0.4,0.45,'More providers increase fiscal exposure.'),('O4','C6',-0.3,0.45,'Low-value activity risk rises without tight governance.'),('O4','C7',1.3,0.60,'Major market-entry gain.'),('O4','C8',0.2,0.50,'Clinical safety depends on scope rules and audit.'),('O4','C9',-0.4,0.45,'Professional contestation likely.'),('O4','C10',0.7,0.60,'Claiming data improves visibility.'),
    # O5
    ('O5','C1',1.9,0.70,'Strong supply architecture with governance.'),('O5','C2',1.7,0.65,'Best whole-system hospital-deflection logic.'),('O5','C3',1.5,0.60,'Equity protections and retained relational functions.'),('O5','C4',1.5,0.65,'Rural/in-person loading and ambulance alternatives.'),('O5','C5',0.5,0.50,'Demand-driven but controlled by rules and audit.'),('O5','C6',0.8,0.55,'Controls reduce low-value activity risk.'),('O5','C7',1.3,0.65,'Direct/optional claims reduce friction.'),('O5','C8',1.3,0.60,'Governance designed into architecture.'),('O5','C9',0.0,0.45,'Complex but coalition-building possible.'),('O5','C10',1.6,0.70,'Data visibility and top-tier KPIs.'),
    # O6
    ('O6','C1',1.4,0.65,'Access expands.'),('O6','C2',0.8,0.55,'Some deflection but poorly controlled.'),('O6','C3',-0.8,0.50,'Co-payment and provider-induced patterns may worsen inequity.'),('O6','C4',0.4,0.45,'May not protect rural in-person care.'),('O6','C5',-1.5,0.65,'High fiscal exposure.'),('O6','C6',-1.6,0.70,'High gaming/low-value risk.'),('O6','C7',1.0,0.55,'Entry improves.'),('O6','C8',-1.2,0.60,'Weak governance.'),('O6','C9',-0.8,0.55,'Politically vulnerable.'),('O6','C10',0.3,0.50,'More claims data but weak accountability.'),
    # O7
    ('O7','C1',0.5,0.60,'Improves urgent/prehospital supply but primary care remains constrained.'),('O7','C2',0.7,0.65,'Ambulance alternatives can reduce ED flow.'),('O7','C3',0.3,0.55,'Equity depends on access pathway design.'),('O7','C4',0.5,0.60,'Useful rural lever.'),('O7','C5',0.0,0.50,'May save hospital costs but needs funding.'),('O7','C6',0.2,0.55,'Moderate risk if protocols tight.'),('O7','C7',0.2,0.50,'Does not solve PHO/primary care entry.'),('O7','C8',0.5,0.60,'Paramedic protocols can be governed.'),('O7','C9',0.3,0.55,'Usually more feasible than PHO/GP funding reform.'),('O7','C10',0.6,0.60,'Ambulance data already relatively mature.'),
    # O8
    ('O8','C1',0.4,0.55,'Direct claiming may enable entry but no contact benefits.'),('O8','C2',0.2,0.50,'Indirect hospital effect only.'),('O8','C3',0.0,0.45,'Equity depends on replacement functions.'),('O8','C4',0.2,0.45,'Potential rural entry but not guaranteed.'),('O8','C5',0.2,0.50,'Simplification may reduce costs.'),('O8','C6',0.0,0.45,'Claiming risk depends on rules.'),('O8','C7',1.5,0.60,'Strongest market-entry simplification.'),('O8','C8',0.3,0.50,'Needs replacement accountability.'),('O8','C9',-0.8,0.45,'Institutional contestation likely.'),('O8','C10',0.3,0.55,'Direct claims can improve data if designed well.'),
    # O9
    ('O9','C1',-0.8,0.80,'Upstream supply remains constrained.'),('O9','C2',-0.4,0.75,'May treat hospital pressure after the fact.'),('O9','C3',-0.2,0.65,'Does not address upstream access equity.'),('O9','C4',-0.3,0.60,'Rural upstream access may remain weak.'),('O9','C5',-0.8,0.65,'High-cost sector absorbs growth.'),('O9','C6',0.7,0.70,'Low claiming-gaming risk, but high system opportunity cost.'),('O9','C7',0.5,0.65,'Administratively familiar.'),('O9','C8',0.5,0.70,'Hospital governance strong.'),('O9','C9',0.6,0.75,'Politically familiar rescue model.'),('O9','C10',0.2,0.65,'Hospital data visible, upstream data still incomplete.'),
)

WEIGHT_SETS = (
    WeightSet('W0','Balanced policy','Default weights for whole-system decision-making.', {c.criterion_id:c.default_weight for c in CRITERIA}),
    WeightSet('W1','Equity and Te Tiriti focused','Prioritises equity, trust, access and rural resilience.', {'C1':14,'C2':10,'C3':25,'C4':12,'C5':8,'C6':6,'C7':5,'C8':9,'C9':4,'C10':6}),
    WeightSet('W2','Fiscal-control focused','Prioritises fiscal sustainability, gaming risk and governance.', {'C1':10,'C2':12,'C3':10,'C4':5,'C5':25,'C6':15,'C7':5,'C8':10,'C9':4,'C10':4}),
    WeightSet('W3','Rural access focused','Prioritises local in-person resilience and access.', {'C1':18,'C2':12,'C3':15,'C4':20,'C5':8,'C6':6,'C7':6,'C8':8,'C9':3,'C10':8}),
    WeightSet('W4','Hospital-pressure focused','Prioritises hospital deflection, upstream access and data visibility.', {'C1':15,'C2':25,'C3':10,'C4':8,'C5':12,'C6':8,'C7':5,'C8':9,'C9':3,'C10':10}),
    WeightSet('W5','Market-entry focused','Prioritises administrative simplicity, entry, access and governance.', {'C1':15,'C2':10,'C3':10,'C4':8,'C5':8,'C6':8,'C7':20,'C8':9,'C9':5,'C10':7}),
)

GAME_POSITIONS = (
    GamePosition('G1','Hospital-salience budget game','hospital-rescue equilibrium','upstream-salience equilibrium',5,5,4,3,3,4,'Hospital pressure is visible, urgent and fundable; upstream failure is dispersed.'),
    GamePosition('G2','Health NZ internal allocation game','hospital-operations dominance','balanced internal accountability',4,5,3,3,3,3,'Hospital operational risk may dominate internal allocation attention.'),
    GamePosition('G3','Capitation marginal-supply game','marginal-rationing equilibrium','marginal-expansion equilibrium',5,4,4,4,3,4,'Weak marginal contact payment can constrain additional clinically necessary work.'),
    GamePosition('G4','Consumer access pathway game','delay/pay/ED substitution','early-access equilibrium',4,4,5,3,3,3,'Consumers route around delays via co-payment, telehealth, ambulance or ED.'),
    GamePosition('G5','PHO intermediation game','intermediated-gatekeeping equilibrium','optional value-adding support',4,3,3,3,4,2.5,'PHO functions may add value, but payment intermediation may add friction.'),
    GamePosition('G6','ACC/Health NZ cross-funder game','cross-subsidy opacity','whole-system funding visibility',4,4,3,3,3,2.5,'ACC activity funding may stabilise supply; isolating it may shift pressure elsewhere.'),
    GamePosition('G7','Ambulance conveyance game','ED-conveyance default','safe alternative-disposition equilibrium',4,5,4,4,3,3.5,'Ambulance alternatives need funding, governance and follow-up.'),
    GamePosition('G8','Scope-of-practice supply game','professional-bottleneck equilibrium','scope-enabled supply equilibrium',5,4,4,4,4,3,'Funding eligibility may be narrower than safe clinical scope.'),
    GamePosition('G9','Telehealth/local-supply game','telehealth-substitution/fragmentation','integrated hybrid-access equilibrium',3,3,4,3,3,3,'Telehealth extends access but may erode local supply if poorly integrated.'),
    GamePosition('G10','Co-payment calibration game','price-rationing equity failure','calibrated co-payment equilibrium',4,4,5,3,4,3,'Co-payment can signal demand or deter necessary care.'),
    GamePosition('G11','KPI salience game','hospital-target dominance','upstream target salience',5,5,4,4,2,4,'Top-tier KPIs determine what becomes managed.'),
    GamePosition('G12','Equity and trust game','transactional-access without trust','benefits plus equity-function equilibrium',5,3,5,3,4,3,'Access benefits do not replace relational and kaupapa Maori/Pacific/locality functions.'),
    GamePosition('G13','Political economy game','institutional-defence equilibrium','access-architecture coalition',3,3,3,2,5,3,'Reform framing determines coalition formation and resistance.'),
    GamePosition('G14','Data observability game','hidden-unmet-need equilibrium','observable upstream-flow equilibrium',5,5,4,4,2,4,'Unobserved upstream need remains less fundable than visible hospital pressure.'),
)

def normalise_weights(weights: Mapping[str,float]) -> dict[str,float]:
    total = float(sum(weights.values()))
    if total <= 0: raise ValueError('weights must sum to a positive value')
    return {k:100*float(v)/total for k,v in weights.items()}

def confidence_adjusted_criterion_score(raw_score: float, confidence: float) -> float:
    if raw_score < -2 or raw_score > 2: raise ValueError('raw_score must be between -2 and +2')
    confidence = max(0.0, min(1.0, confidence))
    return 50.0 + (raw_score/2.0)*50.0*confidence

def criteria_frame(): return pd.DataFrame([asdict(c) for c in CRITERIA])
def policy_options_frame(): return pd.DataFrame([asdict(o) for o in POLICY_OPTIONS])
def policy_scores_frame(): return pd.DataFrame([{'option_id':o,'criterion_id':c,'raw_score_minus2_to_plus2':raw,'confidence_0_to_1':conf,'rationale':rat} for o,c,raw,conf,rat in POLICY_SCORE_ROWS])
def weight_sets_frame():
    rows=[]
    for ws in WEIGHT_SETS:
        row={'weight_set_id':ws.weight_set_id,'weight_set':ws.weight_set,'description':ws.description}; row.update(normalise_weights(ws.weights)); rows.append(row)
    return pd.DataFrame(rows)

def game_priority_score(g: GamePosition) -> float:
    raw = 0.28*g.harm_if_unresolved + 0.24*g.hospital_growth_driver + 0.20*g.equity_relevance + 0.15*g.reform_tractability + 0.13*g.confidence - 0.12*g.reform_risk
    return max(0.0, min(100.0, raw/5.0*100.0))

def game_positions_frame():
    rows=[]
    for g in GAME_POSITIONS:
        row=asdict(g); row['priority_score_0_to_100']=round(game_priority_score(g),2); rows.append(row)
    return pd.DataFrame(rows)

def option_score(option_id: str, weights: Mapping[str,float]) -> dict[str,object]:
    weights=normalise_weights(weights)
    score_rows=policy_scores_frame()
    option_rows=score_rows[score_rows['option_id']==option_id]
    options={o.option_id:o for o in POLICY_OPTIONS}
    if option_id not in options: raise KeyError(option_id)
    if len(option_rows)!=len(CRITERIA): raise ValueError(f'option {option_id} has incomplete scoring rows')
    weighted_total=0.0; raw_weighted_total=0.0; contributions={}
    for _, row in option_rows.iterrows():
        cid=str(row['criterion_id']); raw=float(row['raw_score_minus2_to_plus2']); conf=float(row['confidence_0_to_1'])
        adjusted=confidence_adjusted_criterion_score(raw, conf)
        contribution=weights[cid]*adjusted/100.0
        weighted_total += contribution
        raw_weighted_total += weights[cid]*raw/100.0
        contributions[f'contribution_{cid}']=round(contribution,3)
    option=options[option_id]
    risk_penalty=2.0*option.implementation_risk+2.0*option.equity_risk_penalty+1.5*option.fiscal_gaming_penalty
    risk_adjusted_score=max(0.0,min(100.0,weighted_total-risk_penalty))
    return {'option_id':option.option_id,'option':option.option,'mapped_scenario':option.mapped_scenario,'weighted_total_before_penalty':round(weighted_total,2),'risk_penalty':round(risk_penalty,2),'risk_adjusted_score':round(risk_adjusted_score,2),'raw_weighted_direction_minus2_to_plus2':round(raw_weighted_total,3),**contributions}

def run_mcda(weight_set=None):
    if weight_set is None:
        weights={c.criterion_id:c.default_weight for c in CRITERIA}; weight_set_id='W0'; weight_set_name='Balanced policy'
    elif isinstance(weight_set, WeightSet):
        weights=weight_set.weights; weight_set_id=weight_set.weight_set_id; weight_set_name=weight_set.weight_set
    else:
        weights=weight_set; weight_set_id='custom'; weight_set_name='Custom weights'
    rows=[]
    for option in POLICY_OPTIONS:
        row=option_score(option.option_id, weights); row['weight_set_id']=weight_set_id; row['weight_set']=weight_set_name; rows.append(row)
    df=pd.DataFrame(rows); df['rank']=df['risk_adjusted_score'].rank(ascending=False, method='min').astype(int)
    return df.sort_values(['rank','risk_adjusted_score'], ascending=[True,False]).reset_index(drop=True)

def run_all_weight_sets(): return pd.concat([run_mcda(ws) for ws in WEIGHT_SETS], ignore_index=True)
def score_template_rows():
    rows=[]
    for opt in POLICY_OPTIONS:
        for c in CRITERIA:
            rows.append({'option_id':opt.option_id,'option':opt.option,'criterion_id':c.criterion_id,'criterion':c.criterion,'raw_score_minus2_to_plus2':'','confidence_0_to_1':'','rationale':''})
    return pd.DataFrame(rows)
def game_position_template_rows():
    df=game_positions_frame().copy()
    for col in ['harm_if_unresolved','hospital_growth_driver','equity_relevance','reform_tractability','reform_risk','confidence']:
        df[col]=''
    df['priority_score_0_to_100']=''
    return df

# Write module
module_text = Path(__file__).read_text().split('# Write module')[0]
# remove script-specific ROOT definitions? simpler: write curated module from current file between dataclasses and this marker.
module_text = module_text.replace("ROOT = Path(__file__).resolve().parents[1]\nDOCS = ROOT/'docs'\nOUTPUTS = ROOT/'outputs'\nFIGS = DOCS/'figures'\nMCDA_DIR = DOCS/'mcda'\nTEMPLATES = ROOT/'data/templates'\nfor p in [OUTPUTS, FIGS, MCDA_DIR, TEMPLATES, DOCS/'final', DOCS/'policy-briefs', DOCS/'substack', ROOT/'conductor/tracks/014-mcda-decision-support']:\n    p.mkdir(parents=True, exist_ok=True)\n\n", "")
module_text = module_text.replace("import csv, json, os, subprocess, sys, zipfile, shutil\n", "")
module_text += "\nif __name__ == '__main__':\n    print(run_mcda().to_string(index=False))\n"
(ROOT/'models/primarycare_model/mcda.py').write_text(module_text)
init = ROOT/'models/primarycare_model/__init__.py'
init.write_text((init.read_text() if init.exists() else '').rstrip() + '\n# MCDA decision-support layer added in v0.9.0.\n')

# Test file
(ROOT/'models/tests/test_mcda.py').write_text('''from primarycare_model.mcda import CRITERIA, GAME_POSITIONS, POLICY_OPTIONS, WEIGHT_SETS, game_positions_frame, run_all_weight_sets, run_mcda, score_template_rows\n\n\ndef test_mcda_dimensions():\n    assert len(CRITERIA) == 10\n    assert len(POLICY_OPTIONS) == 10\n    assert len(WEIGHT_SETS) == 6\n    assert len(GAME_POSITIONS) == 14\n\n\ndef test_default_mcda_ranking_is_plausible():\n    df = run_mcda()\n    top = df.iloc[0]\n    assert top["option_id"] == "O5"\n    loose = df[df["option_id"] == "O6"].iloc[0]\n    pcbs = df[df["option_id"] == "O3"].iloc[0]\n    assert pcbs["risk_adjusted_score"] > loose["risk_adjusted_score"]\n\n\ndef test_all_weight_sets_have_rankings():\n    df = run_all_weight_sets()\n    assert set(df["weight_set_id"]) == {ws.weight_set_id for ws in WEIGHT_SETS}\n    assert df.groupby("weight_set_id").size().min() == len(POLICY_OPTIONS)\n\n\ndef test_game_priority_scores_bounded():\n    df = game_positions_frame()\n    assert df["priority_score_0_to_100"].between(0, 100).all()\n    assert df.sort_values("priority_score_0_to_100", ascending=False).iloc[0]["game_id"] in {"G1", "G11", "G14", "G3"}\n\n\ndef test_score_template_complete():\n    df = score_template_rows()\n    assert len(df) == len(CRITERIA) * len(POLICY_OPTIONS)\n''')

# Outputs
criteria_frame().to_csv(OUTPUTS/'mcda-criteria-v0.9.0.csv', index=False)
policy_options_frame().to_csv(OUTPUTS/'mcda-policy-options-v0.9.0.csv', index=False)
policy_scores_frame().to_csv(OUTPUTS/'mcda-policy-option-scorecard-v0.9.0.csv', index=False)
weight_sets_frame().to_csv(OUTPUTS/'mcda-weight-sets-v0.9.0.csv', index=False)
game_positions_frame().to_csv(OUTPUTS/'mcda-game-position-example-v0.9.0.csv', index=False)
run_mcda().to_csv(OUTPUTS/'mcda-example-results-v0.9.0.csv', index=False)
run_all_weight_sets().to_csv(OUTPUTS/'mcda-weight-sensitivity-v0.9.0.csv', index=False)
score_template_rows().to_csv(TEMPLATES/'policy-option-mcda-template-v0.9.0.csv', index=False)
game_position_template_rows().to_csv(TEMPLATES/'game-position-scoring-template-v0.9.0.csv', index=False)

# Figures
rank=run_mcda().sort_values('risk_adjusted_score', ascending=True)
plt.figure(figsize=(9.5,6.0)); plt.barh(rank['option'], rank['risk_adjusted_score']); plt.xlabel('Risk-adjusted MCDA score (0-100)'); plt.title('Game-informed MCDA ranking - balanced weights'); plt.tight_layout(); plt.savefig(FIGS/'mcda-default-ranking-v0.9.0.png', dpi=200); plt.savefig(OUTPUTS/'mcda-default-ranking-v0.9.0.png', dpi=200); plt.close()
priority=game_positions_frame().sort_values('priority_score_0_to_100', ascending=True)
plt.figure(figsize=(9.5,6.8)); plt.barh(priority['game_id']+' '+priority['game_name'], priority['priority_score_0_to_100']); plt.xlabel('Diagnostic priority score (0-100)'); plt.title('Which games most need decision-maker attention?'); plt.tight_layout(); plt.savefig(FIGS/'mcda-game-priority-v0.9.0.png', dpi=200); plt.savefig(OUTPUTS/'mcda-game-priority-v0.9.0.png', dpi=200); plt.close()
sens=run_all_weight_sets(); selected=sens[sens['option_id'].isin(['O1','O3','O5','O6','O8','O9'])]; pivot=selected.pivot(index='weight_set', columns='option', values='risk_adjusted_score')
plt.figure(figsize=(10,6));
for col in pivot.columns: plt.plot(pivot.index, pivot[col], marker='o', label=col)
plt.ylabel('Risk-adjusted MCDA score'); plt.title('MCDA sensitivity across stakeholder weight sets'); plt.xticks(rotation=35, ha='right'); plt.legend(fontsize=7, loc='best'); plt.tight_layout(); plt.savefig(FIGS/'mcda-weight-sensitivity-v0.9.0.png', dpi=200); plt.savefig(OUTPUTS/'mcda-weight-sensitivity-v0.9.0.png', dpi=200); plt.close()

# Markdown helpers
def md_table(df, cols=None, max_rows=None):
    if cols: df=df[cols]
    if max_rows: df=df.head(max_rows)
    return df.to_markdown(index=False)
criteria=criteria_frame(); results=run_mcda(); weights=weight_sets_frame(); games=game_positions_frame(); opts=policy_options_frame(); sens=run_all_weight_sets()
rank_table=results[['rank','option_id','option','weighted_total_before_penalty','risk_penalty','risk_adjusted_score']]
game_table=games[['game_id','game_name','current_equilibrium','better_equilibrium','priority_score_0_to_100']].sort_values('priority_score_0_to_100', ascending=False)
criteria_table=criteria[['criterion_id','criterion','default_weight','related_games']]
weight_summary=sens.pivot(index='option', columns='weight_set', values='rank').reset_index()

(MCDA_DIR/'mcda-framework-v0.9.0.md').write_text(f'''# Game-informed MCDA framework v0.9.0\n\n## Purpose\n\nThis framework adds a deliberative multi-criteria decision analysis layer to the New Zealand primary care funding architecture work. The earlier artefacts mapped the strategic games, created demonstrative models, stress-tested them under uncertainty, and synthesised them into a hybrid model. This MCDA layer is designed to help decision-makers ask a different question:\n\n> Where do we think each game currently sits, how important is it, how confident are we, and which policy option best shifts the system toward a better equilibrium?\n\nThe MCDA is not intended to prove the policy case. It is intended to make judgement explicit. It separates empirical claims, model assumptions, value weights and implementation risk.\n\n## Two-layer design\n\n### Layer 1: diagnostic game-position mapping\n\nDecision-makers score the 14 mapped games by harm, hospital growth contribution, equity relevance, tractability, reform risk and confidence. This identifies which strategic traps need attention before options are ranked.\n\n### Layer 2: policy-option MCDA\n\nDecision-makers score policy options against 10 criteria. Criteria weights can be varied by stakeholder perspective: balanced policy, equity and Te Tiriti, fiscal control, rural access, hospital pressure, and market entry.\n\n## Default criteria\n\n{md_table(criteria_table)}\n\n## Default policy options\n\n{md_table(opts[['option_id','option','mapped_scenario']])}\n\n## Scoring scale\n\n| Score | Meaning |\n|---:|---|\n| -2 | Substantially worsens the criterion |\n| -1 | Slightly worsens the criterion |\n| 0 | No material change or genuinely uncertain direction |\n| +1 | Slightly improves the criterion |\n| +2 | Substantially improves the criterion |\n\nEach score has a confidence rating from 0 to 1. Low-confidence scores are pulled toward neutral in the example model rather than being treated as certain.\n\n## Risk adjustment\n\nThe example model applies option-level penalties for implementation risk, equity risk and fiscal/gaming risk. This is important because a policy option can score well on access while still being unsafe, inequitable or fiscally unstable.\n\n## Default result\n\n{md_table(rank_table)}\n\nThe default demonstrative MCDA ranks the full upstream access architecture first, followed by the Primary Care Benefits Schedule and the benefits schedule plus scope-enabled eligibility. Loose benefits with weak controls rank last after risk adjustment.\n\n## Interpretation\n\nThe MCDA supports the same core conclusion as the hybrid model, but through a decision-maker lens:\n\n> Demand-driven within rules; not demand-driven without rules.\n''')

(MCDA_DIR/'game-position-scoring-rubric-v0.9.0.md').write_text(f'''# Game-position scoring rubric v0.9.0\n\nThis rubric is used before ranking policy options. It asks decision-makers to locate each mapped game in the current system.\n\n## Questions for each game\n\n| Field | Scale | Question |\n|---|---:|---|\n| Harm if unresolved | 1-5 | How damaging is the current equilibrium if left unresolved? |\n| Hospital growth driver | 1-5 | How strongly does this game channel unmet need or resources toward hospitals? |\n| Equity relevance | 1-5 | How strongly does the game affect equity, Te Tiriti legitimacy, trust or high-need groups? |\n| Reform tractability | 1-5 | How feasible is it to shift the game through policy? |\n| Reform risk | 1-5 | How risky is reform if poorly designed? |\n| Confidence | 1-5 | How confident are we in our assessment? |\n\n## Example diagnostic scoring\n\n{md_table(game_table)}\n\n## Workshop use\n\nThe facilitator should invite disagreement. A low score is not a failure. It indicates either lower priority, lower confidence, or a need for better evidence. The most useful output is often the disagreement pattern between stakeholder groups.\n''')

(MCDA_DIR/'policy-option-mcda-rubric-v0.9.0.md').write_text(f'''# Policy-option MCDA scoring rubric v0.9.0\n\n## Criteria\n\n{md_table(criteria_table)}\n\n## Scoring steps\n\n1. Agree on the policy options to score.\n2. Agree on criteria and weights.\n3. Score each option against each criterion using the -2 to +2 scale.\n4. Record confidence for each score.\n5. Apply risk penalties separately.\n6. Run sensitivity analysis across stakeholder weight sets.\n7. Interpret the ranking, not as a command, but as structured decision support.\n\n## Default options\n\n{md_table(opts[['option_id','option','description']])}\n\n## Important caution\n\nThe MCDA should never hide unresolved evidence questions. If participants disagree because evidence is weak, the correct output is not forced consensus. The correct output is a validation task.\n''')

(MCDA_DIR/'stakeholder-workshop-guide-v0.9.0.md').write_text('''# Stakeholder workshop guide v0.9.0\n\n## Purpose\n\nTo test the game map and MCDA with stakeholders before moving to empirical calibration or policy endorsement.\n\n## Suggested participants\n\n- General practice owners and salaried clinicians.\n- Nurse practitioners, pharmacists, allied health providers and paramedics.\n- PHO/locality leaders.\n- Maori and Pacific providers.\n- Rural providers.\n- ACC, Health NZ, Ministry and Treasury officials or former officials.\n- Ambulance and emergency care leaders.\n- Hospital executives and ED clinicians.\n- Consumer and patient advocates.\n\n## Session structure\n\n### Part 1: Orient to the thesis\n\nPresent the thesis:\n\n> Tightly managing primary care and ambulance activity may channel growth into hospitals by default.\n\nClarify that the work is a falsifiable policy hypothesis, not proof.\n\n### Part 2: Game-position scoring\n\nParticipants score each game using the game-position template. Capture individual and group ratings.\n\n### Part 3: Policy-option scoring\n\nParticipants score the policy options using the policy-option MCDA template.\n\n### Part 4: Weighting exercise\n\nParticipants choose or construct a weight set. Suggested starting sets are balanced, equity-focused, fiscal-control, rural-access, hospital-pressure, and market-entry focused.\n\n### Part 5: Sensitivity and disagreement\n\nReview how rankings change by weight set. Ask where disagreement reflects values, evidence gaps, implementation risk, professional interests or fiscal assumptions.\n\n### Part 6: Validation backlog\n\nTurn uncertainty into validation tasks: data requests, OIA requests, modelling tests and stakeholder interviews.\n\n## Outputs\n\n- Group-weighted MCDA results.\n- Stakeholder-specific rankings.\n- Disagreement map.\n- Validation backlog.\n- Revised game map.\n''')

(MCDA_DIR/'weighting-methods-note-v0.9.0.md').write_text(f'''# Weighting methods note v0.9.0\n\n## Default approach\n\nThe current package uses simple weighted-sum MCDA. This is intentionally transparent and easy to use in workshops.\n\n## Available weight sets\n\n{md_table(weights)}\n\n## Recommended use\n\nUse the default balanced weights for the first discussion. Then run sensitivity using alternative weights. Do not average stakeholder groups too early. Group differences are substantive evidence about values and risk tolerance.\n\n## Possible future methods\n\n- Swing weighting to elicit weights from trade-offs.\n- Best-worst method for simpler stakeholder input.\n- Analytic hierarchy process if pairwise comparison is desired.\n- Outranking methods if decision-makers want to identify dominated options rather than one winner.\n\nFor this project, the simple weighted-sum method is preferred initially because the underlying model is demonstrative and non-calibrated.\n''')

(MCDA_DIR/'mcda-results-interpretation-guide-v0.9.0.md').write_text(f'''# MCDA results interpretation guide v0.9.0\n\n## How to read the results\n\nA high score means the option performs well across the selected criteria and weights after risk adjustment. It does not mean the option is proven, affordable or ready to implement.\n\nA low score can mean one of three things:\n\n1. the option genuinely performs poorly;\n2. the option performs well on one criterion but poorly on others;\n3. the option has high implementation, equity or fiscal/gaming risk.\n\n## Default balanced result\n\n{md_table(rank_table)}\n\n## Weight-set sensitivity\n\n{md_table(weight_summary)}\n\n## Key interpretation\n\nThe full upstream access architecture remains the leading option across the example weight sets. However, the margin between capitation reweighting, access targets, a Primary Care Benefits Schedule, and ambulance alternatives varies by stakeholder weighting.\n\nThe loose benefits option demonstrates the warning case: expanding benefits without adequate controls improves access logic but performs poorly once equity, gaming, fiscal and governance risks are included.\n\n## When to revise the MCDA\n\nRevise the scorecard after OIA responses, stakeholder validation workshops, calibrated simulation outputs, fiscal modelling, equity and Te Tiriti review, and ambulance disposition and ED/hospital linkage analysis.\n''')

report=f'''# Game-informed MCDA decision-support report v0.9.0\n\n**Project:** Primary care funding architecture in Australia and New Zealand  \n**Focus:** New Zealand upstream access, primary care, ambulance and hospital-pressure games  \n**Version:** v0.9.0  \n**Status:** Demonstrative decision-support layer; not empirically calibrated\n\n## Executive summary\n\nThis report adds a game-informed MCDA layer to the final hybrid model. The purpose is to help decision-makers evaluate whether the mapped games matter, how strongly each game contributes to the policy problem, and which policy options are most likely to move the system toward better equilibria.\n\nThe MCDA does not replace empirical modelling. It makes judgement explicit. It is designed for RACMA discussion, stakeholder workshops, policy option screening and validation planning.\n\nThe central thesis remains:\n\n> New Zealand may be managing primary care and ambulance activity so tightly that unmet need is channelled into hospitals by default.\n\nThe MCDA translates that thesis into two decision-support tools:\n\n1. **Diagnostic game-position mapping**: where does each game currently sit, and how important is it?\n2. **Policy-option MCDA**: which reform option best balances access, equity, hospital deflection, fiscal control, governance, market entry and feasibility?\n\n![Default MCDA ranking](mcda-default-ranking-v0.9.0.png)\n\n## Why MCDA is useful here\n\nThis policy problem is not just a technical funding-design problem. It also involves values, risk tolerance, professional boundaries, equity, Te Tiriti legitimacy, rural resilience, fiscal exposure, data observability and political feasibility.\n\nA pure model can show what follows from assumptions. MCDA shows which assumptions and values decision-makers are using.\n\n## Diagnostic game map\n\nThe highest-priority diagnostic games in the example scoring are:\n\n{md_table(game_table.head(8))}\n\n![Diagnostic game priority](mcda-game-priority-v0.9.0.png)\n\nThe diagnostic map suggests that KPI salience, data observability, hospital salience, capitation marginal supply, ambulance conveyance and scope-of-practice supply are especially important games to test and discuss.\n\n## Policy-option MCDA\n\nThe default MCDA criteria are:\n\n{md_table(criteria_table)}\n\nThe default policy options are:\n\n{md_table(opts[['option_id','option','mapped_scenario']])}\n\n## Balanced-weight result\n\n{md_table(rank_table)}\n\nThe full upstream access architecture ranks first in the demonstrative MCDA. The Primary Care Benefits Schedule ranks second. Benefits plus scope-enabled eligibility ranks third but is more heavily penalised for implementation and governance risk. Capitation reweighting and capitation reweighting plus an access target perform moderately: they improve allocation and visibility, but do not fully solve marginal supply.\n\nLoose demand-driven benefits with weak controls rank last, despite scoring well on access. This is because the risk-adjustment layer penalises weak equity protections, weak data, weak governance, and high gaming/fiscal exposure.\n\n## Sensitivity across stakeholder weight sets\n\n{md_table(weight_summary)}\n\n![MCDA sensitivity across stakeholder weight sets](mcda-weight-sensitivity-v0.9.0.png)\n\nThe ranking is not intended to force consensus. It is intended to show where the result is robust and where it depends on stakeholder values.\n\n## Interpretation\n\nThe MCDA supports a refined version of the policy thesis:\n\n> A demand-driven Primary Care Benefits Schedule may improve marginal supply and hospital-deflection logic, but it becomes a viable policy architecture only when paired with scope governance, equity protections, co-payment calibration, ambulance alternatives, direct/optional claiming, data observability and top-tier KPIs.\n\nThis can be expressed as:\n\n> Demand-driven within rules; not demand-driven without rules.\n\n## How to use this package\n\nUse the MCDA in three ways:\n\n1. **Internal RACMA discussion**: test whether colleagues accept the game map and priority scores.\n2. **Stakeholder workshop**: compare group-specific scores and weight sets.\n3. **Empirical validation planning**: turn low-confidence, high-impact criteria into research tasks.\n\n## Audit status\n\nThis is a structured decision-support artefact. It is not proof of policy effectiveness. It should be updated after OIA responses, stakeholder validation, review findings, fiscal modelling and calibrated simulation.\n\n## Included artefacts\n\n- MCDA framework.\n- Game-position scoring rubric.\n- Policy-option scoring rubric.\n- Stakeholder workshop guide.\n- Weighting methods note.\n- Results interpretation guide.\n- Criteria, option, scorecard and weight-set CSVs.\n- Blank scoring templates.\n- Executable MCDA model.\n- Example figures and workbook.\n'''
for dest in [MCDA_DIR/'mcda-decision-support-report-v0.9.0.md', DOCS/'final/mcda-decision-support-report-v0.9.0.md', OUTPUTS/'mcda-decision-support-report-v0.9.0.md']:
    dest.write_text(report)

(DOCS/'policy-briefs/brief-08-game-informed-mcda-v0.9.0.md').write_text(f'''# Policy brief 08 - Game-informed MCDA decision support v0.9.0\n\n## Policy question\n\nHow can decision-makers compare primary care funding architecture options when the problem involves multiple games, uncertain evidence, equity trade-offs, fiscal risk and professional politics?\n\n## Proposal\n\nUse a game-informed MCDA alongside the hybrid model.\n\nThe game map identifies strategic traps. The MCDA asks which traps matter most and which reform options move the system toward better equilibria.\n\n## Why this matters\n\nA single model output can be dismissed as assumption-driven. MCDA makes those assumptions visible. It allows different stakeholders to weight criteria differently and test whether the preferred policy architecture remains plausible under those values.\n\n## Recommended MCDA criteria\n\n{md_table(criteria_table)}\n\n## Example result\n\n{md_table(rank_table.head(6))}\n\n## Policy interpretation\n\nThe full upstream access architecture performs best in the example MCDA. A Primary Care Benefits Schedule performs well, but needs additional governance and equity protections. Loose demand-driven benefits perform poorly after risk adjustment.\n\n## Recommended next step\n\nRun a structured stakeholder workshop using the v0.9.0 scoring templates, then use the results to revise the scorecard and validation backlog.\n''')
(DOCS/'substack/post-10-game-informed-mcda-v0.9.0.md').write_text('''# Substack post 10 - How should we decide which primary care funding game matters most?\n\nThe next step in this series is not another argument about whether capitation or fee-for-service is better.\n\nIt is a decision question.\n\nWhich strategic traps matter most? Which are we most confident about? Which are easiest to shift? Which are dangerous if we shift them badly?\n\nThat is where a game-informed MCDA is useful. MCDA means multi-criteria decision analysis. In plain English, it is a structured way of comparing options when there is no single metric that can carry the whole decision.\n\nIn primary care funding, there is no single metric. Access matters. Equity matters. Rural presence matters. Hospital avoidance matters. Fiscal control matters. Gaming risk matters. Clinical governance matters. Political feasibility matters. Data matters.\n\nThe game map tells us what the traps are. The MCDA asks which traps matter most.\n\nThe most important point is this: the preferred model is not simply demand-driven funding. A loose benefits schedule can increase access while creating gaming, safety, fiscal and equity risks.\n\nThe better line is:\n\n> Demand-driven within rules; not demand-driven without rules.\n\nThat means defined contact types, provider scope, clinical governance, co-payment protections, data visibility, audit, top-tier KPIs, and retained equity and locality functions.\n\nThe MCDA does not prove the answer. It shows the trade-offs. That is exactly what a serious policy debate should do.\n''')

# Track metadata
track=ROOT/'conductor/tracks/014-mcda-decision-support'
(track/'metadata.json').write_text(json.dumps({'track_id':'014-mcda-decision-support','version':'0.9.0','status':'complete at demonstrative decision-support stage','created':'2026-05-08','purpose':'Add a game-informed MCDA layer to help decision-makers score games, weight criteria, compare policy options and plan validation.'}, indent=2))
(track/'spec.md').write_text('''# Track 014 - Game-informed MCDA decision support v0.9.0\n\n## Objective\n\nCreate a deliberative decision-support layer that uses the mapped games to structure MCDA scoring, stakeholder weighting, policy option comparison and validation planning.\n\n## Scope\n\n- Diagnostic game-position scoring.\n- Policy-option MCDA scoring.\n- Weight-set sensitivity analysis.\n- Stakeholder workshop guide.\n- CSV templates and executable model.\n- MCDA report, brief and workbook.\n\n## Non-goals\n\n- Empirical calibration.\n- Formal policy endorsement.\n- Replacement of stakeholder deliberation or equity review.\n''')
(track/'plan.md').write_text('''# Plan - Track 014 v0.9.0\n\n1. Define MCDA criteria mapped to the 14 policy games.\n2. Define policy options and example scorecard.\n3. Add executable MCDA model and tests.\n4. Generate example outputs, figures and templates.\n5. Draft framework, rubrics, workshop guide and report.\n6. Produce workbook and standalone DOCX/PDF report.\n7. Update repo index, changelog, release notes and version.\n''')

(DOCS/'repo-index-v0.9.0.md').write_text('''# Repository index v0.9.0\n\n## New in v0.9.0\n\n- Game-informed MCDA decision-support layer.\n- Diagnostic game-position scoring.\n- Policy-option MCDA scoring.\n- Stakeholder weight-set sensitivity analysis.\n- Workshop templates and workbook.\n- MCDA report and policy brief.\n\n## Key new files\n\n```text\ndocs/mcda/mcda-framework-v0.9.0.md\ndocs/mcda/game-position-scoring-rubric-v0.9.0.md\ndocs/mcda/policy-option-mcda-rubric-v0.9.0.md\ndocs/mcda/stakeholder-workshop-guide-v0.9.0.md\ndocs/mcda/weighting-methods-note-v0.9.0.md\ndocs/mcda/mcda-results-interpretation-guide-v0.9.0.md\ndocs/mcda/mcda-decision-support-report-v0.9.0.md\nmodels/primarycare_model/mcda.py\nmodels/tests/test_mcda.py\noutputs/mcda-example-results-v0.9.0.csv\noutputs/mcda-weight-sensitivity-v0.9.0.csv\noutputs/mcda-game-position-example-v0.9.0.csv\noutputs/mcda-workbook-v0.9.0.xlsx\noutputs/mcda-decision-support-report-v0.9.0.docx\noutputs/mcda-decision-support-report-v0.9.0.pdf\n```\n\n## Status\n\nThe v0.9.0 MCDA layer is demonstrative and deliberative. It is designed for structured decision support and stakeholder testing, not empirical proof.\n''')
(ROOT/'RELEASE-NOTES-v0.9.0.md').write_text('''# Release notes v0.9.0 - Game-informed MCDA decision support\n\n## Summary\n\nv0.9.0 adds a decision-support layer to the primary care funding architecture project. The package now includes a game-informed MCDA that lets decision-makers score where each mapped game sits, weight decision criteria, compare policy options and examine sensitivity across stakeholder perspectives.\n\n## Added\n\n- MCDA code module and tests.\n- 10 decision criteria mapped to the 14 games.\n- 10 policy options.\n- 6 stakeholder weight sets.\n- Diagnostic game-position priority scoring.\n- Policy option scorecard and risk-adjusted MCDA results.\n- Sensitivity analysis across weight sets.\n- Workshop guide, rubrics and templates.\n- MCDA workbook, report and figures.\n\n## Caveat\n\nThe MCDA is demonstrative and non-calibrated. It should be used to structure deliberation and validation, not as a final policy ranking.\n''')
(ROOT/'VERSION.md').write_text('# Version\n\nCurrent release: v0.9.0\n\nStatus: game-informed MCDA decision-support layer added. Empirical calibration remains outstanding.\n')
for path, addition in [
    (ROOT/'CHANGELOG.md','''\n## v0.9.0 - Game-informed MCDA decision support\n\n- Added a game-informed MCDA layer with diagnostic game-position scoring, policy-option scoring, stakeholder weight sensitivity and risk-adjusted rankings.\n- Added MCDA report, brief, rubrics, workshop guide, templates and workbook.\n- Added executable `mcda.py` model and tests.\n- Status remains demonstrative/non-calibrated.\n'''),
    (ROOT/'conductor/tracks.md','''\n## 014 - Game-informed MCDA decision support\n\nStatus: implemented in v0.9.0.\n\nPurpose: help decision-makers score where each mapped game sits, weight decision criteria, compare policy options and identify validation priorities.\n'''),
    (ROOT/'README.md','''\n## v0.9.0 MCDA decision-support layer\n\nThe repository now includes a game-informed MCDA layer under `docs/mcda/` and `models/primarycare_model/mcda.py`. This layer converts the game map into diagnostic game-position scoring, policy-option MCDA scoring, stakeholder weight-set sensitivity and workshop templates. The MCDA is demonstrative and non-calibrated.\n''')]:
    text=path.read_text() if path.exists() else ''
    if 'v0.9.0' not in text and '014 - Game-informed MCDA' not in text:
        path.write_text(text.rstrip()+"\n"+addition)
    elif path.name in ['CHANGELOG.md','README.md'] and 'Game-informed MCDA decision support' not in text:
        path.write_text(text.rstrip()+"\n"+addition)

artefacts=[]
for rel in ['docs/mcda/mcda-framework-v0.9.0.md','docs/mcda/game-position-scoring-rubric-v0.9.0.md','docs/mcda/policy-option-mcda-rubric-v0.9.0.md','docs/mcda/stakeholder-workshop-guide-v0.9.0.md','docs/mcda/weighting-methods-note-v0.9.0.md','docs/mcda/mcda-results-interpretation-guide-v0.9.0.md','docs/mcda/mcda-decision-support-report-v0.9.0.md','docs/policy-briefs/brief-08-game-informed-mcda-v0.9.0.md','docs/substack/post-10-game-informed-mcda-v0.9.0.md','models/primarycare_model/mcda.py','models/tests/test_mcda.py','outputs/mcda-example-results-v0.9.0.csv','outputs/mcda-weight-sensitivity-v0.9.0.csv','outputs/mcda-game-position-example-v0.9.0.csv','outputs/mcda-policy-option-scorecard-v0.9.0.csv','outputs/mcda-criteria-v0.9.0.csv','outputs/mcda-policy-options-v0.9.0.csv','outputs/mcda-weight-sets-v0.9.0.csv','data/templates/policy-option-mcda-template-v0.9.0.csv','data/templates/game-position-scoring-template-v0.9.0.csv','outputs/mcda-default-ranking-v0.9.0.png','outputs/mcda-game-priority-v0.9.0.png','outputs/mcda-weight-sensitivity-v0.9.0.png','outputs/mcda-decision-support-report-v0.9.0.docx','outputs/mcda-decision-support-report-v0.9.0.pdf','outputs/mcda-workbook-v0.9.0.xlsx']:
    artefacts.append({'path':rel,'version':'0.9.0','type':Path(rel).suffix.lstrip('.') or 'directory','purpose':'MCDA decision-support layer'})
pd.DataFrame(artefacts).to_csv(DOCS/'final/artefact-pack-index-v0.9.0.csv', index=False)
pd.DataFrame(artefacts).to_csv(OUTPUTS/'artefact-pack-index-v0.9.0.csv', index=False)
print('v0.9.0 MCDA files generated')
print(run_mcda()[['rank','option_id','option','risk_adjusted_score']].to_string(index=False))
