# Architecture

## Flow
1. Client submits SOP text to FastAPI.
2. Analyzer extracts steps, systems, data entities, and decision points.
3. Planner maps each step to: RAG, tool-using agent, RPA/classic automation, or human.
4. Risk scorer flags PII, approvals, financial impact, and audit needs.
5. Response returns architecture blueprint plus ROI estimate ranges.

## Key decisions
- Keep the planner deterministic and explainable; LLM is used for extraction, not final approval.
- Every automated financial/legal step requires human-in-the-loop.
- All tool calls are logged for audit.

## Production hardening
- Replace mock planner with LangGraph + model gateway.
- Add auth, tenant isolation, eval datasets, and observability.
