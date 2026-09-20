# Agentic Workflow Migrator

Turn a manual standard operating procedure (SOP) into an AI-agent migration plan.

## Problem
Enterprises have manual, multi-step workflows. Leaders need a clear answer to:
what should become RAG, what should become an agent, and what should stay human?

## What it does
- Accepts SOP text via API
- Identifies automatable steps, data sources, and risk points
- Outputs a migration architecture: RAG vs agent vs human-in-the-loop
- Estimates effort, risk, and ROI range

## Architecture
See `docs/ARCHITECTURE.md`.

## Quickstart
```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
uvicorn src.main:app --reload
```

POST `/analyze` with:
```json
{"sop_text": "Step 1: receive invoice..."}
```
