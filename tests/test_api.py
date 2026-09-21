from fastapi.testclient import TestClient

from app.api.main import app


client = TestClient(app)


def test_health_check():
    response = client.get("/")

    assert response.status_code == 200

    assert response.json() == {
        "status": "running",
        "service": "SupportPilot AI",
    }


def test_process_ticket():
    response = client.post(
        "/tickets",
        json={
            "ticket_id": "TEST001",
            "customer_message": "I forgot my password",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["ticket_id"] == "TEST001"
    assert data["category"] == "account"
    assert data["response"]
    assert data["decision"] in {"resolve", "escalate"}
    assert 0.0 <= data["confidence"] <= 1.0
    assert data["final_status"] in {
        "resolved",
        "escalated_to_human",
    }