# SupportPilot AI

**SupportPilot AI** is an agentic AI system that automates customer support ticket processing.

The system classifies incoming support tickets, searches similar historical tickets using semantic search, generates a response using Gemini, and then decides whether the ticket can be automatically resolved or should be escalated to a human agent.

---

## Architecture

```text
                         CUSTOMER TICKET
                               |
                               v
                    +----------------------+
                    |   Ticket Classifier  |
                    |      Gemini API      |
                    +----------+-----------+
                               |
                               v
                    +----------------------+
                    |       ChromaDB       |
                    |  Semantic Retrieval  |
                    | Similar Past Tickets |
                    +----------+-----------+
                               |
                               v
                    +----------------------+
                    |    Response Agent    |
                    |      Gemini API      |
                    +----------+-----------+
                               |
                               v
                    +----------------------+
                    |    Quality Router    |
                    |  Resolve / Escalate  |
                    +----------+-----------+
                               |
                     +---------+---------+
                     |                   |
                     v                   v
              +-------------+     +-------------+
              |   Resolve   |     |   Escalate |
              |    Ticket   |     |  to Human  |
              +-------------+     +-------------+
```

### How the Architecture Works

1. **Ticket Classification**

   * The customer ticket is sent to the Gemini API.
   * The classifier assigns the ticket to a category such as billing, account, technical, shipping, or refund.

2. **Semantic Retrieval**

   * ChromaDB stores historical support cases.
   * The customer's message is compared with previous tickets using semantic similarity.
   * The most relevant support cases are retrieved.

3. **Response Generation**

   * The retrieved support cases are provided as context to the Gemini response agent.
   * The agent generates a clear and professional response.

4. **Quality Routing**

   * A quality-control agent evaluates the generated response.
   * The system decides whether the ticket should be resolved automatically or escalated to a human.

5. **Final Status**

   * `resolved` → the ticket can be handled automatically.
   * `escalated_to_human` → the ticket requires human assistance.

---

## Workflow

```text
START
  |
  v
Classify Ticket
  |
  v
Retrieve Similar Tickets
  |
  v
Generate Response
  |
  v
Quality Router
  |
  +-----------> Resolve -----------> END
  |
  +-----------> Escalate ----------> END
```

---

## Technology Stack

* **Python 3.12**
* **LangGraph** — agentic workflow orchestration
* **Google Gemini API** — classification, response generation, and routing
* **ChromaDB** — semantic vector search
* **FastAPI** — REST API
* **Pydantic** — data validation
* **Pytest** — automated testing
* **Docker** — containerization
* **GitHub Codespaces** — cloud development environment

---

## Project Structure

```text
Supportsystem-AI/
│
├── app/
│   ├── agents/
│   │   ├── classifier.py
│   │   ├── responder.py
│   │   └── router.py
│   │
│   ├── api/
│   │   └── main.py
│   │
│   ├── core/
│   │   └── models.py
│   │
│   ├── rag/
│   │   └── vector_store.py
│   │
│   └── graph.py
│
├── data/
│   ├── knowledge_base.json
│   └── evaluation_dataset.json
│
├── evaluation/
│   └── evaluate.py
│
├── tests/
│   ├── test_api.py
│   ├── test_classifier.py
│   ├── test_models.py
│   └── test_routing.py
│
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
```

---

# How to Run

## Prerequisites

Make sure you have:

* Python 3.12 or newer
* Git
* A Gemini API key

---

## 1. Clone the Repository

```bash
git clone https://github.com/ayushsingh1524/Supportsystem-AI.git
cd Supportsystem-AI
```

---

## 2. Create a Virtual Environment

### macOS / Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### Windows

```bash
python -m venv .venv
.venv\Scripts\activate
```

---

## 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 4. Configure the Gemini API Key

Create a `.env` file in the project root:

```env
GEMINI_API_KEY=your_gemini_api_key_here
```

Do not commit the `.env` file to GitHub.

The project already includes `.gitignore` rules to prevent the API key from being committed.

---

## 5. Start the FastAPI Server

Run:

```bash
uvicorn app.api.main:app --reload
```

The API will start at:

```text
http://localhost:8000
```

