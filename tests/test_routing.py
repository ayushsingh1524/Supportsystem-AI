from app.graph import route_decision


def test_resolve_route():
    state = {
        "decision": "resolve",
    }

    assert route_decision(state) == "resolve"


def test_escalate_route():
    state = {
        "decision": "escalate",
    }

    assert route_decision(state) == "escalate"


def test_unknown_decision_escalates():
    state = {
        "decision": "unknown",
    }

    assert route_decision(state) == "escalate"