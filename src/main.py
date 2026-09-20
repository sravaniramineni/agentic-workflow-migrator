from fastapi import FastAPI
from pydantic import BaseModel, Field
from .scoring import score_step, estimate_roi

app = FastAPI(title="Agentic Workflow Migrator")

class AnalyzeRequest(BaseModel):
    sop_text: str = Field(min_length=20)
    minutes_per_step: float = 15.0
    frequency_per_month: int = 100

class StepPlan(BaseModel):
    step: str
    pattern: str
    rationale: str
    risk: float
    confidence: float

class AnalyzeResponse(BaseModel):
    steps: list[StepPlan]
    recommended_architecture: str
    roi: dict

@app.post("/analyze", response_model=AnalyzeResponse)
def analyze(req: AnalyzeRequest):
    chunks = [c.strip() for c in req.sop_text.replace("\n", " ").split(".") if c.strip()]
    steps = []
    for i, chunk in enumerate(chunks[:12], start=1):
        s = score_step(chunk)
        steps.append(StepPlan(step=f"Step {i}: {chunk[:80]}", **s))
    return AnalyzeResponse(
        steps=steps,
        recommended_architecture="RAG knowledge layer + tool-using agents + human approvals",
        roi=estimate_roi([s.model_dump() for s in steps], req.minutes_per_step, req.frequency_per_month),
    )
