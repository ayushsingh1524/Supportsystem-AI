import os
import time

from google import genai


client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))


def route_ticket(ticket_message: str, category: str, response: str) -> dict:
    prompt = f"""
You are a support ticket quality-control agent.

Evaluate whether the proposed response is safe and sufficiently
supported by the available information.

Customer ticket:
{ticket_message}

Predicted category:
{category}

Proposed response:
{response}

Return exactly two lines:

DECISION: resolve OR escalate
CONFIDENCE: a number between 0 and 1

Use these rules:
- resolve if the response directly addresses the ticket and is
  supported by the available information.
- escalate if important information is missing, the issue is unclear,
  or the response may require human judgment.
"""

    for attempt in range(3):
        try:
            result = client.models.generate_content(
                model="gemini-3.1-flash-lite",
                contents=prompt,
            )

            lines = [
                line.strip()
                for line in result.text.strip().splitlines()
                if line.strip()
            ]

            decision = "escalate"
            confidence = 0.0

            for line in lines:
                if line.upper().startswith("DECISION:"):
                    value = line.split(":", 1)[1].strip().lower()

                    if value in {"resolve", "escalate"}:
                        decision = value

                elif line.upper().startswith("CONFIDENCE:"):
                    try:
                        confidence = float(
                            line.split(":", 1)[1].strip()
                        )
                    except ValueError:
                        confidence = 0.0

            confidence = max(0.0, min(1.0, confidence))

            return {
                "decision": decision,
                "confidence": confidence,
            }

        except Exception as error:
            print(f"Router attempt {attempt + 1} failed: {error}")

            if attempt < 2:
                time.sleep(2)

    return {
        "decision": "escalate",
        "confidence": 0.0,
    }
