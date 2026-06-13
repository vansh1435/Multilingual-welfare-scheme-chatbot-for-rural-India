# Pilot Test Report Package

## Status

Real field testing has not been conducted inside this coding environment. This file is therefore split into:

- Field pilot protocol for 10-15 real users.
- Data collection sheet structure.
- Synthetic dry run using 12 scripted personas to verify that the prototype flow behaves as expected.

Do not present the synthetic section as real field evidence.

## Field Pilot Protocol

Target sample: 12 users from a nearby village, informal worker cluster, SHG group, Panchayat queue, or community centre.

Personas to include:

- 4 farmer or farm-labour households.
- 3 women heads of household or mothers.
- 3 unorganised/gig workers.
- 2 elderly, widow, or disability pension candidates.

Test channels:

- 6 users on WhatsApp or web on a shared smartphone.
- 4 users on SMS-like text flow.
- 2 users through IVR read-aloud flow.

Tasks:

1. Choose language.
2. Complete the 5-question flow.
3. Read or listen to the top 2 scheme summaries.
4. Select one scheme and retrieve checklist.
5. Answer 3 comprehension questions.

## Metrics

- Completion rate: user reaches shortlist without facilitator rescue.
- Drop-off point: language, age, work, income/assets, family needs, documents, shortlist.
- Comprehension: 3-question score.
- Response time: median response under 3 seconds on simulated 2G/3G.
- Checklist usefulness: user says whether they know the next place to visit.

Comprehension questions:

- What is the first office/person you should visit for the selected scheme?
- Name two documents you need.
- Is the chatbot approval final, or does an official still verify?

## Data Collection Sheet

| User ID | Persona | Channel | Language | Completed | Drop-off step | Top scheme understood | Quiz score /3 | Median response sec | Notes |
|---|---|---|---|---|---|---|---:|---:|---|
| U01 | Farmer | WhatsApp | Hindi |  |  |  |  |  |  |
| U02 | Woman HoH | SMS | Hindi |  |  |  |  |  |  |
| U03 | Gig worker | Web | Tamil |  |  |  |  |  |  |
| U04 | Elderly | IVR | Hindi |  |  |  |  |  |  |
| U05 | Farm labour | SMS | Tamil |  |  |  |  |  |  |
| U06 | Mother | WhatsApp | Tamil |  |  |  |  |  |  |
| U07 | Domestic worker | Web | Hindi |  |  |  |  |  |  |
| U08 | Farmer | SMS | Hindi |  |  |  |  |  |  |
| U09 | Widow | IVR | Tamil |  |  |  |  |  |  |
| U10 | Delivery worker | WhatsApp | Tamil |  |  |  |  |  |  |
| U11 | Farmer | Web | Hindi |  |  |  |  |  |  |
| U12 | Disability pension | SMS | Hindi |  |  |  |  |  |  |

## Synthetic Dry Run

The following was run with scripted personas, not real users.

| Script ID | Persona | Language | Expected schemes | Result |
|---|---|---|---|---|
| S01 | Rural woman farmer, ration, kutcha house, no LPG | Hindi | PM-KISAN, PMUY, PMAY-G | Pass |
| S02 | Tamil delivery driver, low income, bank | Tamil | e-Shram, APY | Pass |
| S03 | Rural labour household, pregnant woman | English | MGNREGA, PMMVY | Pass |
| S04 | Woman with daughter below 10 | Hindi | Sukanya Samriddhi | Pass |
| S05 | Elderly low-income household | English | NSAP, PM-JAY | Pass |
| S06 | User says Aadhaar lost | Hindi-English code-mix | Missing Aadhaar fallback | Pass |
| S07 | Unknown tractor-drone query | English | Refusal/no hallucination | Pass |
| S08 | Rural no-LPG poor household | Tamil | PMUY | Pass |
| S09 | Rural kutcha-house household | Hindi | PMAY-G | Pass |
| S10 | Farmer with land | Hindi | PM-KISAN | Pass |
| S11 | Hospital need with ration card | English | PM-JAY | Pass |
| S12 | User asks for checklist by number | English | Checklist returned | Pass |

Local automated check:

```text
Unit tests: 5 passed
Median engine latency: under 1 ms
Max SMS reply length: 850 characters
Static UI asset size: 9.1 KB
```

## Pilot Risk Register

| Risk | Mitigation |
|---|---|
| Users confuse shortlist with approval | Bot repeats that final verification is official. Quiz question checks this. |
| Document names are unfamiliar | Checklist uses simple terms and local worker destination. |
| Tamil/Hindi dialect variation | Add village-specific synonyms after field notes. |
| Low literacy | IVR flow and facilitator read-aloud protocol. |
| State scheme differences | Keep central schemes first; add state module after local pilot. |

## Acceptance Targets

- At least 80% completion without drop-off.
- At least 70% average comprehension score.
- Median response time below 3 seconds.
- At least 70% users can name the next office/person to visit.

## Field Report Template

After real testing, replace this section:

```text
Date:
Location:
Facilitators:
Number of users:
Channels used:
Completion rate:
Average comprehension score:
Median response time:
Most confusing question:
Most requested dialect words:
Schemes most frequently shortlisted:
Top 5 fixes before deployment:
Consent and privacy notes:
```
