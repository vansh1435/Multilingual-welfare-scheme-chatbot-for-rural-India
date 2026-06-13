# User Flow Diagram

## Channel Entry

```mermaid
flowchart TD
    A["User starts on WhatsApp, SMS, web, or IVR"] --> B["Language choice: Hindi, Tamil, English"]
    B --> C["Q1: Age and gender"]
    C --> D["Q2: Location and work"]
    D --> E["Q3: Income, housing, LPG status"]
    E --> F["Q4: Family needs"]
    F --> G["Q5: Available or missing documents"]
    G --> H["Profile normalizer handles code-mixing"]
    H --> I["Grounded scheme scorer"]
    I --> J["Personalised shortlist with source URLs"]
    J --> K["User selects scheme number"]
    K --> L["Document checklist in chosen language"]
    L --> M["Apply via CSC, Panchayat, bank, Anganwadi, LPG distributor, or official portal"]
```

## Persona 1: Farmer Household

```mermaid
flowchart LR
    A["Sita, 38, rural woman farmer"] --> B["Answers: village, farmer with land, ration card, kutcha house, no LPG"]
    B --> C["Shortlist: PM-KISAN, PMUY, PMAY-G, MGNREGA, PM-JAY"]
    C --> D["Checklist: Aadhaar, bank, land record, ration card, LPG KYC, Gram Sabha verification"]
    D --> E["Next step: PM-KISAN portal/CSC and LPG distributor"]
```

## Persona 2: Gig Worker

```mermaid
flowchart LR
    A["Ravi, 28, delivery driver"] --> B["Answers: city, delivery/gig work, low income, Aadhaar and bank available"]
    B --> C["Shortlist: e-Shram, Atal Pension Yojana, PM-JAY if beneficiary-list match exists"]
    C --> D["Checklist: Aadhaar OTP/CSC biometric, bank account, occupation, nominee details"]
    D --> E["Next step: e-Shram portal/UMANG/CSC and bank for APY"]
```

## Persona 3: Woman Head Of Household

```mermaid
flowchart LR
    A["Meena, 24, rural woman head of household"] --> B["Answers: village labour, ration card, pregnant, girl child below 10, no LPG"]
    B --> C["Shortlist: PMMVY, PMUY, Sukanya Samriddhi, MGNREGA, PM-JAY"]
    C --> D["Checklist: Aadhaar, bank, MCP card, child's birth certificate, ration/family proof"]
    D --> E["Next step: Anganwadi/ASHA, LPG distributor, post office/bank"]
```

## Low-Friction Channel Choice

For a user with a Rs 500 keypad phone, SMS and IVR are the safest fallbacks because they do not require mobile data or app literacy. WhatsApp is better when a shared family smartphone is available because it supports longer text, document links, and language rendering. The project therefore supports all three:

- SMS: short text responses, no media dependency.
- IVR: voice-first flow for low literacy.
- WhatsApp: richer checklist delivery when data is available.

## Offline Fallback

If the user has no data balance:

- Use SMS keyword flow through `/webhook/sms`.
- Use IVR through `/webhook/ivr`.
- Send a compact checklist that can be shown to a CSC operator, Panchayat secretary, ASHA, Anganwadi worker, bank mitra, or LPG distributor.
- Cache the scheme catalogue locally; no live model call is required for core eligibility.
