from typing import Optional

from fastapi import FastAPI
from fastapi.responses import JSONResponse

from app.models import OrchestrationRequest, OrchestrationResponse
from app.orchestrator import orchestrate_request

app = FastAPI(title="TM1 Agentic Orchestrator", version="0.1.0")


@app.get("/health")
def health_check() -> dict:
    return {"status": "ok", "service": "tm1-agentic-orchestrator"}


@app.post("/api/orchestrate", response_model=OrchestrationResponse)
def orchestrate(question_request: OrchestrationRequest) -> OrchestrationResponse:
    result = orchestrate_request(question_request.question)

    return OrchestrationResponse(
        classification=result["classification"],
        output_type=result["output_type"],
        summary=result["summary"],
        reasoning=result["reasoning"],
        generated_code=result["generated_code"],
        impact_summary=result["impact_summary"],
        recommended_approach=result["recommended_approach"],
    )


@app.exception_handler(Exception)
async def handler(_: Exception):
    return JSONResponse(status_code=500, content={"detail": "Unexpected server error"})
