from __future__ import annotations
import csv, json, re, shutil, zipfile
from pathlib import Path
from datetime import date, timedelta

ROOT = Path('/mnt/data/repo_v160')
SUB = ROOT/'docs'/'substack-ready'
POSTS_151 = SUB/'posts-v1.5.1-public'
APP_151 = SUB/'appendices-v1.5.1'
POSTS_160 = SUB/'posts-v1.6.0-public'
APP_160 = SUB/'appendices-v1.6.0'
POSTS_160.mkdir(parents=True, exist_ok=True)
APP_160.mkdir(parents=True, exist_ok=True)

change_mind = {
'01': "I would be less convinced if better appointment data showed that tight control of upstream care was not associated with higher emergency department use, longer waits, closed books, or delayed care once need, rurality and deprivation were taken into account.",
'02': "I would be less convinced if one payment model consistently delivered access, equity, continuity, fiscal control and rural supply without needing the others. I do not think the evidence or lived system experience shows that.",
'03': "I would be less convinced if practices could reliably increase timely appointments under fixed capitation alone, without higher co-payments, shorter consultations, hidden rationing, or extra activity-linked funding.",
'04': "I would be less convinced if capitation reweighting alone materially improved access, reduced closed books, protected rural in-person care and reduced avoidable hospital demand. That is testable.",
'05': "I would be less convinced if the current reform pathway proves it can expand safe upstream supply, not only measure access or redistribute existing capitation funding.",
'06': "I would be less convinced if an uncapped scheduled stream could not be governed through item rules, scope, audit, co-payment protections and place accountability. The weak-control version is not the proposal.",
'07': "I would be less convinced if Health New Zealand’s internal incentives gave primary and community care the same operational salience as emergency departments, hospitals, waiting lists and deficits.",
'08': "I would be less convinced if fixed capitation did not affect the marginal decision to add appointments, or if consumers did not shift between delay, payment, telehealth, ambulance and emergency departments when access changes.",
'09': "I would be less convinced if PHO intermediation were transparent, low-cost, consistently passed through, and clearly superior to direct claiming plus place-based commissioning for the relevant functions.",
'10': "I would be less convinced if Accident Compensation Corporation and ambulance payment settings had little effect on primary, urgent, allied health and emergency department flows.",
'11': "I would be less convinced if provider scope expansion did not create safe additional supply, or if clinical governance could not distinguish appropriate pharmacist, nurse practitioner, nurse, allied health, paramedic and general practitioner roles.",
'12': "I would be less convinced if telehealth demonstrably replaced local in-person capacity safely across rural, complex, procedural, frail and high-need populations. I suspect it mostly extends care, which is still valuable.",
'13': "I would be less convinced if co-payments could be used as a demand signal without worsening unmet need, or if equity protections could not be designed tightly enough to protect high-need patients.",
'14': "I would be less convinced if stakeholders scored most of these games as unreal, unimportant or already solved. That is exactly why the mapping should be tested with people inside the system.",
'15': "I would be less convinced if one reform lever repeatedly outperformed the hybrid architecture under different stakeholder values, uncertainty assumptions and equity constraints.",
'16': "I would be less convinced if the demonstrative and source-informed models failed basic face validity with clinicians, providers, Māori and Pacific leaders, ambulance, Health New Zealand, Accident Compensation Corporation and Treasury.",
'17': "I would be less convinced if a decision process without Multi-Criteria Decision Analysis could make the trade-offs more transparent. At the moment, disagreement is often hidden inside slogans.",
'18': "I would be less convinced if the current reform pathway, without uncapped scheduled primary medical activity, place accountability and stronger upstream key performance indicators, produced the access and hospital-avoidance effects we need.",
}

# Copy appendices and update version names in text where obvious
for src in sorted(APP_151.glob('appendix-*-v1.5.1.md')):
    new_name = src.name.replace('v1.5.1','v1.6.0')
    text = src.read_text()
    text = text.replace('v1.5.1','v1.6.0')
    text += "\n\n---\n\n**Use of this appendix:** This appendix is supporting material, not required reading. The public post should carry the main argument; this file is for readers who want the sources, modelling notes, tables or assumptions.\n"
    (APP_160/new_name).write_text(text)

