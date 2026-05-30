from __future__ import annotations
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Mapping
import pandas as pd
import matplotlib.pyplot as plt

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


if __name__ == '__main__':
    print(run_mcda().to_string(index=False))
