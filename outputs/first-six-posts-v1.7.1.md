# Are we buying hospital growth by rationing cheaper care upstream?

**Source-confidence label:** public-document supported policy hypothesis, economic theory and model assumption; not calibrated prediction.

There is a simple question underneath a lot of New Zealand health policy.

Are we managing primary care, urgent care and ambulance services so tightly that we are accidentally buying more hospital demand?

That sounds provocative. I do not mean it as a slogan. I mean it as a system-design question.

Primary care is usually the cheaper, earlier and more human part of the system. It is where a person asks about a cough before it becomes pneumonia. It is where a child’s fever is assessed before a parent panics and goes to the emergency department. It is where blood pressure, diabetes, pain, frailty, prescriptions, forms, mental health and uncertainty are dealt with before they become bigger problems.

![Figure for Are we buying hospital growth by rationing cheaper care upstream?](../figures/fig-01-whole-system-flow-v1.2.0.png)

*Figure: conceptual explainer for this post. It is not an observed outcome chart or calibrated prediction.*

But primary care does not expand by magic. Someone has to pay for the next appointment. Someone has to fund the room, the nurse, the doctor, the pharmacist, the nurse practitioner, the receptionist, the software, the phone calls, the follow-up and the risk.

That is why funding architecture matters.

When people hear “primary care funding”, they often think the debate is just about whether general practitioners should be paid more. That is too narrow. Of course money matters. But the deeper issue is how the money moves.

A funding model is not just accounting. It is a set of rules. It tells providers what work is viable, what work is risky, what work is invisible, and what work is someone else’s problem.

In New Zealand, the core funding model for general practice is capitation. Capitation means a clinic receives a fixed amount per enrolled person each year. The Ministry of Health says capitation was introduced in 2002 and remains the core way general practice is funded. The formula is now being reweighted because the old formula no longer reflects today’s population, complexity, rurality and deprivation.

That reweighting is sensible. But it may not be enough.

Here is the problem. Capitation is good at giving a practice responsibility for a population. It is useful for continuity and planned care. But once a patient is enrolled, the next appointment often creates extra cost without an equivalent extra payment.

That is what economists call a marginal problem. Marginal just means “the next one”. The next consultation. The next phone call. The next urgent appointment. The next wound dressing. The next follow-up. The next rural session. The next child with a fever.

If the next piece of work is weakly funded, the system will eventually ration it. Rationing may not look like a sign on the door. It may look like a three-week wait, closed books, higher co-payments, shorter appointments, fewer rural clinics, or patients being told to try online care or go to the emergency department.

The need does not disappear. It moves.

Some of it moves to urgent care. Some moves to ambulance. Some moves to hospital. Some becomes silent unmet need. Some becomes worse illness later.

This is where the hospital always has an advantage. Hospital pressure is visible. Ambulances ramping outside an emergency department are visible. Waiting lists are visible. Media stories about delayed cancer treatment are visible. A missed primary care appointment is not visible in the same way.

So the system can end up doing something perverse. It tightly manages growth in the lower-cost, earlier-intervention parts of the system, then funds the more expensive hospital consequences later.

That is the “hospital growth by default” hypothesis.

The answer is not to abolish capitation. Capitation has important strengths. The answer is also not to create an uncontrolled fee-for-service free-for-all. Fee-for-service means paying for each service, and if it is poorly designed it can reward low-value volume.

The answer is a hybrid.

My working proposal is this:

> Keep capitation for continuity and population responsibility. Add an uncapped, rules-based, fee-for-service stream for eligible primary medical activity, similar in logic to Accident Compensation Corporation treatment payments. Pair that with place-based accountability so providers cannot simply cherry-pick easy work.

Uncapped does not mean uncontrolled. It means the total volume of eligible primary medical work is not artificially fixed in advance. The controls sit elsewhere: item rules, public contribution rates, clinical necessity, provider scope, documentation, audit, co-payment protections, and accountability for whole populations.

That is the big idea in this series.

I want to explain it slowly. I will cover fee-for-service, capitation, co-payments, primary health organisations, Accident Compensation Corporation, urgent care, ambulance, game theory, microeconomics, modelling, and why formula fights can go on forever without solving the real problem.

## What would change my mind?

I would be less convinced if better appointment data showed that tight control of upstream care was not associated with higher emergency department use, longer waits, closed books, or delayed care once need, rurality and deprivation were taken into account.