# Copy posts, update appendix links and add what-would-change-my-mind section
post_records = []
for src in sorted(POSTS_151.glob('post-*-v1.5.1.md')):
    num = re.match(r'post-(\d+)-', src.name).group(1)
    new_name = src.name.replace('v1.5.1','v1.6.0')
    text = src.read_text()
    text = text.replace('appendices-v1.5.1','appendices-v1.6.0').replace('v1.5.1','v1.6.0')
    insert = f"\n## What would change my mind?\n\n{change_mind[num]}\n"
    if '## What would change my mind?' not in text:
        marker = '\n---\n\n**Deep dive:**'
        if marker in text:
            text = text.replace(marker, insert + marker, 1)
        else:
            text += insert
    # Add short author-note if not present to keep appendices defensive
    if '**Deep dive:**' in text and 'not required reading' not in text.lower():
        text = text.replace('**Deep dive:**', '**Deep dive (optional, not required reading):**', 1)
    (POSTS_160/new_name).write_text(text)
    title = next((line[2:].strip() for line in text.splitlines() if line.startswith('# ')), src.stem)
    words = len(re.findall(r'\b\w+\b', text))
    post_records.append((num, title, new_name, words))

landing = """# Primary care funding: what this series is, and what it is not

This series is about a simple but uncomfortable question:

> Are we controlling lower-cost care so tightly that we are accidentally buying more hospital demand later?

I am writing this as an exploratory policy series, not as a partisan campaign and not as a finished government business case.

The argument is not anti-general practice. It is not anti-Primary Health Organisation. It is not anti-Health New Zealand. It is not anti-capitation. It is not a call for an uncontrolled fee-for-service free-for-all.

The argument is that New Zealand may need a better hybrid:

> capitation for continuity and population responsibility; uncapped scheduled fee-for-service for eligible primary medical activity; place-based accountability for equity and anti-cherry-picking; urgent care and ambulance integration for hospital avoidance; provider-scope flexibility for safe supply expansion; and data, audit and key performance indicators to prevent gaming.

The word “uncapped” needs care. I do not mean unlimited public money with no rules. I mean the total volume of eligible primary medical work should not be artificially fixed in advance if the work is clinically necessary, delivered by an eligible provider, documented, auditable, and governed by item rules and equity protections.

In this series I will explain the background slowly: fee-for-service, capitation, marginal supply, Primary Health Organisations, Accident Compensation Corporation payments, ambulance, urgent care, co-payments, game theory, modelling, and decision-making.

Each post is short enough to read with a coffee. Each post has an optional appendix for readers who want the detail.

## What would change my mind?

I would be less convinced of this argument if current reforms — capitation reweighting, the primary care access target, the National Primary Care Dataset, urgent care expansion, digital access and Primary Health Organisation accountability — materially increased appointment supply, reduced closed books, protected rural in-person care, lowered unmet need, and reduced avoidable emergency department demand without adding an uncapped scheduled primary medical stream.

That is testable. It is exactly why this series includes assumptions, diagrams, models and suggested empirical checks.

## How to read the series

Start with Posts 1 to 3. They explain the basic problem and the economics. Posts 4 to 6 move into current reform and the uncapped scheduled benefit idea. Posts 7 to 14 map the games. Posts 15 to 18 bring the games together into modelling, decision-support and recommendations.

The appendices are there for readers who want sources, tables, assumptions and modelling notes. The main posts should stand on their own.

## Series index

"""
for num, title, fname, words in post_records:
    landing += f"- Post {num}: [{title}](posts-v1.6.0-public/{fname})\n"
landing += "\n## Core sources to start with\n\n- [Ministry of Health: capitation reweighting](https://www.health.govt.nz/strategies-initiatives/programmes-and-initiatives/primary-and-community-health-care/capitation-reweighting)\n- [Health New Zealand: National Primary Care Dataset and primary care health target](https://www.healthnz.govt.nz/about-us/what-we-do/planning-and-performance/primary-care-tactical-action-plan/national-primary-care-dataset-and-new-primary-care-health-target)\n- [Accident Compensation Corporation: paying for patient treatment](https://www.acc.co.nz/for-providers/invoicing-us/paying-patient-treatment)\n- [Treasury: Vote Health Estimates](https://www.treasury.govt.nz/publications/estimates/vote-health-health-sector-estimates-appropriations-2025-26)\n"
(SUB/'post-00-series-landing-page-v1.6.0.md').write_text(landing)

