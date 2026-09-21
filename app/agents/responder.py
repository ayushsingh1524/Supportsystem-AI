import os
import time

from google import genai


client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))


def generate_response(ticket_message: str, similar_tickets: list[dict]) -> str:
    context = "\n\n".join(
        [
            f"Previous ticket: {item['ticket']}\n"
            f"Category: {item['category']}\n"
            f"Resolution: {item['resolution']}"
            for item in similar_tickets
        ]
    )

    prompt = f"""
You are a helpful customer support agent.

Use the previous support cases below as context.

Previous support cases:
{context}

New customer ticket:
{ticket_message}

Write a clear, concise, professional response to the customer.

Rules:
- Use the previous cases as guidance.
- Do not invent policies, refunds, prices, or guarantees.
- If the available context is insufficient, tell the customer that
  the issue needs further assistance.
- Do not mention that you are an AI.
- Return only the response that should be sent to the customer.
"""

    for attempt in range(3):
        try:
            response = client.models.generate_content(
                model="gemini-3.1-flash-lite",
                contents=prompt,
            )

            return response.text.strip()

        except Exception as error:
            print(f"Responder attempt {attempt + 1} failed: {error}")

            if attempt < 2:
                time.sleep(2)

    return (
        "Thank you for contacting support. "
        "We need further assistance to resolve this issue."
    )