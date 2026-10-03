"""FastAPI entry point for the healthcare triage demo."""

from fastapi import FastAPI
from pydantic import BaseModel, Field

from app.workflow import run_triage

app = FastAPI(
    title="Healthcare Triage API",
    description=(
        "Demo educational workflow that classifies a patient query and "
        "returns a simulated next action. Not a medical diagnosis system."
    ),
    version="1.0.0",
)


class QueryRequest(BaseModel):
    """Incoming JSON body for POST /api/v1/query."""

    patient_id: str = Field(..., min_length=1, description="Patient identifier")
    query: str = Field(..., min_length=1, description="Patient question or symptom text")


class QueryResponse(BaseModel):
    """JSON returned after the LangGraph workflow finishes."""

    patient_id: str
    status: str
    action: str


@app.post("/api/v1/query", response_model=QueryResponse)
def query_endpoint(payload: QueryRequest) -> QueryResponse:
    """Accept a patient query, run triage + action nodes, and return the result."""
    result = run_triage(patient_id=payload.patient_id, query=payload.query)
    return QueryResponse(
        patient_id=result["patient_id"],
        status=result["status"],
        action=result["action"],
    )