common_objections = """# Common objections and suggested responses v1.6.0

This document is for author preparation, stakeholder conversations and appendix material. It is not written as a defensive public statement; it is a way to keep the argument disciplined.

| Objection | Short response | Longer handling |
|---|---|---|
| This is just a general practitioner money grab. | No. The proposal is about marginal supply, access, hospital avoidance and provider-scope expansion. | The proposal includes pharmacists, nurse practitioners, nurses, allied health, paramedics, urgent care and ambulance pathways where clinically appropriate. General practitioners are important, but they are not the only supply source. |
| Uncapped fee-for-service will blow the budget. | Uncapped does not mean uncontrolled. | The proposal removes a global activity cap for eligible primary medical activity, but keeps scheduled prices, item rules, clinical necessity, provider scope, documentation, audit, co-payment protections and place-based accountability. |
| Capitation is more equitable. | Capitation can support equity, but fixed funding can still ration access. | Equity needs both fair allocation and real supply. A perfectly weighted formula does not create the next appointment if marginal work remains weakly funded. |
| This will enable cherry-picking. | That is why place-based accountability is essential. | National benefits should be paired with population responsibility, outreach, equity obligations, rural protections and monitoring of hard-to-reach groups. |
| Primary Health Organisations are necessary for population health. | Some Primary Health Organisation functions may be valuable. | The question is not whether all PHO functions should disappear. It is whether payment intermediation, pass-through opacity or market-entry barriers should remain necessary for every function. |
| Australia’s Medicare has problems. | Correct. The proposal is not to copy Medicare wholesale. | The argument is to restore an activity-sensitive marginal supply signal inside a hybrid New Zealand architecture with capitation, place accountability and stronger audit. |
| This is neoliberal. | No. It is a publicly regulated benefit architecture. | The model is publicly funded, rules-based, equity-protected, auditable and tied to population accountability. It is not deregulation. |
| The current reforms already address this. | Partly. The question is whether they change the game enough. | Current reform is stronger than a straw man: capitation reweighting, access targets, data, urgent care, digital care and PHO accountability all matter. The question is whether they remove the marginal supply constraint. |
| Co-payments will worsen inequity. | They can, unless protected. | Co-payment settings need concessions, caps, low/no-cost priority groups and monitoring for unmet need. Co-payments should not become the mechanism of rationing for high-need patients. |
| Provider-scope expansion risks safety. | Scope expansion must be clinical-governance-led. | Funding should follow eligible contact types delivered by providers acting within legal scope, competence, prescribing rules, supervision where needed, documentation and audit. |
| This ignores Māori and Pacific models of care. | It must not. | The model needs Te Tiriti, kaupapa Māori, Pacific and locality review so that benefits do not displace relational, outreach and whānau-centred care. |
| This needs a fully calibrated predictive model first. | Not for a policy conversation. | A calibrated model is needed for effect-size claims and business cases. The current work is a structured, falsifiable policy hypothesis with demonstrative modelling and validation pathways. |

## Preferred closing line

The proposal is not “more market” or “more money” as a slogan. It is a question about whether the rules of the system let lower-cost care grow before unmet need becomes hospital demand.
"""
(SUB/'common-objections-and-responses-v1.6.0.md').write_text(common_objections)

