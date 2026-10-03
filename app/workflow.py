"""LangGraph workflow: triage classification, then a simulated next action.

This demo uses deterministic keyword matching instead of an LLM.
It is not a medical diagnosis system.
"""

from typing import Literal, TypedDict

from langgraph.graph import END, START, StateGraph

# Allowed triage labels produced by the graph.
TriageStatus = Literal["Emergency", "Routine", "Admin"]


class WorkflowState(TypedDict):
    """Shared state that flows through the LangGraph nodes."""

    patient_id: str
    query: str
    status: str
    action: str


# Emergency phrases are checked first so urgent wording wins over admin wording.
EMERGENCY_KEYWORDS = (
    "severe chest pain",
    "chest pain",
    "difficulty breathing",
    "shortness of breath",
    "can't breathe",
    "cannot breathe",
    "unconscious",
    "unresponsive",
    "severe bleeding",
    "heavy bleeding",
    "stroke",
    "face drooping",
    "slurred speech",
    "heart attack",
)

ADMIN_KEYWORDS = (
    "appointment",
    "billing",
    "insurance",
    "reschedule",
    "cancellation",
    "cancel",
    "medical records",
    "medical record",
)

# Simulated next step for each triage status.
ACTIONS = {
    "Emergency": "Seek immediate emergency medical care",
    "Routine": "Route to doctor",
    "Admin": "Route to administrative support",
}


def classify_query(query: str) -> TriageStatus:
    """Return exactly one of Emergency, Routine, or Admin using keywords."""
    text = query.lower()

    if any(keyword in text for keyword in EMERGENCY_KEYWORDS):
        return "Emergency"

    if any(keyword in text for keyword in ADMIN_KEYWORDS):
        return "Admin"

    return "Routine"


def triage_node(state: WorkflowState) -> dict:
    """Inspect the patient query and set the triage status."""
    status = classify_query(state["query"])
    return {"status": status}


def action_node(state: WorkflowState) -> dict:
    """Turn the triage status into a simulated next action."""
    status = state["status"]
    return {"action": ACTIONS[status]}


def build_workflow():
    """Build a two-node graph: START -> triage -> action -> END."""
    graph = StateGraph(WorkflowState)

    graph.add_node("triage", triage_node)
    graph.add_node("action", action_node)

    graph.add_edge(START, "triage")
    graph.add_edge("triage", "action")
    graph.add_edge("action", END)

    return graph.compile()


# Compile once when the module loads so each API call reuses the same graph.
workflow = build_workflow()


def run_triage(patient_id: str, query: str) -> WorkflowState:
    """Run the graph and return the final state."""
    return workflow.invoke(
        {
            "patient_id": patient_id,
            "query": query,
            "status": "",
            "action": "",
        }
    )
