from fastapi import FastAPI
from pydantic import BaseModel, Field

app = FastAPI(title="Agentic Workflow Migrator")

class AnalyzeRequest(BaseModel):
    sop_text: str = Field(min_length=20)

class StepPlan(BaseModel):
    step: str
    pattern: str
    rationale: str

class AnalyzeResponse(BaseModel):
    steps: list[StepPlan]
    recommended_architecture: str
    roi_note: str

@app.post("/analyze", response_model=AnalyzeResponse)
def analyze(req: AnalyzeRequest):
    # Starter heuristic: production would use LangGraph + LLM extraction.
    chunks = [c.strip() for c in req.sop_text.replace("\n", " ").split(".") if c.strip()]
    steps = []
    for i, chunk in enumerate(chunks[:8], start=1):
        lowered = chunk.lower()
        if any(k in lowered for k in ["approve", "payment", "legal", "contract"]):
            pattern = "human-in-the-loop"
            rationale = "High financial/legal risk; require approval."
        elif any(k in lowered for k in ["lookup", "search", "find", "report"]):
            pattern = "RAG"
            rationale = "Knowledge retrieval over enterprise sources."
        else:
            pattern = "tool-using agent"
            rationale = "Multi-step action across systems/APIs."
        steps.append(StepPlan(step=f"Step {i}: {chunk[:80]}", pattern=pattern, rationale=rationale))
    return AnalyzeResponse(
        steps=steps,
        recommended_architecture="RAG knowledge layer + tool-using agents + human approvals",
        roi_note="Estimate manual effort per step and multiply by frequency; validate with stakeholders.",
    )
