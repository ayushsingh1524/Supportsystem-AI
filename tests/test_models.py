from app.core.models import SupportTicket


def test_support_ticket_creation():
    ticket = SupportTicket(
        ticket_id="TEST004",
        customer_message="My payment failed",
    )

    assert ticket.ticket_id == "TEST004"
    assert ticket.customer_message == "My payment failed"
    assert ticket.category is None
    assert ticket.priority is None
    assert ticket.status == "open"


def test_support_ticket_defaults():
    ticket = SupportTicket(
        ticket_id="TEST005",
        customer_message="Where is my order?",
    )

    assert ticket.status == "open"