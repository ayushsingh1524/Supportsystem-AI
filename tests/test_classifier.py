from app.agents.classifier import classify_ticket
from app.core.models import SupportTicket


def test_billing_classification():
    ticket = SupportTicket(
        ticket_id="TEST002",
        customer_message="I was charged twice for my order",
    )

    result = classify_ticket(ticket)

    assert result.category == "billing"


def test_account_classification():
    ticket = SupportTicket(
        ticket_id="TEST003",
        customer_message="I forgot my password",
    )

    result = classify_ticket(ticket)

    assert result.category == "account"