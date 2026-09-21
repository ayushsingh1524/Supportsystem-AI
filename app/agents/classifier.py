import os

from google import genai

from app.core.models import SupportTicket


client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))


CATEGORIES = [
    "billing",
    "technical",
    "account",
    "shipping",
    "refund",
    "other",
]


def classify_ticket(ticket: SupportTicket) -> SupportTicket:
    prompt = f"""
You are a support ticket classifier.

Classify the following customer support ticket into exactly ONE category.

Allowed categories:
{", ".join(CATEGORIES)}

Customer ticket:
{ticket.customer_message}

Return ONLY the category name.
"""

    response = client.models.generate_content(
        model="gemini-3.1-flash-lite",
        contents=prompt,
    )

    category = response.text.strip().lower()

    if category not in CATEGORIES:
        category = "other"

    ticket.category = category

    return ticket