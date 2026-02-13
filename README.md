# Call Automation AI

A lightweight, local-first **call automation AI** starter that helps automate outbound call workflows.

## What it does

- Generates a personalized call opening line.
- Detects basic intent from customer responses:
  - `interested`
  - `not_interested`
  - `callback`
  - `unknown`
- Recommends and applies the next action:
  - handoff to sales
  - do-not-call closure
  - callback scheduling
  - follow-up SMS

## Python quick start

```bash
python call_automation_ai.py
```

## Website quick start (recommended)

Start the included server:

```bash
python serve_web.py
```

Then open:

```text
http://localhost:8000/
```

> The root URL redirects to `/web/` automatically.

Alternative (static server):

```bash
python -m http.server 8000
```

Then open:

```text
http://localhost:8000/web/
```

The website includes:
- contact form fields
- opening-line generation
- customer-reply analysis
- automation status + action output

## Run tests

```bash
pytest -q
```

## Extend it

You can evolve this starter into a production system by adding:

- CRM integration (HubSpot, Salesforce)
- telephony integration (Twilio, Vonage)
- LLM-powered intent scoring and summarization
- callback scheduling windows by timezone
- call compliance filters and opt-out tracking