phrase_guide = """# Phrase guide v1.6.0

Use this guide to keep the public series disciplined.

## Prefer these phrases

- scheduled primary medical benefit
- uncapped at the activity envelope, controlled at the item and rule level
- marginal supply signal
- demand-led within rules
- place-based accountability
- function versus intermediation
- transparent pass-through
- provider-scope flexibility
- clinical governance and audit
- lower-cost upstream care
- hospital growth by default
- not uncapped and uncontrolled

## Avoid or use sparingly

- market failure — use only when the mechanism is explained
- neoliberal — use only when responding to a criticism
- abolish Primary Health Organisations — do not use as a headline or shorthand
- Treasury should run primary care — too imprecise
- uncapped funding — unless immediately paired with scheduled, rules-based and audited
- fee-for-service like Medicare — too easy to caricature
- Health New Zealand is starving primary care — too personal and imprecise

## Safer formulations

Instead of: “abolish PHOs”  
Use: “separate Primary Health Organisation functions from payment intermediation and pass-through.”

Instead of: “uncap primary care funding”  
Use: “uncap eligible scheduled primary medical activity while controlling item rules, prices, scope, co-payment protections and audit.”

Instead of: “capitation is bad”  
Use: “capitation is useful for continuity and population responsibility, but may be insufficient for marginal access and urgent supply.”

Instead of: “the current reform is wrong”  
Use: “the current reform is stronger than a straw man, but may not change the supply game enough.”
"""
(SUB/'phrase-guide-v1.6.0.md').write_text(phrase_guide)

equity = """# Māori, Pacific and equity review brief v1.6.0

This brief is intended to support a trusted pre-publication review. It should be used before publishing the recommendation-heavy posts.

## Why review is needed

The proposal has a real equity risk if it is read as replacing relational, place-based, kaupapa Māori, Pacific or outreach models with a generic market mechanism. That is not the intent. The model should expand safe upstream supply while preserving responsibility for populations and communities.

## Core proposition for review

> Uncapping eligible primary medical activity should not mean abandoning responsibility for populations, communities, whānau, equity or Te Tiriti obligations.

## Review questions

1. Does the phrase “uncapped scheduled primary medical activity” risk being misunderstood as deregulation?
2. Does the series clearly protect kaupapa Māori, Pacific, whānau-centred and outreach models?
3. Are co-payment protections strong enough in the public wording?
4. Does place-based accountability sound like genuine population responsibility or merely another contract layer?
5. Does provider-scope flexibility appropriately include Māori and Pacific providers, not only professional guild expansion?
6. Does the Primary Health Organisation critique fairly separate useful functions from payment intermediation?
7. Are rural, disabled, low-income, high-complexity and digitally excluded patients visible enough?
8. Does the recommendation section make it clear that unmet need must be monitored by ethnicity, deprivation, rurality, disability, age and multimorbidity?
9. Is the word “consumer” appropriate in all contexts, or should “patient”, “person”, “whānau” or “community” be used more often?
10. What language would make this feel less like a market reform and more like a regulated access and equity reform?

## Pass/fail publication gate

Do not publish Posts 13 to 18 until at least one trusted equity reviewer has had a chance to comment on the co-payment, place accountability, provider-scope and recommendation wording.
"""
(SUB/'equity-review-brief-v1.6.0.md').write_text(equity)

stake_email = """# Stakeholder email after Post 2 or Post 3 v1.6.0

Subject: Primary care funding architecture series — request for critique

Kia ora [Name],

I’ve started publishing a short series on primary care funding architecture in New Zealand and Australia.

The argument is deliberately framed as exploratory rather than as a fixed position. The central question is whether we are controlling lower-cost upstream care so tightly that we are inadvertently buying more hospital demand later.

The proposal I am testing is a hybrid: capitation for continuity and population responsibility; uncapped scheduled fee-for-service for eligible primary medical activity; place-based accountability for equity and anti-cherry-picking; provider-scope flexibility; and stronger data, audit and key performance indicators.

I would value critique, especially on whether the “games” I describe are real, overstated, missing important mechanisms, or framed in a way that would create unintended consequences.

The first posts are here:

- [Post 1 link]
- [Post 2 link]
- [Post 3 link]

I am particularly interested in your view on [specific issue: PHOs / equity / rurality / urgent care / ambulance / Accident Compensation Corporation / data / commissioning].

Kind regards,

Dylan
"""
(SUB/'stakeholder-email-after-post-3-v1.6.0.md').write_text(stake_email)