You should see something similar to:

```text
Uvicorn running on http://127.0.0.1:8000
```

---

## 6. Check the API

Open this URL in your browser:

```text
http://localhost:8000
```

Expected response:

```json
{
  "status": "running",
  "service": "SupportPilot AI"
}
```

---

## 7. Process a Support Ticket

Open another terminal while the FastAPI server is running.

Run:

```bash
curl -X POST http://localhost:8000/tickets \
-H "Content-Type: application/json" \
-d '{
  "ticket_id": "T001",
  "customer_message": "I forgot my password"
}'
```

The system will:

```text
Customer Ticket
      |
      v
Classification
      |
      v
ChromaDB Retrieval
      |
      v
Response Generation
      |
      v
Quality Routing
      |
      v
Final Decision
```

Example response:

```json
{
  "ticket_id": "T001",
  "category": "account",
  "response": "Use the password reset option on the login page and follow the instructions sent to your registered email.",
  "decision": "resolve",
  "confidence": 0.95,
  "final_status": "resolved"
}
```

The exact response and confidence may vary because the system uses an LLM.

---

# API Endpoint

## POST `/tickets`

Processes a customer support ticket.

### Request

```json
{
  "ticket_id": "T001",
  "customer_message": "My payment failed"
}
```

### Response

```json
{
  "ticket_id": "T001",
  "category": "billing",
  "response": "Check that your payment method has sufficient funds and that the card details are correct.",
  "decision": "resolve",
  "confidence": 0.95,
  "final_status": "resolved"
}
```

---

# Run Tests

Make sure the virtual environment is activated.

Run:

```bash
pytest -v
```

The tests cover:

* Support ticket data models
* Ticket classification
* Resolve/escalate routing
* FastAPI API endpoints

---

# Run Evaluation

The project includes a labeled evaluation dataset for measuring classification performance.

Run:

```bash
python evaluation/evaluate.py
```

The evaluation script reports:

```text
===== Evaluation Results =====
Total tickets: 20
Correct classifications: XX
Classification accuracy: XX.XX%
```

The reported accuracy should always come from an actual evaluation run rather than being manually assumed.

---

# Run with Docker

Docker can also be used to run the application.

First make sure Docker is installed and running.

Set the Gemini API key:

```bash
export GEMINI_API_KEY="your_gemini_api_key_here"
```

Then run:

```bash
docker compose up --build
```

The API will be available at:

```text
http://localhost:8000
```

To stop the application:

```bash
docker compose down
```

---

# Supported Categories

The classifier currently supports:

```text
billing
technical
account
shipping
refund
other
```

---

# Key Features

### AI Ticket Classification

Automatically identifies the category of incoming customer support tickets.

### Retrieval-Augmented Generation

Uses ChromaDB to retrieve similar historical support tickets before generating a response.

### Agentic Workflow

LangGraph coordinates multiple stages:

```text
Classification
      ↓
Retrieval
      ↓
Response Generation
      ↓
Quality Control
      ↓
Resolve / Escalate
```

### Human Escalation

Tickets that cannot be safely handled automatically can be routed to human support.

### REST API

FastAPI exposes the support automation workflow through an HTTP API.

### Automated Testing

Pytest tests the main application components and API behavior.

---

# Evaluation

The project contains an evaluation dataset with labeled support tickets.

Current evaluation focuses on:

* Classification accuracy

The evaluation framework can be extended to measure:

* Routing accuracy
* Escalation accuracy
* Response quality
* Retrieval quality
* Automation rate
* Manual-review reduction

Any performance metrics reported for this project should be based on reproducible evaluation results.

---

# Security

* API keys are stored using environment variables.
* `.env` is excluded from Git.
* API keys should never be committed to the repository.
* `.chroma/` is excluded from Git because it contains locally generated vector-store data.

---

# Future Improvements

* Add a production database for ticket storage.
* Add authentication and authorization.
* Add a support-agent dashboard.
* Add more evaluation examples.
* Add deterministic confidence scoring.
* Improve response-quality evaluation.
* Add monitoring and logging.
* Deploy the API to a cloud platform.

---

# License

This project is intended for educational and portfolio purposes.
