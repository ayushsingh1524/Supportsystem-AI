from fastapi import FastAPI

from app.graph import build_support_graph


app = FastAPI(
    title="SupportPilot AI",
    description="Agentic AI system for automated support ticket processing.",
    version="1.0.0",
)


graph = build_support_graph()


@app.get("/")
def health_check():
    return {
        "status": "running",
        "service": "SupportPilot AI",
    }


@app.post("/tickets")
def process_ticket(ticket: dict):
    state = {
        "ticket_id": ticket["ticket_id"],
        "customer_message": ticket["customer_message"],
        "category": None,
        "similar_tickets": [],
        "response": None,
        "decision": None,
        "confidence": 0.0,
        "final_status": None,
    }

    result = graph.invoke(state)

    return {
        "ticket_id": result["ticket_id"],
        "category": result["category"],
        "response": result["response"],
        "decision": result["decision"],
        "confidence": result["confidence"],
        "final_status": result["final_status"],
    }