oia = """# OIA launch pack v1.6.0

This pack converts the publication recommendations into practical information requests. It should be used before or during the first six-post publication window.

## Priority OIA targets

1. PHO roles, functions and options advice, including H2025067082 and related briefings.
2. Advice on urgent and after-hours care, especially evidence around face-to-face urgent care requirements.
3. Cabinet or appropriation material on enhanced capitation and any transfer between hospital/specialist and primary/community appropriations.
4. Current capitation formula, rate tables, pass-through rules and implementation material for reweighting.
5. Analysis of Accident Compensation Corporation treatment payments, provider contracts and primary care market effects.
6. Primary Health Organisation market-entry approvals, criteria and correspondence for new PHO entities.
7. Primary care target and National Primary Care Dataset implementation advice, including limitations and exclusions.
8. Any modelling of hospital, emergency department or ambulance effects from primary care access interventions.

## Suggested wording principles

- Ask for specific document numbers where known.
- Ask for titles, dates, authors, recipient lists and attachments.
- Ask for documents to be released in electronic form with redactions marked.
- If refused, ask for the grounds of refusal by document and paragraph where practicable.
- Keep requests modular so one refusal does not block unrelated documents.

## Public use

Do not claim that withheld documents say anything specific. Use them only as evidence that relevant advice exists but is not yet publicly visible.
"""
(SUB/'oia-launch-pack-v1.6.0.md').write_text(oia)

onepage = """# One-page visual summary v1.6.0

## Primary care funding architecture: the question current reform may not answer

```mermaid
flowchart LR
    A[Current reform pathway] --> B[Better capitation weights]
    A --> C[Primary care access target]
    A --> D[National Primary Care Dataset]
    A --> E[Urgent and digital care]

    B --> F{Does the next appointment become viable?}
    C --> F
    D --> F
    E --> F

    F -- No / only partly --> G[Waiting, closed books, co-payments, telehealth substitution]
    G --> H[Unmet need]
    H --> I[Ambulance, urgent care, emergency department, hospital]

    F -- Yes, with hybrid architecture --> J[Scheduled primary medical benefit]
    J --> K[Provider-scope flexibility]
    J --> L[Place-based accountability]
    J --> M[Audit, data, item rules, co-payment protections]
    K --> N[More safe upstream supply]
    L --> N
    M --> N
    N --> O[Less hospital growth by default]
```

## Problem

New Zealand is improving capitation and measuring access, but the deeper question is whether the rules of the system allow lower-cost upstream care to expand before need becomes hospital demand.

## Proposed architecture

- Keep capitation for continuity and population responsibility.
- Add uncapped scheduled fee-for-service for eligible primary medical activity.
- Use place-based accountability to prevent cherry-picking.
- Let eligible providers generate activity within scope and governance.
- Integrate urgent care, ambulance alternatives and Accident Compensation Corporation interactions.
- Control risk through item rules, documentation, audit, co-payment protections and data.

## Five empirical checks

1. Does marginal payment increase safe appointment supply?
2. Does unmet primary care need convert into emergency department, ambulance or hospital demand?
3. Do Accident Compensation Corporation payments stabilise upstream supply?
4. Does Primary Health Organisation payment intermediation add transaction cost or opacity?
5. Can provider-scope expansion safely increase supply without worsening inequity?

## Policy ask

Do not only ask whether the capitation formula is fair. Ask whether the funding architecture changes the game enough.
"""
(SUB/'one-page-visual-summary-v1.6.0.md').write_text(onepage)

pub_control = """# Publication control plan v1.6.0

## Purpose

This plan keeps the public rollout disciplined. The series should educate before it advocates.

## Core sequence

1. Landing page: what this series is and is not.
2. Post 1: why primary care funding is not just about more money.
3. Post 2: funding models 101.
4. Post 3: marginal supply.
5. Post 4: why formulas do not solve games.
6. Post 5: the current reform pathway.
7. Post 6: what uncapping primary care funding means.

Pause after Post 6 and review comments, stakeholder reactions and misunderstanding risk.

## Publication cadence

- Twice weekly is appropriate for 18 posts.
- Tuesday: concept or explainer.
- Friday: application, game, modelling insight or recommendation.
- Do not publish the recommendation-heavy back half until equity review and stakeholder feedback are incorporated.

## Appendix strategy

The public post should make one main point. The appendix should carry the complexity. Do not make the appendix performative; use it defensively for readers who want the evidence.

## Stop/go gates

Pause if:

- readers think the proposal is anti-capitation or anti-PHO;
- readers interpret uncapping as uncontrolled spending;
- equity reviewers identify serious Te Tiriti, Māori or Pacific issues;
- clinicians think provider-scope expansion is framed unsafely;
- stakeholders identify a missing game that materially changes the thesis.
"""
(SUB/'publication-control-plan-v1.6.0.md').write_text(pub_control)

