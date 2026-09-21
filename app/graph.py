from typing import TypedDict

from langgraph.graph import END, START, StateGraph

from app.agents.classifier import classify_ticket
from app.agents.responder import generate_response
from app.agents.router import route_ticket
from app.core.models import SupportTicket
from app.rag.vector_store import build_knowledge_base, search_similar_tickets


class SupportState(TypedDict):
    ticket_id: str
    customer_message: str
    category: str | None
    similar_tickets: list[dict]
    response: str | None
    decision: str | None
    confidence: float
    final_status: str | None


def classify_node(state: SupportState) -> SupportState:
    ticket = SupportTicket(
        ticket_id=state["ticket_id"],
        customer_message=state["customer_message"],
    )

    ticket = classify_ticket(ticket)

    return {
        **state,
        "category": ticket.category,
    }


def retrieval_node(state: SupportState) -> SupportState:
    build_knowledge_base()

    results = search_similar_tickets(
        state["customer_message"],
        n_results=3,
    )

    similar_tickets = [
        {
            "ticket": document,
            "category": metadata["category"],
            "resolution": metadata["resolution"],
        }
        for document, metadata in zip(
            results["documents"][0],
            results["metadatas"][0],
        )
    ]

    return {
        **state,
        "similar_tickets": similar_tickets,
    }


def response_node(state: SupportState) -> SupportState:
    response = generate_response(
        ticket_message=state["customer_message"],
        similar_tickets=state["similar_tickets"],
    )

    return {
        **state,
        "response": response,
    }


def router_node(state: SupportState) -> SupportState:
    result = route_ticket(
        ticket_message=state["customer_message"],
        category=state["category"] or "other",
        response=state["response"] or "",
    )

    return {
        **state,
        "decision": result["decision"],
        "confidence": result["confidence"],
    }


def resolve_node(state: SupportState) -> SupportState:
    return {
        **state,
        "final_status": "resolved",
    }


def escalate_node(state: SupportState) -> SupportState:
    return {
        **state,
        "final_status": "escalated_to_human",
    }


def route_decision(state: SupportState) -> str:
    if state["decision"] == "resolve":
        return "resolve"

    return "escalate"


def build_support_graph():
    graph = StateGraph(SupportState)

    graph.add_node("classify", classify_node)
    graph.add_node("retrieve", retrieval_node)
    graph.add_node("respond", response_node)
    graph.add_node("route", router_node)
    graph.add_node("resolve", resolve_node)
    graph.add_node("escalate", escalate_node)

    graph.add_edge(START, "classify")
    graph.add_edge("classify", "retrieve")
    graph.add_edge("retrieve", "respond")
    graph.add_edge("respond", "route")

    graph.add_conditional_edges(
        "route",
        route_decision,
        {
            "resolve": "resolve",
            "escalate": "escalate",
        },
    )

    graph.add_edge("resolve", END)
    graph.add_edge("escalate", END)

    return graph.compile()