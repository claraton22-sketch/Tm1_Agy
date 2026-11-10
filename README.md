# TM1 Agentic Orchestrator

This repository contains a starter agentic orchestrator for TM1 use cases. It receives a user question and classifies the request into one of the following modes:

- code generation
- impact analysis
- approach finalization
- clarification needed

The architecture is intentionally simple and extensible so it can evolve into a richer TM1 copilot.

## Features

- Request classification via keyword-based orchestration logic
- TM1 code generation template engine
- Impact analysis summaries for cubes, dimensions, and processes
- Approach recommendation and decision framing
- FastAPI-based API endpoint for orchestration

## Project structure

- `app/main.py` - API entry point
- `app/models.py` - request/response schemas
- `app/orchestrator.py` - classification and workflow orchestration
- `app/tm1_templates.py` - stubbed TM1 code generation templates

## Quick start

1. Create a virtual environment
2. Install dependencies
3. Run the service

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

## Example request

```bash
curl -X POST http://127.0.0.1:8000/api/orchestrate \
  -H "Content-Type: application/json" \
  -d '{"question":"Generate a TM1 process to load data into Sales cube from staging file"}'
```

## Example response

```json
{
  "classification": "code_generation",
  "output_type": "tm1_process",
  "summary": "The request is to generate TM1 code.",
  "generated_code": "...",
  "impact_summary": null,
  "recommended_approach": null
}
```

## Notes

This is a foundation for a broader TM1 assistant. In a production system, you would replace the simple keyword classifier with an LLM-based router or a policy engine tied to your TM1 standards and metadata model.
