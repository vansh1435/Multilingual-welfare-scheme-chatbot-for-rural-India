# 2-Page Impact Projection

## Page 1: Theory Of Change

JanSahayak targets the last-mile awareness gap rather than policy design. The intervention is simple: ask 5 questions in the user's language, shortlist relevant schemes, and send a document checklist with the exact next place to visit.

Problem addressed:

- Rural and low-income users often do not know which schemes apply to them.
- Documentation requirements are intimidating and spread across portals.
- English/Hindi-only portals exclude many Tamil-speaking or dialect-speaking users.
- Low data balance and low literacy make app-heavy workflows unreliable.

Intervention:

- Multilingual chatbot in Hindi, Tamil, and English.
- Channel support for WhatsApp, SMS, IVR, and lightweight web.
- Curated catalogue of 10 high-impact schemes.
- Grounded responses with official source URLs.
- Short, SMS-able document checklists.

Expected behaviour change:

1. User discovers 2-5 likely schemes instead of relying on hearsay.
2. User knows which documents to collect before visiting an office.
3. User visits the correct local touchpoint: CSC, Panchayat, Anganwadi, ASHA, bank, post office, or LPG distributor.
4. Local NGO or district staff spends less time explaining basic eligibility and more time completing applications.

Primary beneficiaries:

- Farmer households: PM-KISAN, PMAY-G, MGNREGA, PM-JAY.
- Women heads of household: PMUY, PMMVY, Sukanya Samriddhi.
- Unorganised/gig workers: e-Shram, APY, PM-JAY.
- Elderly/widow/disability cases: NSAP.

Core success assumptions:

- 80% of users complete the 5-question flow.
- 70% understand the top scheme summary and can name two documents.
- 20% of users who receive a checklist proceed to a local application touchpoint.
- 30-50% of those who proceed complete at least one application or verification step.

## Page 2: District-Scale Estimate

Scenario: one NGO or district administration deploys JanSahayak for 10,000 rural/low-income users over 6 months.

Conservative funnel:

| Stage | Rate | Users |
|---|---:|---:|
| Reached by campaign | 100% | 10,000 |
| Complete flow | 80% | 8,000 |
| Understand shortlist/checklist | 70% of completers | 5,600 |
| Visit correct application touchpoint | 20% of understood users | 1,120 |
| Complete application/verification step | 40% of visitors | 448 |

Illustrative entitlement value:

| Scheme type | Example annual/one-time value | If 448 successful users split across schemes |
|---|---:|---:|
| PM-KISAN | Rs 6,000/year | 120 users = Rs 7.2 lakh/year |
| PM-JAY | Up to Rs 5 lakh hospital cover/year | 100 families receive health risk protection |
| PMUY | Deposit-free LPG connection and first support | 80 households gain clean-cooking access |
| MGNREGA | Wage employment entitlement | 80 households can demand wage work |
| PMMVY/NSAP/SSY/e-Shram/APY | Cash support, pension pathway, savings, registry access | 68 users get targeted next-step support |

Direct cash-flow estimate is intentionally conservative because health insurance, housing, and employment entitlements do not translate into guaranteed immediate cash. Even if only PM-KISAN-like annual cash benefits are counted for 120 households, the direct annual transfer is about Rs 7.2 lakh. If PMAY-G, PM-JAY hospitalisation protection, MGNREGA wage days, and PMUY connection value are included when actually realised, the social protection value can move into crores for a 10,000-beneficiary programme.

Operational cost estimate:

| Cost item | Lean deployment assumption |
|---|---:|
| Server hosting | Free to Rs 1,000/month on Render/Replit/HF Spaces-style hosting |
| WhatsApp/SMS/IVR | Depends on provider and volume; SMS/IVR should be reserved for no-data users |
| Field facilitator training | 1 day for NGO/Panchayat volunteers |
| Catalogue maintenance | Monthly official-source review by one coordinator |

High-leverage adoption path:

1. Pilot with 12 real users and update dialect terms.
2. Add district-specific state schemes and local office contacts.
3. Integrate with a CSC/NGO callback queue for users missing documents.
4. Track anonymised funnel metrics: started, completed, checklist generated, touchpoint visit, application submitted.

Impact safeguards:

- Never claim approval; only recommend next steps.
- Cite official sources.
- Do not collect Aadhaar numbers in chat.
- Keep an offline/SMS/IVR fallback.
- Maintain a versioned scheme catalogue with last-verified dates.

Conclusion:

For a district or NGO serving 10,000 users, the main value is reducing wasted visits and missed eligibility. A modest 20% lift in users taking the correct next step can produce hundreds of additional applications, with direct cash, health-risk protection, wage employment access, housing support, clean fuel access, and pension pathways reaching households that would otherwise remain unaware.
