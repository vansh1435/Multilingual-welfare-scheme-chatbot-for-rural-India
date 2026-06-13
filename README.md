# JanSahayak

Low-bandwidth multilingual welfare scheme assistant for rural users over web, WhatsApp/SMS-style webhooks, and IVR-style TwiML.

## What It Does

- Supports Hindi, Tamil, and English.
- Covers 10 focused high-impact schemes: PM-KISAN, PM-JAY, PMAY-G, PMUY, MGNREGA, Sukanya Samriddhi, PMMVY, e-Shram, Atal Pension Yojana, and NSAP.
- Runs a 5-question eligibility flow and returns a personalised shortlist.
- Produces scheme-specific document checklists in the user's language.
- Uses a local retrieval catalogue with official scheme URLs instead of hallucinating open-ended eligibility.
- Works without external Python packages.

## Run Locally

```powershell
cd C:\Users\vansh\Documents\Codex\2026-06-13\challenge-1-1-ai-based-multilingual\outputs\jansahayak
python app.py --port 8011
```

Open:

```text
http://127.0.0.1:8011
```

## API

```http
POST /api/chat
Content-Type: application/json

{
  "session_id": "demo-phone-1",
  "message": "1",
  "channel": "web"
}
```

Twilio-compatible endpoints:

```text
POST /webhook/whatsapp
POST /webhook/sms
POST /webhook/ivr
```

For Twilio WhatsApp Sandbox or SMS, point the incoming message webhook to the matching endpoint. The server returns TwiML `<Response><Message>...</Message></Response>`.

For IVR, point a voice webhook to `/webhook/ivr`. The endpoint returns a simple `<Gather>` TwiML response with Hindi speech settings.

## Test And Quality Check

```powershell
python -m unittest discover -s tests -v
python scripts\quality_check.py
```

Current local verification:

```text
unit tests: 5 passed
median_engine_latency_ms: < 1 ms
max_sms_reply_chars: 850
static_asset_size_kb: 9.1 KB
```

## Grounding Strategy

The chatbot never asks a general model to invent eligibility. It retrieves from `data/schemes.json`, scores the user's profile against conservative rules, and returns:

- scheme name
- benefit summary
- document checklist
- application steps
- official source URL
- confidence label

When the answer is state-specific or not in the catalogue, it refuses with a fallback message and directs the user to CSC, Panchayat, bank, Anganwadi, or official portal verification.

## Official Sources Used

- PM-KISAN: https://pmkisan.gov.in/
- PMUY: https://pmuy.gov.in/
- PMMVY: https://pmmvy.wcd.gov.in/
- e-Shram: https://eshram.gov.in/
- NSAP: https://nsap.nic.in/
- myScheme platform context: https://www.myscheme.gov.in/
- Jan Suraksha/APY context: https://jansuraksha.gov.in/
- PM-JAY portal: https://pmjay.gov.in/
- PMAY-G portal: https://pmayg.nic.in/netiayHome/home.aspx
- MGNREGA portal: https://nrega.nic.in/
- India Post savings schemes context: https://www.indiapost.gov.in/

## Deliverables

- `deliverables/user_flow_diagram.md`
- `deliverables/pilot_test_report.md`
- `deliverables/impact_projection.md`
- `deliverables/architecture_and_safety.md`

The pilot report is field-ready and includes a labelled synthetic dry run. It does not claim that real village users were tested, because that would require actual fieldwork.
