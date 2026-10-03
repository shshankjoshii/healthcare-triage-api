# Healthcare Triage API

Educational demo of a small FastAPI service that classifies a patient query and returns a simulated next action. Classification uses deterministic Python keyword matching inside a LangGraph workflow. **This is not a medical diagnosis system and must not be used for real clinical decisions.**

## Architecture / workflow

```
Client JSON
    |
    v
POST /api/v1/query  (FastAPI + Pydantic)
    |
    v
LangGraph: START -> triage -> action -> END
    |
    v
JSON: patient_id, status, action
```

1. **triage** inspects `query` and sets `status` to exactly one of `Emergency`, `Routine`, or `Admin`.
2. **action** maps that status to a simulated next step:
   - Emergency → Seek immediate emergency medical care
   - Routine → Route to doctor
   - Admin → Route to administrative support

Emergency keywords are checked first, then admin keywords. Anything else is Routine.

## Technologies used

- Python 3.12
- FastAPI
- Pydantic
- LangGraph
- Uvicorn
- Docker

No paid or external LLM API is used.

## Installation

Requires Python 3.12.

```bash
python -m venv .venv
```

Windows (PowerShell):

```powershell
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

macOS / Linux:

```bash
source .venv/bin/activate
pip install -r requirements.txt
```

## How to run locally

From the project root:

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Open API docs at `http://localhost:8000/docs`.

## API endpoint

`POST /api/v1/query`

Request body:

```json
{
  "patient_id": "123",
  "query": "String"
}
```

Response body:

```json
{
  "patient_id": "123",
  "status": "Emergency | Routine | Admin",
  "action": "..."
}
```

## Example request / response

Emergency:

```bash
curl -X POST http://localhost:8000/api/v1/query \
  -H "Content-Type: application/json" \
  -d "{\"patient_id\": \"123\", \"query\": \"severe chest pain and difficulty breathing\"}"
```

```json
{
  "patient_id": "123",
  "status": "Emergency",
  "action": "Seek immediate emergency medical care"
}
```

Admin:

```bash
curl -X POST http://localhost:8000/api/v1/query \
  -H "Content-Type: application/json" \
  -d "{\"patient_id\": \"123\", \"query\": \"I need to reschedule my appointment\"}"
```

```json
{
  "patient_id": "123",
  "status": "Admin",
  "action": "Route to administrative support"
}
```

Routine:

```bash
curl -X POST http://localhost:8000/api/v1/query \
  -H "Content-Type: application/json" \
  -d "{\"patient_id\": \"123\", \"query\": \"I have a mild headache for two days\"}"
```

```json
{
  "patient_id": "123",
  "status": "Routine",
  "action": "Route to doctor"
}
```

## How to run with Docker

```bash
docker build -t healthcare-triage-api .
docker run --rm -p 8000:8000 healthcare-triage-api
```

Then call `http://localhost:8000/api/v1/query` the same way as locally.

## Disclaimer

This project is a **demo / educational** triage workflow. Keyword matching is simplified on purpose. It does not provide medical advice, diagnosis, or emergency services.
