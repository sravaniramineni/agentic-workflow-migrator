"""Risk, confidence, and ROI scoring for migration plans."""

RISK_WEIGHTS = {
    "approve": 0.35, "payment": 0.35, "refund": 0.30, "legal": 0.40,
    "contract": 0.35, "pii": 0.25, "customer data": 0.25, "audit": 0.15,
}
AUTOMATION_SIGNALS = {
    "lookup": 0.2, "search": 0.2, "report": 0.15, "copy": 0.25,
    "paste": 0.25, "download": 0.15, "upload": 0.15, "email": 0.10,
}

def score_step(text: str) -> dict:
    lowered = text.lower()
    risk = 0.05
    for kw, w in RISK_WEIGHTS.items():
        if kw in lowered:
            risk += w
    automation_fit = sum(w for kw, w in AUTOMATION_SIGNALS.items() if kw in lowered)
    confidence = round(min(0.95, 0.55 + automation_fit), 2)
    if risk >= 0.5:
        pattern, rationale = "human-in-the-loop", "High financial/legal/PII risk; require approval."
    elif automation_fit >= 0.2 and any(k in lowered for k in ("lookup", "search", "find", "report")):
        pattern, rationale = "RAG", "Knowledge retrieval over enterprise sources."
    elif automation_fit >= 0.15:
        pattern, rationale = "tool-using agent", "Repetitive multi-step action across systems."
    else:
        pattern, rationale = "needs-discovery", "Ambiguous step; run a stakeholder workshop."
    return {
        "risk": round(min(risk, 1.0), 2),
        "confidence": confidence,
        "pattern": pattern,
        "rationale": rationale,
    }

def estimate_roi(steps: list[dict], minutes_per_step: float = 15.0, frequency_per_month: int = 100) -> dict:
    automatable = [s for s in steps if s["pattern"] in ("RAG", "tool-using agent")]
    hours_saved = len(automatable) * minutes_per_step * frequency_per_month / 60
    return {
        "automatable_steps": len(automatable),
        "total_steps": len(steps),
        "est_hours_saved_monthly": round(hours_saved, 1),
        "note": "Validate minutes_per_step and frequency with stakeholders before committing.",
    }