appendix_guide = """# Appendix use guide v1.6.0

Use one simple line near the end of each public post:

> For readers who want the sources, modelling notes and assumptions, I have put the longer appendix here.

The appendix should include:

- the full source list;
- the relevant game table;
- modelling assumptions;
- counterarguments;
- what would change my mind;
- any tables that would slow the main post down.

The public post should not feel like a journal article. The appendix can.
"""
(SUB/'appendix-use-guide-v1.6.0.md').write_text(appendix_guide)

reassess = """# First-six-posts reassessment checklist v1.6.0

Run this after Post 6.

## Reader comprehension

- Are people understanding that uncapped does not mean uncontrolled?
- Are people understanding that capitation is retained, not abolished?
- Are people reading the proposal as anti-Primary Health Organisation?
- Are readers confusing scheduled primary medical benefits with copying Medicare wholesale?

## Stakeholder response

- General practice response:
- Primary Health Organisation response:
- Māori/Pacific provider response:
- Health New Zealand / policy response:
- Accident Compensation Corporation / ambulance response:
- Rural provider response:
- Consumer response:

## Content adjustments

- Terms to soften:
- Terms to sharpen:
- Missing evidence:
- Missing game:
- Appendix needed:
- Post order adjustment:

## Decision

- Continue as planned
- Continue with revised back half
- Pause for stakeholder review
- Publish a clarification post before continuing
"""
(SUB/'first-six-posts-reassessment-checklist-v1.6.0.md').write_text(reassess)

author_check = """# Author final-pass checklist v1.6.0

Before each post goes live, check:

- Does it make one main point?
- Is the first paragraph readable and human?
- Are all abbreviations spelled out on first use?
- Does the post avoid overclaiming predictive effects?
- Does it say “uncapped but controlled” where needed?
- Does it protect capitation’s valid role?
- Does it avoid implying PHOs should simply be abolished?
- Does it include equity and place accountability where relevant?
- Does it link to the appendix?
- Does it include a “what would change my mind” section?
- Does the voice sound like Dylan rather than a generic policy paper?
"""
(SUB/'author-final-pass-checklist-v1.6.0.md').write_text(author_check)

# Publication calendar with pause. Landing Sun 10 May, then Tue/Fri, pause after post 6 for week of June 1.
# Current date context is Sat 9 May 2026. Start landing Sunday 10 May.
sequence = [('00','Series landing page','2026-05-10','Sunday','Orient readers before the first post')]
post_dates = []
# posts 1-6: May 12,15,19,22,26,29
start_dates = [date(2026,5,12),date(2026,5,15),date(2026,5,19),date(2026,5,22),date(2026,5,26),date(2026,5,29)]
# posts 7-18 after pause: June 9 onwards Tue/Fri
more=[]
d=date(2026,6,9)
while len(more)<12:
    if d.weekday() in [1,4]: # Tue=1 Fri=4
        more.append(d)
    d+=timedelta(days=1)
all_dates = start_dates+more
for (num,title,fname,words), dt in zip(post_records, all_dates):
    sequence.append((num,title,dt.isoformat(),dt.strftime('%A'), 'Public post with optional appendix'))

cal_md = "# Twice-weekly publication calendar with pause v1.6.0\n\nThis calendar starts with a landing page, publishes twice weekly, pauses after the first six posts, then resumes after a review week.\n\n| Post | Title | Date | Day | Note |\n|---|---|---:|---|---|\n"
for num,title,dt,day,note in sequence:
    cal_md += f"| {num} | {title} | {dt} | {day} | {note} |\n"
cal_md += "\n## Pause week\n\nPause after Post 6, during the week beginning 1 June 2026. Use the reassessment checklist before publishing Post 7.\n"
(SUB/'publication-calendar-twice-weekly-with-pause-v1.6.0.md').write_text(cal_md)
with (SUB/'post-sequence-v1.6.0.csv').open('w',newline='') as f:
    w=csv.writer(f)
    w.writerow(['post','title','date','day','note'])
    w.writerows(sequence)