---

**Deep dive (optional, not required reading):** I’ve kept the fuller explanation, game table, modelling notes and full source list in the [appendix for this post](../appendices-v1.6.0/appendix-01-are-we-buying-hospital-growth-by-rationing-cheaper-care-upstream-v1.6.0.md).

**Note:** This series is exploratory policy analysis. It is not a party-political argument, not a claim that any single funding model is perfect, and not a calibrated prediction of savings. The central question is whether New Zealand's current funding architecture lets lower-cost upstream care expand safely before need becomes hospital demand.

## Useful links

- [Ministry of Health: capitation reweighting](https://www.health.govt.nz/strategies-initiatives/programmes-and-initiatives/primary-and-community-health-care/capitation-reweighting)
- [Cabinet material: Primary Health Care Funding Improvements](https://www.health.govt.nz/information-releases/cabinet-material-primary-health-care-funding-improvements-and-update-on-primary-health-care)
- [Health New Zealand: National Primary Care Dataset and new primary care health target](https://www.healthnz.govt.nz/about-us/what-we-do/planning-and-performance/primary-care-tactical-action-plan/national-primary-care-dataset-and-new-primary-care-health-target)
- [Ministry of Health: primary care health target](https://www.health.govt.nz/strategies-initiatives/programmes-and-initiatives/primary-and-community-health-care/primary-care-health-target)
- [Treasury: Vote Health 2025/26 Estimates](https://www.treasury.govt.nz/publications/estimates/vote-health-health-sector-estimates-appropriations-2025-26)

---

# Fee-for-service, capitation and blended funding: the plain-English version

**Source-confidence label:** public-document supported policy hypothesis, economic theory and model assumption; not calibrated prediction.

Before talking about reform, it helps to understand the three basic ways we pay for primary care.

The first is fee-for-service. A provider does a service and receives a payment. The service might be a consultation, a procedure, a review, a wound dressing, a vaccination, a minor operation or an urgent assessment.

Fee-for-service has one major strength: it pays for the next piece of work.

If a clinic sees more patients, it receives more revenue. If a nurse practitioner provides more eligible consultations, those consultations can be funded. If a rural clinician does more urgent-care sessions, there is a payment signal attached to that work.

That can increase supply. It tells the system that doing more work is financially possible.

But fee-for-service has a danger. If it is poorly designed, it can reward volume rather than value. It can make short, simple, repeat contacts more attractive than slow, complex, relationship-based care. It can also encourage providers to focus on services that are easy to bill, rather than services that matter most.

So fee-for-service is useful, but dangerous.

The second model is capitation. A provider receives a fixed payment for each enrolled person, usually adjusted by patient characteristics such as age, sex, deprivation, rurality and illness burden.

Capitation has real strengths. It supports continuity. It gives a clinic responsibility for a defined population. It can support preventive care and team-based work that does not fit neatly into a single consultation. It is also attractive to funders because the total funding is more predictable.

But capitation has a different danger. Once the patient is enrolled, the next contact is often a cost rather than a revenue event. If a person needs more visits, more phone calls, more follow-up, more complexity and more risk management, the practice may receive little additional payment.

That can lead to rationing. Not necessarily because anyone is being lazy or uncaring. It happens because time and workforce are finite.

The third model is programme or targeted funding. This is money for specific activities, such as immunisation, long-term condition care, screening, care coordination or access programmes.

Targeted funding can be useful when government wants to promote particular outcomes. But it can become complicated. It can fragment care into many little funding streams, each with its own forms, rules, audits and reporting.

This is why most sensible systems use a blend.

A blended model uses capitation for baseline responsibility, fee-for-service for eligible activity, and targeted funding for priority programmes. The trick is not choosing one model as if it were perfect. None of them is perfect.

The trick is matching the payment signal to the type of care.

For example:

- continuity and preventive care suit capitation;
- urgent appointments and procedures suit fee-for-service;
- immunisation catch-up or outreach may suit targeted funding;
- rural access may need loading or place-based support;
- complex long-term care may need both capitation and activity-sensitive payments.

In New Zealand, the Government itself describes primary care funding as blended: capitation, co-payments and targeted streams. That is true. But the important question is whether the blend is strong enough at the margin.

The margin is the next appointment.

If the next appointment is clinically needed but weakly funded, the system may still ration access even if the overall model is technically “blended”.

That is why I keep coming back to an Accident Compensation Corporation-style analogy. Accident Compensation Corporation payments are not unlimited chaos. They are rules-based. Providers must be qualified. Treatment must be clinically appropriate. Documentation is required. Some items require approval. There are scheduled contributions.

In other words, activity can be demand-led without being uncontrolled.

That is the distinction I think New Zealand needs to explore for primary medical care.

Not a blank cheque.

Not a return to 1980s medicine.

Not replacing capitation.

A properly designed hybrid.

Capitation for population responsibility.

Fee-for-service for eligible medical activity.

Place-based commissioning for people and communities who might otherwise be left behind.

And transparent data so we can see whether the system is actually improving access, rather than just shifting patients around.

![fig-02-funding-models-101-v1.2.0](../figures/fig-02-funding-models-101-v1.2.0.png)


### The useful way to think about all three

A simple way to remember the three models is this:

- capitation pays for **responsibility**;
- fee-for-service pays for **activity**;
- programme funding pays for **specific organised work**.

A mature system usually needs all three. The argument starts when one of them is asked to do a job it cannot do well.

## What would change my mind?

I would be less convinced if one payment model consistently delivered access, equity, continuity, fiscal control and rural supply without needing the others. I do not think the evidence or lived system experience shows that.

---

**Deep dive (optional, not required reading):** I’ve kept the fuller explanation, game table, modelling notes and full source list in the [appendix for this post](../appendices-v1.6.0/appendix-02-fee-for-service-capitation-and-blended-funding-the-plain-english-version-v1.6.0.md).

**Note:** This series is exploratory policy analysis. It is not a party-political argument, not a claim that any single funding model is perfect, and not a calibrated prediction of savings. The central question is whether New Zealand's current funding architecture lets lower-cost upstream care expand safely before need becomes hospital demand.

## Useful links

- [Ministry of Health: capitation reweighting](https://www.health.govt.nz/strategies-initiatives/programmes-and-initiatives/primary-and-community-health-care/capitation-reweighting)
- [RACGP/AJGP: understanding general practice funding models](https://www1.racgp.org.au/ajgp/2024/december/understanding-general-practice-funding-models-in-a)
- [Cochrane: payment methods for outpatient healthcare providers](https://www.cochrane.org/evidence/CD011865_payment-methods-healthcare-providers-outpatient-healthcare-settings)
- [Australian Department of Health: Review of General Practice Incentives](https://www.health.gov.au/resources/publications/review-of-general-practice-incentives-expert-advisory-panel-report-to-the-australian-government?language=en)
- [Accident Compensation Corporation: paying patient treatment](https://www.acc.co.nz/for-providers/invoicing-us/paying-patient-treatment)

---

# Marginal supply: the tiny economic idea that decides whether appointments exist

**Source-confidence label:** public-document supported policy hypothesis, economic theory and model assumption; not calibrated prediction.

A lot of this debate turns on one small economic idea: marginal supply.

“Marginal” means the next one.

The next appointment. The next prescription review. The next same-day urgent slot. The next rural clinic. The next wound dressing. The next complex consultation. The next follow-up after an ambulance crew decides not to take someone to hospital.

The question is simple:

![Figure for Marginal supply: the tiny economic idea that decides whether appointments exist](../figures/fig-15-marginal-revenue-cost-v1.5.0.png)

*Figure: conceptual explainer for this post. It is not an observed outcome chart or calibrated prediction.*

> Is the next clinically useful contact financially viable for the provider to deliver?

That does not mean clinicians think only about money. They do not. But clinics are not abstract moral machines. They are organisations with finite staff, rooms, phones, software, admin support, rent, indemnity, clinical risk and exhaustion.

If the next contact has a cost, but little or no payment signal, the system will ration it.

That is especially true when workforce is tight.

Under a mostly capitated system, a practice receives a fixed payment per enrolled person. That payment helps support the practice. But after the patient is enrolled, seeing them more often may not bring enough additional revenue to cover the extra time and cost.

Under fee-for-service, the next eligible contact brings a payment. That payment may not fully cover cost either, but it creates a marginal signal. It tells the provider that expanding activity is possible.

The diagram below is deliberately simple. It shows marginal cost rising as a practice takes on more contacts. Early contacts may be easy to absorb. Later ones are harder because the practice needs extra staff, longer hours, more rooms or more administration.

Under weak marginal revenue, supply stops early. Under scheduled fee-for-service, more contacts become viable.

![fig-08-marginal-supply-capitation-vs-ffs-v1.4.0](../figures/fig-08-marginal-supply-capitation-vs-ffs-v1.4.0.png)

This is not an argument that fee-for-service is always good. It is an argument that every system needs some way to pay for the next clinically necessary contact.

If it does not, the rationing still happens. It just happens less honestly.

The system rations by:

- waiting time;
- closed books;
- appointment length;
- phone triage;
- co-payment increases;
- referral thresholds;
- telling patients to use emergency departments;
- shifting work to ambulance or urgent care;
- using telehealth for problems that may still need hands-on examination.

Some of those tools are useful. Triage is useful. Telehealth is useful. Co-payments can play a role. But when they become the main rationing mechanism, the system is in trouble.

A hard funding envelope can look tidy from the centre. The budget is controlled. The line item is stable. The formula is updated. The target is announced.

But from the patient’s point of view, the question is simpler: can I get care when I need it?

From the provider’s point of view: can we afford to open another slot without burning out staff or bankrupting the practice?

From the hospital’s point of view: why are more people turning up at the emergency department?

Those are all marginal-supply questions.

This is why I think New Zealand should explore an uncapped, scheduled, rules-based primary medical fee-for-service stream. Not uncapped prices. Not uncapped provider behaviour. Uncapped eligible activity.

The public contribution would be scheduled. The service would need to be eligible. The provider would need to be working within scope. Documentation would be required. Patterns of overuse would be audited. Co-payment protections would be needed for children, Community Services Card holders, rural patients, high-need groups and people with complex long-term conditions.

The point is to stop using a capped envelope as the main control.

A capped envelope is simple, but it pushes pressure elsewhere.

A rules-based activity stream is more complicated, but it can let supply grow where care is lower cost and earlier.

Microeconomics does not tell us the exact policy answer. But it does tell us what to look for.

If the next clinically useful contact is unfunded, that contact will eventually disappear.

And if enough contacts disappear upstream, they reappear downstream as ambulance calls, urgent care demand and hospital pressure.


### Why this matters for rural areas

Marginal supply is especially important in rural areas. A city practice may be able to absorb a bit more work by using a larger team, extending hours or shifting some care to telehealth. A rural service may have fewer staff, fewer rooms, longer travel times, fewer locums and less backup.

That means the marginal cost of the next in-person clinic can rise very quickly. If the payment signal does not rise with it, the system will drift toward remote-only care or no care at all.

## What would change my mind?

I would be less convinced if practices could reliably increase timely appointments under fixed capitation alone, without higher co-payments, shorter consultations, hidden rationing, or extra activity-linked funding.

---

**Deep dive (optional, not required reading):** I’ve kept the fuller explanation, game table, modelling notes and full source list in the [appendix for this post](../appendices-v1.6.0/appendix-03-marginal-supply-the-tiny-economic-idea-that-decides-whether-appointments-exist-v1.6.0.md).

**Note:** This series is exploratory policy analysis. It is not a party-political argument, not a claim that any single funding model is perfect, and not a calibrated prediction of savings. The central question is whether New Zealand's current funding architecture lets lower-cost upstream care expand safely before need becomes hospital demand.

## Useful links

- [Ministry of Health: capitation reweighting](https://www.health.govt.nz/strategies-initiatives/programmes-and-initiatives/primary-and-community-health-care/capitation-reweighting)
- [Accident Compensation Corporation: paying patient treatment](https://www.acc.co.nz/for-providers/invoicing-us/paying-patient-treatment)
- [Cochrane: payment methods for outpatient healthcare providers](https://www.cochrane.org/evidence/CD011865_payment-methods-healthcare-providers-outpatient-healthcare-settings)
- [RACGP/AJGP: understanding general practice funding models](https://www1.racgp.org.au/ajgp/2024/december/understanding-general-practice-funding-models-in-a)
- [Cabinet material: Primary Health Care Funding Improvements](https://www.health.govt.nz/information-releases/cabinet-material-primary-health-care-funding-improvements-and-update-on-primary-health-care)

---

# Why formulas do not solve games

**Source-confidence label:** public-document supported policy hypothesis, economic theory and model assumption; not calibrated prediction.

Funding formulas look technical. They feel objective. They use numbers, weights, datasets, regression models and official language.

But formulas do not remove politics. They often concentrate it.

New Zealand has seen this before with the Population-Based Funding Formula, which was used to distribute District Health Board funding. A New Zealand Medical Journal article analysed 487 newspaper articles about that formula between 2003 and 2016. The formula became a public flashpoint, especially in the South Island. A central theme was dissatisfaction with allocations and concern about transparency.

That should not surprise anyone.

![Figure for Why formulas do not solve games](../figures/fig-09-fixed-envelope-rationing-v1.4.0.png)

*Figure: conceptual explainer for this post. It is not an observed outcome chart or calibrated prediction.*

A funding formula is a way of deciding shares. Once shares are at stake, everyone has a reason to argue that the formula misses something important.

Rurality. Deprivation. Age. Ethnicity. Unmet need. Complexity. Diseconomies of scale. Transport. Workforce costs. Growth. Decline. Fixed infrastructure. Historical underfunding. Future demand.

All of those things matter.

But the more variables you add, the more the debate becomes a contest about weights. One group says deprivation is underweighted. Another says rurality is underweighted. Another says age is underweighted. Another says historical utilisation bakes in past access failure. Another says the model punishes efficient providers. Another says it rewards providers who generate activity.

That does not mean formulas are useless. They are necessary. If public money is being allocated across populations, there must be some logic to the allocation.

But a formula can only answer one kind of question:

> How should a funding pool be distributed?

It cannot fully answer a different question:

> Should the pool itself be capped in a way that suppresses clinically useful activity?

That is the distinction I think matters in primary care.

The current capitation reweighting work is sensible. The Ministry of Health says the old formula was based on how people used general practice in the late 1990s. Since then New Zealand has changed: more long-term conditions, more multimorbidity, more treatment options, more complexity managed in the community, and different rural and deprivation patterns.

So yes, the formula should change.

But reweighting capitation does not solve the marginal-supply problem by itself.

It can make funding distribution fairer across practices. It can move more funding toward practices with higher-need enrolled populations. It can reduce some inequity. Those are good things.

But if the overall architecture remains heavily capped, the next appointment may still be weakly funded.

This is why I worry about “missing the wood from the trees”.

The tree is the formula. The wood is the system game.

The formula asks whether Practice A should get more than Practice B.

The game asks whether either practice can afford to provide the next clinically needed contact.

The formula asks whether rurality should have a higher weight.

The game asks whether a rural patient can actually see someone in person.

The formula asks whether multimorbidity is included.

The game asks whether complex patients get enough time, follow-up and coordination.

The formula asks whether deprivation is measured properly.

The game asks whether people in deprived communities are rationed by cost, waiting time or closed books.

The formula asks whether the model is fair.

The game asks whether the system grows in the right place.

That is why my proposal is not to stop capitation reweighting. It is to add another layer.

Keep improving the formula.

But do not expect the formula to do the job of a funding architecture.

The architecture should include:

- capitation for continuity and population accountability;
- uncapped scheduled fee-for-service for eligible primary medical contacts;
- targeted funding for priority programmes;
- place-based accountability to prevent cherry-picking;
- co-payment protections;
- transparent data;
- urgent-care and ambulance integration;
- audit and clinical governance.

That is more complicated than a formula.

But the system is complicated.

The danger is that we spend years arguing over capitation weights while the real supply constraint remains intact.

A better formula may distribute scarcity more fairly.

It may not remove the scarcity.


### The trap in formula politics

Formula fights are seductive because they look technical. Everyone can point to a variable. Age. Deprivation. Rurality. Ethnicity. Multimorbidity. Workforce cost. Practice size. Travel time.

All of those variables matter. But the deeper problem is that no formula can carry all the political expectations placed on it. If the total envelope is fixed, every added weight creates a redistribution. Someone gains. Someone loses. The debate then becomes a fight over the denominator, the coefficients and the evidence base.

## What would change my mind?

I would be less convinced if capitation reweighting alone materially improved access, reduced closed books, protected rural in-person care and reduced avoidable hospital demand. That is testable.

---

**Deep dive (optional, not required reading):** I’ve kept the fuller explanation, game table, modelling notes and full source list in the [appendix for this post](../appendices-v1.6.0/appendix-04-why-formulas-do-not-solve-games-v1.6.0.md).

**Note:** This series is exploratory policy analysis. It is not a party-political argument, not a claim that any single funding model is perfect, and not a calibrated prediction of savings. The central question is whether New Zealand's current funding architecture lets lower-cost upstream care expand safely before need becomes hospital demand.

## Useful links

- [Ministry of Health: capitation reweighting](https://www.health.govt.nz/strategies-initiatives/programmes-and-initiatives/primary-and-community-health-care/capitation-reweighting)
- [Cabinet material: Primary Health Care Funding Improvements](https://www.health.govt.nz/information-releases/cabinet-material-primary-health-care-funding-improvements-and-update-on-primary-health-care)
- [New Zealand Medical Journal: media content analysis of the Population-Based Funding Formula](https://nzmj.org.nz/media/pages/journal/vol-131-no-1480/a-media-content-analysis-of-new-zealand-s-district-health-board-population-based-funding-formula/6ff2e1d910-1696474509/a-media-content-analysis-of-new-zealand-s-district-health-board-population-based-funding-formula.pdf)
- [New Zealand Medical Journal: Population-Based Funding Formula transparency article](https://nzmj.org.nz/media/pages/journal/vol-126-no-1376/6c9b9d56a4-1696469440/vol-126-no-1376.pdf)
- [Ministry of Health: PHO finances briefing](https://www.health.govt.nz/system/files/2025-11/H2025069314-Briefing-PHO-finances-a-summary-of-available-information.pdf)

---

# The current reform pathway: stronger than a straw man, but maybe still incomplete

**Source-confidence label:** public-document supported policy hypothesis, economic theory and model assumption; not calibrated prediction.

One criticism of my early framing was fair: New Zealand is not doing nothing.

The current reform pathway is more substantial than simply tweaking capitation.

The Government is reweighting capitation. It is introducing a primary care access target. Health New Zealand is building a National Primary Care Dataset. There is performance-based funding. There is 24/7 digital general practitioner access. There is a large urgent and after-hours programme. There are workforce initiatives. There is policy work on Primary Health Organisations. There is a separate appropriation for primary, community, public and population health services.

That matters.

If the critique is written as if the only thing happening is capitation reweighting, it becomes too easy to dismiss.

So the better question is not:

> Why is New Zealand only changing the capitation formula?

The better question is:

> Does the current reform pathway change the game enough?

That is a much stronger question.

The current reform has some obvious strengths.

First, the new capitation formula should be fairer. It includes factors such as age, sex, multimorbidity, rurality and deprivation. That is better than an old formula built from late-1990s utilisation patterns.

Second, the primary care access target makes access visible. For the first time, primary care has a national access target. The proposed target is that more than 80 percent of people can access an appointment with a general practice provider within one week.

Third, the National Primary Care Dataset should improve observability. If we can see when appointments are booked, when people are seen, and what the outcome was, we can start to understand access rather than guessing.

Fourth, urgent and after-hours care is being expanded. The Government has announced investment to support a goal of 98 percent of New Zealanders being able to access urgent care within one hour’s drive.

Fifth, official policy is starting to talk about the broader general practice team, not only doctors.

All of that is important.

But there are still gaps.

A target does not create appointments by itself.

A dataset does not create supply by itself.

A better capitation formula does not necessarily fund the next urgent contact.

A digital service does not replace all local, in-person care.

Urgent care does not solve routine continuity.

Performance payments do not necessarily fix the base economics of practices.

Separate appropriations do not automatically prevent hospital pressure from dominating political attention.

This is why I think the current reform should be treated as the comparator, not the endpoint.

The current reform may improve allocation, visibility and some access. The question is whether it removes the hard cap on eligible primary medical activity.

I do not think it fully does.

The most important missing mechanism is still the marginal supply signal.

If a practice has extra patient demand but no viable way to fund the next clinically useful contact, the system still rations. If a nurse practitioner, pharmacist, paramedic, physiotherapist, general practitioner or other clinician can safely deal with a defined problem, but the funding architecture does not let that activity be generated and paid for, supply is still artificially constrained.

That is why the proposal is to add an uncapped, rules-based fee-for-service stream for eligible primary medical care.

Not all care. Not all providers doing anything they want. Not all volume without controls.

Eligible medical activity.

Scheduled contribution rates.

Scope-based provider eligibility.

Clinical necessity rules.

Documentation.

Audit.

Co-payment protections.

Place-based accountability.

This would sit beside capitation, not replace it.

In other words, the current reform pathway may be the foundation. The hybrid model is the next layer.

The diagram below compares the current reform pathway with the hybrid architecture I am suggesting. It is not a statistical forecast. It is a structured way of thinking about where each architecture is strong and weak.

![fig-14-current-reform-vs-uncapped-hybrid-v1.4.0](../figures/fig-14-current-reform-vs-uncapped-hybrid-v1.4.0.png)

The current reform is strongest on allocation fairness, data, targets and some urgent-care access. The hybrid model is stronger where the current pathway may remain weaker: marginal supply, provider-scope flexibility, whole-population accountability and uncapped eligible activity.

So the critique is not “the Government has done nothing”.

The critique is:

> The Government has started to change the system. But it may still be managing upstream activity too tightly, while hospital demand remains the pressure valve.

That is the game we need to test.


### Why this matters for criticism

If we ignore the current reform agenda, the critique becomes weak. It sounds like we are arguing against a system that no longer exists. That is why the current reform pathway should be the real comparator.

## What would change my mind?

I would be less convinced if the current reform pathway proves it can expand safe upstream supply, not only measure access or redistribute existing capitation funding.

---

**Deep dive (optional, not required reading):** I’ve kept the fuller explanation, game table, modelling notes and full source list in the [appendix for this post](../appendices-v1.6.0/appendix-05-the-current-reform-pathway-stronger-than-a-straw-man-but-maybe-still-incomplete-v1.6.0.md).

**Note:** This series is exploratory policy analysis. It is not a party-political argument, not a claim that any single funding model is perfect, and not a calibrated prediction of savings. The central question is whether New Zealand's current funding architecture lets lower-cost upstream care expand safely before need becomes hospital demand.

## Useful links

- [Ministry of Health: capitation reweighting](https://www.health.govt.nz/strategies-initiatives/programmes-and-initiatives/primary-and-community-health-care/capitation-reweighting)
- [Cabinet material: Primary Health Care Funding Improvements](https://www.health.govt.nz/information-releases/cabinet-material-primary-health-care-funding-improvements-and-update-on-primary-health-care)
- [Ministry of Health: primary care health target](https://www.health.govt.nz/strategies-initiatives/programmes-and-initiatives/primary-and-community-health-care/primary-care-health-target)
- [Health New Zealand: National Primary Care Dataset and new primary care health target](https://www.healthnz.govt.nz/about-us/what-we-do/planning-and-performance/primary-care-tactical-action-plan/national-primary-care-dataset-and-new-primary-care-health-target)
- [Ministry of Health: PHO finances briefing](https://www.health.govt.nz/system/files/2025-11/H2025069314-Briefing-PHO-finances-a-summary-of-available-information.pdf)

---

# What I mean by uncapping primary care funding

**Source-confidence label:** public-document supported policy hypothesis, economic theory and model assumption; not calibrated prediction.

When I say primary care funding should be “uncapped”, I need to be precise.

I do not mean every provider should be able to bill anything, for anything, at any price.

I do not mean abolishing capitation.

I do not mean removing clinical governance.

![Figure for What I mean by uncapping primary care funding](../figures/fig-16-uncapped-scheduled-benefit-supply-v1.5.0.png)

*Figure: conceptual explainer for this post. It is not an observed outcome chart or calibrated prediction.*

I do not mean ignoring equity.

I mean something narrower and more useful:

> Eligible primary medical activity should not be limited by a hard global funding envelope. It should be demand-led within rules.

That is an important difference.

A capped envelope says: here is the total pool; once the pool is exhausted, the system must ration.

A rules-based benefit says: if the service is eligible, the provider is qualified, the patient meets criteria, the documentation is adequate and the claim is not suspicious, the public contribution flows.

That is closer to how Accident Compensation Corporation treatment funding works.

Accident Compensation Corporation does not pay for everything. It pays or contributes to injury treatment when the treatment is clinically appropriate, delivered by an appropriately qualified provider, documented, necessary, and within the relevant regulation or contract.

There are rules. There are item codes. There are contribution rates. There are contracts. Some services require pre-approval. There are expectations about quality and the number of treatments needed.

That is why the Accident Compensation Corporation analogy is useful.

It shows that activity-sensitive funding can be controlled without using a fixed global cap as the main rationing tool.

For primary medical care, an uncapped benefit stream could start with specific contact types:

- same-day or next-day urgent primary medical assessment;
- complex consultations requiring longer time;
- rural in-person assessment;
- minor procedures that prevent escalation;
- follow-up after ambulance non-conveyance;
- care after emergency department discharge;
- clinically necessary reviews for frailty or multimorbidity;
- defined nurse practitioner, pharmacist, paramedic, physiotherapist or general practitioner services within scope.

The public contribution would be scheduled. The patient might pay a co-payment, depending on policy settings. For high-need groups, children, Community Services Card holders, rural patients or priority services, the co-payment could be reduced or removed.

The key point is that the total number of eligible services would not be fixed in advance.

If patients need care, and providers can safely deliver it, the system should not suppress that activity just because the envelope has been capped.

The controls should be smarter:

- item definitions;
- clinical eligibility;
- scope of practice;
- documentation;
- audit;
- unusual-billing detection;
- outcome monitoring;
- co-payment caps;
- locality obligations;
- minimum service coverage;
- reporting against access and equity.

This is what I mean by “uncapped does not mean uncontrolled”.

![fig-13-hybrid-architecture-v1.4.0](../figures/fig-13-hybrid-architecture-v1.4.0.png)

Why does this matter?

Because if the main control is a hard cap, the system often controls the budget by suppressing care upstream.

That does not mean people stop needing care.

It means they wait. Or pay. Or go elsewhere. Or deteriorate. Or call an ambulance. Or end up in hospital.

The hospital system is then funded to deal with the pressure because hospital pressure is more visible and less avoidable.

That is not good economics. It is delayed spending at a higher cost.

A better model would let eligible primary medical activity grow safely.

It would still keep capitation. Capitation is important for continuity and population accountability. It would still keep place-based responsibility. Otherwise providers could cherry-pick easy work and leave hard-to-reach populations behind.

The proposal is a hybrid:

- capitation for having responsibility;
- fee-for-service for doing eligible medical work;
- place-based accountability for reaching everyone;
- data and audit for controlling gaming;
- co-payment protections for equity.

That is not neoliberal. It is not a blank cheque. It is not an anti-public model.

It is a way of paying for the care we want to happen before the hospital becomes the only place left to go.


### What would still be controlled?

This is the part people often miss. If eligible activity is uncapped, almost everything else still needs rules.

The item price is scheduled. The provider must be eligible. The service must match a defined contact type. The provider must act within legal scope. The record must show clinical need. Repeated patterns can be audited. Co-payment protections can be applied. Some services can require pre-approval or additional documentation.

That is why Accident Compensation Corporation is such a useful analogy. It does not mean every provider can bill anything they want forever. It means there is a rules-based stream where eligible injury-related treatment can generate payment.

## What would change my mind?

I would be less convinced if an uncapped scheduled stream could not be governed through item rules, scope, audit, co-payment protections and place accountability. The weak-control version is not the proposal.

---

**Deep dive (optional, not required reading):** I’ve kept the fuller explanation, game table, modelling notes and full source list in the [appendix for this post](../appendices-v1.6.0/appendix-06-what-i-mean-by-uncapping-primary-care-funding-v1.6.0.md).

**Note:** This series is exploratory policy analysis. It is not a party-political argument, not a claim that any single funding model is perfect, and not a calibrated prediction of savings. The central question is whether New Zealand's current funding architecture lets lower-cost upstream care expand safely before need becomes hospital demand.

## Useful links

- [Ministry of Health: capitation reweighting](https://www.health.govt.nz/strategies-initiatives/programmes-and-initiatives/primary-and-community-health-care/capitation-reweighting)
- [Accident Compensation Corporation: paying patient treatment](https://www.acc.co.nz/for-providers/invoicing-us/paying-patient-treatment)
- [Ministry of Business, Innovation and Employment: ACC regulated payments for treatment](https://www.mbie.govt.nz/business-and-employment/employment-and-skills/employment-legislation-reviews/increasing-regulated-acc-payments-for-treatment/proposed-updates-to-acc-regulated-payments-for-treatment/options-for-payment-increases-and-how-they-were-assessed)
- [Cochrane: payment methods for outpatient healthcare providers](https://www.cochrane.org/evidence/CD011865_payment-methods-healthcare-providers-outpatient-healthcare-settings)
- [RACGP/AJGP: understanding general practice funding models](https://www1.racgp.org.au/ajgp/2024/december/understanding-general-practice-funding-models-in-a)