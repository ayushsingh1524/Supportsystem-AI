from pydantic import BaseModel


class SupportTicket(BaseModel):
    ticket_id: str
    customer_message: str
    category: str | None = None
    priority: str | None = None
    status: str = "open"