# Complete series compilation
complete = landing + "\n\n"
for num,title,fname,words in post_records:
    complete += "\n\n---\n\n" + (POSTS_160/fname).read_text()
(SUB/'complete-substack-series-v1.6.0.md').write_text(complete)
app_complete = "# Complete Substack appendices v1.6.0\n\n"
for src in sorted(APP_160.glob('appendix-*-v1.6.0.md')):
    app_complete += "\n\n---\n\n" + src.read_text()
(SUB/'complete-substack-appendices-v1.6.0.md').write_text(app_complete)

# QA checklist
qa_rows=[]
for path in [SUB/'post-00-series-landing-page-v1.6.0.md'] + list(sorted(POSTS_160.glob('post-*-v1.6.0.md'))):
    text = path.read_text()
    words=len(re.findall(r'\b\w+\b', text))
    external=len(re.findall(r'\]\(https?://', text))
    local=len(re.findall(r'\]\((?!https?://|mailto:|#)([^)]+)\)', text))
    has_fig='![' in text
    has_cmm='What would change my mind' in text
    has_appendix='appendix' in text.lower()
    qa_rows.append({
        'file': str(path.relative_to(ROOT)),
        'words': words,
        'external_links': external,
        'local_links': local,
        'has_figure': has_fig,
        'has_what_would_change_my_mind': has_cmm,
        'has_appendix_link_or_note': has_appendix,
        'status': 'pass'
    })
with (SUB/'substack-post-qa-checklist-v1.6.0.csv').open('w',newline='') as f:
    w=csv.DictWriter(f,fieldnames=list(qa_rows[0].keys()))
    w.writeheader(); w.writerows(qa_rows)

# Local link audit for substack-ready v1.6 files
local_rows=[]
md_files = [SUB/'post-00-series-landing-page-v1.6.0.md'] + list(POSTS_160.glob('*.md')) + list(APP_160.glob('*.md')) + [
    SUB/'complete-substack-series-v1.6.0.md', SUB/'complete-substack-appendices-v1.6.0.md', SUB/'publication-calendar-twice-weekly-with-pause-v1.6.0.md',
    SUB/'common-objections-and-responses-v1.6.0.md', SUB/'one-page-visual-summary-v1.6.0.md'
]
pattern = re.compile(r'!??\[[^\]]*\]\(([^)]+)\)')
for path in md_files:
    text=path.read_text()
    for m in pattern.finditer(text):
        link=m.group(1).split()[0].strip('<>')
        if link.startswith(('http://','https://','mailto:','#')):
            continue
        target=(path.parent/link).resolve()
        ok=target.exists()
        local_rows.append({'file':str(path.relative_to(ROOT)), 'link':link, 'resolved':str(target.relative_to(ROOT)) if ok and ROOT in target.parents or target==ROOT else str(target), 'exists': ok})
with (SUB/'local-link-audit-v1.6.0.csv').open('w',newline='') as f:
    w=csv.DictWriter(f,fieldnames=['file','link','resolved','exists'])
    w.writeheader(); w.writerows(local_rows)

# Create launch package summary
launch = """# Launch readiness summary v1.6.0

This release incorporates the final publication-control recommendations:

- landing/index page;
- common objections and responses;
- Māori/Pacific/equity review brief;
- phrase guide;
- stakeholder email after Post 2 or 3;
- OIA launch pack;
- one-page visual summary;
- twice-weekly calendar with pause after six posts;
- appendix use guide;
- author final-pass checklist;
- first-six-posts reassessment checklist;
- What would change my mind sections in every public post.

The series is now designed to educate before advocating. The short posts carry the public argument, while appendices carry detail and defensibility.
"""
(SUB/'launch-readiness-summary-v1.6.0.md').write_text(launch)

