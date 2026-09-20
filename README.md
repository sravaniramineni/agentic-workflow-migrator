# Agentic Workflow Migrator

Turn a written SOP into a step-by-step AI migration plan: which steps should be RAG, which should be tool-using agents, which need a human — plus an ROI estimate you can take to stakeholders.

## When to use this

You're an architect or consultant facing a stack of manual SOPs (invoice processing, onboarding, ticket triage, …) and need a defensible answer to *"what do we automate first, and how?"* This tool gives you a first-pass analysis in seconds so the stakeholder workshop starts with evidence, not opinions.

## How it works

1. **Paste the SOP** — the API splits it into individual steps.
2. **Score every step** — `src/scoring.py` assigns:
   - **risk** (0–1): spikes on words like *approve, payment, refund, legal, PII, audit*
   - **confidence** (0–1): how automatable the step looks
   - **pattern**: one of `RAG`, `tool-using agent`, `human-in-the-loop`, or `needs-discovery`
3. **Get an ROI estimate** — hours saved per month from the automatable steps, using your own `minutes_per_step` and `frequency_per_month` inputs.
4. **Use it as a workshop input** — it narrows the conversation; it doesn't replace stakeholder validation.

## Project structure

```
src/main.py        FastAPI service exposing POST /analyze
src/scoring.py     Step scoring + ROI estimation logic
docs/ARCHITECTURE.md   Design and flow diagrams
docs/ADR-001.md        Why scoring is keyword-based and deterministic
Dockerfile           Container image
.github/workflows/ci.yml   CI on every push
```

## Prerequisites

- Python 3.11+

## Quickstart

```bash
pip install -r requirements.txt
uvicorn src.main:app --reload
```

In another terminal:

```bash
curl -X POST http://localhost:8000/analyze -H "Content-Type: application/json" -d '{
  "sop_text": "Download the vendor invoice PDF. Copy line items into the ERP. Search the vendor master data for duplicates. Approve payment for the finance team.",
  "minutes_per_step": 12,
  "frequency_per_month": 200
}'
```

### Example response

```json
{
  "steps": [
    {"step": "Step 1: Download the vendor invoice PDF", "pattern": "tool-using agent",
     "risk": 0.05, "confidence": 0.7, "rationale": "Repetitive multi-step action across systems."},
    {"step": "Step 3: Search the vendor master data for duplicates", "pattern": "RAG",
     "risk": 0.05, "confidence": 0.75, "rationale": "Knowledge retrieval over enterprise sources."},
    {"step": "Step 4: Approve payment for the finance team", "pattern": "human-in-the-loop",
     "risk": 0.75, "confidence": 0.55, "rationale": "High financial/legal/PII risk; require approval."}
  ],
  "recommended_architecture": "RAG knowledge layer + tool-using agents + human approvals",
  "roi": {"automatable_steps": 3, "total_steps": 4, "est_hours_saved_monthly": 120.0}
}
```

The risk keyword lists (`RISK_WEIGHTS`) and automation signals (`AUTOMATION_SIGNALS`) in `src/scoring.py` are the tuning knobs — adjust them per domain before a real engagement.

## Running the tests / CI

Every push runs the test suite via `.github/workflows/ci.yml`. Run it locally:

```bash
python -m pytest  # add tests/ as the suite grows
```

## Deploy with Docker

```bash
docker build -t workflow-migrator .
docker run -p 8000:8000 workflow-migrator
```

## Taking this to production

- Replace the sentence splitter with a proper SOP parser (one step per numbered item).
- Swap keyword scoring for an LLM-based classifier with a calibration set, keeping this deterministic scorer as a baseline.
- Persist plans to a database; add auth (see the `mcp-tool-gateway` repo pattern).

## Further reading

- `docs/ARCHITECTURE.md` — system design
- `docs/ADR-001.md` — why the scoring is deterministic keyword-based
