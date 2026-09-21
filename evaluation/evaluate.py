import json
from pathlib import Path

from app.agents.classifier import classify_ticket
from app.core.models import SupportTicket


DATA_PATH = Path("data/evaluation_dataset.json")


def load_dataset():
    with open(DATA_PATH, "r", encoding="utf-8") as file:
        return json.load(file)


def evaluate_classification():
    dataset = load_dataset()

    correct = 0
    total = len(dataset)

    results = []

    for item in dataset:
        ticket = SupportTicket(
            ticket_id=item["ticket_id"],
            customer_message=item["customer_message"],
        )

        result = classify_ticket(ticket)

        predicted = result.category
        expected = item["expected_category"]

        is_correct = predicted == expected

        if is_correct:
            correct += 1

        results.append(
            {
                "ticket_id": item["ticket_id"],
                "expected": expected,
                "predicted": predicted,
                "correct": is_correct,
            }
        )

        print(
            f"{item['ticket_id']}: "
            f"expected={expected}, "
            f"predicted={predicted}, "
            f"correct={is_correct}"
        )

    accuracy = (correct / total) * 100 if total else 0

    print("\n===== Evaluation Results =====")
    print(f"Total tickets: {total}")
    print(f"Correct classifications: {correct}")
    print(f"Classification accuracy: {accuracy:.2f}%")

    return {
        "total": total,
        "correct": correct,
        "accuracy": accuracy,
        "results": results,
    }


if __name__ == "__main__":
    evaluate_classification()