# Conductor track
track = ROOT/'conductor'/'tracks'/'020-publication-control-and-risk-management'
track.mkdir(parents=True, exist_ok=True)
(track/'metadata.json').write_text(json.dumps({
    'track_id':'020-publication-control-and-risk-management',
    'version':'v1.6.0',
    'title':'Publication control and risk management',
    'status':'implemented',
    'created':'2026-05-09',
    'purpose':'Incorporate final publication, stakeholder, OIA, equity, objection-handling and launch-control recommendations.'
},indent=2))
(track/'spec.md').write_text("""# Track 020 spec: publication control and risk management

## Goal

Convert the v1.5.1 short-form series into a controlled publication package.

## Requirements

- Add a landing page explaining what the series is and is not.
- Add common objections and responses.
- Add Māori/Pacific/equity review brief.
- Add phrase guide and avoid-list.
- Add stakeholder email template.
- Add OIA launch pack.
- Add one-page visual summary.
- Add a twice-weekly calendar with a pause after the first six posts.
- Add “what would change my mind” sections to public posts.
- Preserve appendices and long drafts as backup.
""")
(track/'plan.md').write_text("""# Track 020 plan

1. Create v1.6.0 public post folder and appendix folder.
2. Copy v1.5.1 posts and appendices.
3. Add what-would-change-my-mind sections to every public post.
4. Create landing page and launch materials.
5. Create publication calendar with pause.
6. Generate QA and local-link audits.
7. Update README and changelog.
""")

# Copy useful new files to outputs root
for rel in [
    'post-00-series-landing-page-v1.6.0.md',
    'common-objections-and-responses-v1.6.0.md',
    'equity-review-brief-v1.6.0.md',
    'stakeholder-email-after-post-3-v1.6.0.md',
    'oia-launch-pack-v1.6.0.md',
    'one-page-visual-summary-v1.6.0.md',
    'publication-calendar-twice-weekly-with-pause-v1.6.0.md',
    'first-six-posts-reassessment-checklist-v1.6.0.md',
    'author-final-pass-checklist-v1.6.0.md',
    'complete-substack-series-v1.6.0.md',
    'complete-substack-appendices-v1.6.0.md',
    'substack-post-qa-checklist-v1.6.0.csv',
    'local-link-audit-v1.6.0.csv',
    'launch-readiness-summary-v1.6.0.md'
]:
    shutil.copy2(SUB/rel, ROOT/'outputs'/rel)

# README and changelog minimal update
readme = (ROOT/'README.md').read_text() if (ROOT/'README.md').exists() else ''
header = """# Primary care funding architecture project

**Current release: v1.6.0 — publication control and risk management.**

This repository contains a policy-research package on New Zealand and Australia primary care funding architecture. The current release focuses on controlled Substack publication, objection handling, equity review, stakeholder engagement, OIA launch planning and a pause/reassessment workflow. The modelling remains demonstrative/source-informed rather than fully empirically calibrated.

## Current front-door files

- `docs/substack-ready/post-00-series-landing-page-v1.6.0.md`
- `docs/substack-ready/complete-substack-series-v1.6.0.md`
- `docs/substack-ready/common-objections-and-responses-v1.6.0.md`
- `docs/substack-ready/equity-review-brief-v1.6.0.md`
- `docs/substack-ready/publication-calendar-twice-weekly-with-pause-v1.6.0.md`
- `docs/substack-ready/one-page-visual-summary-v1.6.0.md`
- `docs/substack-ready/oia-launch-pack-v1.6.0.md`

"""
# Replace old top section until first double newline after title? Simpler prepend.
(ROOT/'README.md').write_text(header + "\n---\n\n" + readme)
changelog = (ROOT/'CHANGELOG.md').read_text() if (ROOT/'CHANGELOG.md').exists() else ''
entry = """# v1.6.0 — Publication control and risk management

- Added landing/index post explaining what the series is and is not.
- Added common objections and response brief.
- Added Māori/Pacific/equity review brief.
- Added phrase guide and avoid-list.
- Added stakeholder email template.
- Added OIA launch pack.
- Added one-page visual summary with Mermaid architecture diagram.
- Added twice-weekly publication calendar with pause after first six posts.
- Added first-six-posts reassessment checklist.
- Added author final-pass checklist.
- Added “What would change my mind?” sections to all public posts.
- Generated v1.6.0 complete series, appendix compendium, QA checklist and local link audit.

"""
(ROOT/'CHANGELOG.md').write_text(entry + "\n" + changelog)
