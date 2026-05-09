"""Structured map of the New Zealand primary care policy game.

This is a classification scaffold, not a calibrated empirical model. It encodes
players, mechanisms, equilibrium risks and levers so they can be reused in
simulation model prototypes and tests.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class GameMapItem:
    """A component game in the broader NZ health-system policy game."""

    game_id: str
    name: str
    players: tuple[str, ...]
    game_type: str
    mechanism: str
    status_quo_equilibrium: str
    policy_lever: str
    testable_prediction: str


@dataclass(frozen=True)
class PayoffLever:
    """A variable that changes incentives inside the policy game."""

    symbol: str
    name: str
    interpretation: str
    expected_direction: str


def get_nz_game_map() -> tuple[GameMapItem, ...]:
    """Return the v0.4.0 New Zealand policy-game atlas."""

    return (
        GameMapItem(
            game_id="G1",
            name="Hospital-salience budget game",
            players=("Ministers", "Treasury", "Ministry of Health", "Health NZ", "Hospitals", "Public/media"),
            game_type="Repeated game with asymmetric observability",
            mechanism="Hospital pressure is visible and politically costly; upstream access failure is dispersed and delayed.",
            status_quo_equilibrium="Periodic hospital rescue with incremental upstream cost control.",
            policy_lever="Make primary care and ambulance access top-tier performance domains and allow eligible upstream activity to expand.",
            testable_prediction="Hospital rescue dominates while upstream unmet need remains weakly observed and weakly funded at the margin.",
        ),
        GameMapItem(
            game_id="G2",
            name="Health NZ internal allocation game",
            players=("Health NZ hospital operations", "Health NZ primary/community commissioning", "Commissioner/Board", "Minister"),
            game_type="Principal-agent and internal common-pool game",
            mechanism="An entity that operates hospitals and commissions upstream care faces direct operational hospital risk.",
            status_quo_equilibrium="Hospital delivery risk dominates management attention and baseline protection.",
            policy_lever="Create hospital-equivalent accountability for primary care and ambulance outcomes.",
            testable_prediction="If primary/ambulance target salience rises, allocation and management attention shift upstream.",
        ),
        GameMapItem(
            game_id="G3",
            name="Capitation marginal-supply game",
            players=("Practices", "Broader primary care teams", "Enrolled patients", "PHOs", "Health NZ"),
            game_type="Stackelberg supply response game",
            mechanism="Capitation supports continuity but weakens marginal public payment for additional contacts.",
            status_quo_equilibrium="Rationing through waits, fees, closed books, shorter visits or telehealth substitution.",
            policy_lever="Retain capitation but add contact-type benefits for eligible activity.",
            testable_prediction="Reweighting alone improves distribution but may not sufficiently increase total contact supply.",
        ),
        GameMapItem(
            game_id="G4",
            name="Consumer access pathway game",
            players=("Patients", "Whanau", "Practices", "Telehealth", "Ambulance", "ED"),
            game_type="Congestion and price-choice game",
            mechanism="Patients choose pathways based on co-payment, waiting time, travel, trust, urgency and digital access.",
            status_quo_equilibrium="When early access is costly or unavailable, some patients delay or use ED/ambulance.",
            policy_lever="Calibrate co-payments, concessions and safety nets while expanding eligible contact supply.",
            testable_prediction="High wait/fee/travel costs increase delay, ED substitution and ambulance use.",
        ),
        GameMapItem(
            game_id="G5",
            name="PHO intermediation game",
            players=("PHOs", "Health NZ", "Practices", "New entrants", "Communities"),
            game_type="Transaction-cost and principal-agent game",
            mechanism="Intermediation can add population-health value or create friction, opacity and entry barriers.",
            status_quo_equilibrium="Useful functions coexist with possible payment gatekeeping.",
            policy_lever="Separate PHO/locality functions from mandatory payment intermediation.",
            testable_prediction="Direct or optional claiming reduces entry costs only if population-health functions are preserved elsewhere.",
        ),
        GameMapItem(
            game_id="G6",
            name="ACC/Health NZ cross-funder game",
            players=("ACC", "Health NZ", "Treasury", "Practices", "Ambulance providers", "Patients"),
            game_type="Cross-funder externality / prisoner's dilemma",
            mechanism="ACC activity funding may support practice viability; siloed savings may shift costs to Health NZ or patients.",
            status_quo_equilibrium="Cross-funder effects are under-recognised without whole-of-Crown modelling.",
            policy_lever="Model ACC, ambulance, primary care and hospital flows together.",
            testable_prediction="Constraining ACC FFS in isolation may reduce practice viability and increase non-injury unmet need or hospital demand.",
        ),
        GameMapItem(
            game_id="G7",
            name="Ambulance conveyance game",
            players=("Ambulance providers", "Paramedics", "EDs", "Health NZ", "ACC", "Patients"),
            game_type="Safety-constrained incentive game",
            mechanism="Conveyance can be safer organisationally than alternatives if payment, liability and follow-up are misaligned.",
            status_quo_equilibrium="ED conveyance remains default when alternatives are not explicitly supported.",
            policy_lever="Fund and measure hear-and-treat, treat-and-refer and alternative destinations with safe follow-up.",
            testable_prediction="Alternative-disposition payments and governance reduce avoidable ED conveyance if safety is maintained.",
        ),
        GameMapItem(
            game_id="G8",
            name="Scope-of-practice supply game",
            players=("GPs", "Nurse practitioners", "Pharmacists", "Nurses", "Allied health", "Paramedics", "Regulators", "Funders"),
            game_type="Regulatory coordination / anticommons game",
            mechanism="Funding eligibility narrower than clinical scope creates artificial bottlenecks.",
            status_quo_equilibrium="Supply remains constrained around traditional provider categories.",
            policy_lever="Allow accredited providers to claim eligible contacts within legal scope and governance.",
            testable_prediction="Broader eligibility increases supply elasticity without quality loss if governed well.",
        ),
        GameMapItem(
            game_id="G9",
            name="Telehealth/local-supply game",
            players=("Telehealth providers", "Local practices", "Rural patients", "Health NZ"),
            game_type="Entry and cream-skimming game",
            mechanism="Scalable telehealth can absorb simple care while weakening local in-person viability if not integrated.",
            status_quo_equilibrium="Simple access improves but local examination/procedural capacity may deteriorate.",
            policy_lever="Fund telehealth as an extender and protect rural in-person access measures.",
            testable_prediction="Telehealth-only expansion improves simple contacts but may increase fragmentation and reduce local viability.",
        ),
        GameMapItem(
            game_id="G10",
            name="Co-payment calibration game",
            players=("Government", "Providers", "Patients"),
            game_type="Moral hazard / equity trade-off game",
            mechanism="Co-payments can signal demand but deter necessary care for high-need and low-income patients.",
            status_quo_equilibrium="Fees ration care, with equity risks, unless targeted protections exist.",
            policy_lever="Use transparent co-payments, concessions, safety nets and essential-service caps.",
            testable_prediction="Poorly calibrated co-payments increase delayed care and inequitable ED substitution.",
        ),
        GameMapItem(
            game_id="G11",
            name="KPI salience game",
            players=("Ministers", "Health NZ", "Ministry", "Providers", "Public"),
            game_type="Measurement and gaming game",
            mechanism="What is reported at top-tier level becomes organisationally salient; narrow targets can be gamed.",
            status_quo_equilibrium="Hospital targets dominate; upstream measures remain lower salience or incomplete.",
            policy_lever="Elevate primary care and ambulance KPIs with balancing measures.",
            testable_prediction="Top-tier reporting shifts behaviour only if paired with balancing measures and funding consequences.",
        ),
        GameMapItem(
            game_id="G12",
            name="Equity and trust game",
            players=("Maori communities", "Pacific communities", "Rural communities", "Kaupapa Maori providers", "Pacific providers", "Health NZ", "Ministry"),
            game_type="Assurance and co-production game",
            mechanism="Direct claiming can expand activity but does not replace population-health, trust, outreach or culturally specific care.",
            status_quo_equilibrium="Transactional payment and population-health commissioning each solve only part of the problem.",
            policy_lever="Blend contact benefits with explicit equity, outreach, kaupapa Maori, Pacific and locality functions.",
            testable_prediction="Direct benefits improve access only if equity functions remain funded and accountable.",
        ),
        GameMapItem(
            game_id="G13",
            name="Political economy game",
            players=("Political parties", "Sector bodies", "Colleges", "PHOs", "Unions", "Media", "Public"),
            game_type="Signalling and coalition game",
            mechanism="The same reform can be framed as pro-market, pro-patient, anti-PHO, anti-GP or anti-equity.",
            status_quo_equilibrium="Actors defend institutional positions; governments avoid easily caricatured reforms.",
            policy_lever="Use a non-partisan system-design narrative around access, supply and hospital avoidance.",
            testable_prediction="Coalition support increases when reform is framed as access architecture rather than sector income.",
        ),
        GameMapItem(
            game_id="G14",
            name="Data observability game",
            players=("Health NZ", "Ministry", "PHOs", "Practices", "Patients", "Researchers"),
            game_type="Information-asymmetry game",
            mechanism="Upstream unmet need remains less fundable if it is not visible and linked to downstream outcomes.",
            status_quo_equilibrium="Data gaps preserve hospital-dominant salience.",
            policy_lever="Link primary care access, ambulance disposition, ED demand and avoidable admissions by equity group.",
            testable_prediction="Better upstream observability changes performance narratives and can shift budget behaviour.",
        ),
    )


def get_payoff_levers() -> tuple[PayoffLever, ...]:
    """Return key variables that can be operationalised in simulation."""

    return (
        PayoffLever("p_h", "hospital political penalty", "Political cost per unit of hospital pressure", "Higher values favour hospital rescue"),
        PayoffLever("omega_p", "primary care target salience", "Relative weight of primary care targets in Health NZ utility", "Higher values favour upstream investment"),
        PayoffLever("omega_a", "ambulance target salience", "Relative weight of ambulance outcomes in Health NZ utility", "Higher values favour ambulance alternatives"),
        PayoffLever("M", "marginal contact benefit", "Public benefit paid for eligible primary care contact", "Higher values favour provider expansion if above marginal cost"),
        PayoffLever("c", "co-payment", "Patient out-of-pocket contribution", "Moderates demand but can worsen equity"),
        PayoffLever("lambda_pho", "PHO transaction cost", "Administrative/friction cost of intermediation", "Higher values favour direct/optional claiming"),
        PayoffLever("theta_scope", "scope flexibility", "Extent to which eligible contacts can be generated by broader providers", "Higher values increase supply elasticity"),
        PayoffLever("rho_acc", "ACC revenue dependence", "Contribution of ACC activity to practice viability", "Higher values increase spillover risk if ACC constrained"),
        PayoffLever("mu_ambulance", "ambulance alternative effectiveness", "Effect of hear/treat/refer on ED conveyance", "Higher values favour ambulance alternative investment"),
        PayoffLever("eta_data", "upstream data observability", "Visibility of primary care and ambulance access failure", "Higher values reduce hidden unmet need"),
    )


def find_games_by_player(player_fragment: str) -> tuple[GameMapItem, ...]:
    """Return games involving a player whose name contains the supplied fragment."""

    needle = player_fragment.lower()
    return tuple(
        game for game in get_nz_game_map()
        if any(needle in player.lower() for player in game.players)
    )


def game_ids() -> tuple[str, ...]:
    """Return all game identifiers."""

    return tuple(game.game_id for game in get_nz_game_map())
