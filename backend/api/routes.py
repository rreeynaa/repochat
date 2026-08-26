from fastapi import APIRouter, HTTPException

from backend.api.schemas import (
    AskRequest,
    AskResponse,
    IndexRequest,
    IndexResponse,
    StatusResponse,
)
from backend.config import settings
from backend.rag.pipeline import RagPipeline

router = APIRouter()

# A single pipeline instance per process: this keeps the (slow-to-load)
# embedding model and the vector DB connection warm across requests.
_pipeline = RagPipeline()


@router.post("/index", response_model=IndexResponse)
def index_repository(request: IndexRequest) -> IndexResponse:
    try:
        summary = _pipeline.index_repository(request.repo_path, request.repo_name)
    except (FileNotFoundError, NotADirectoryError) as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    return IndexResponse(**summary)


@router.post("/ask", response_model=AskResponse)
def ask_question(request: AskRequest) -> AskResponse:
    config_problems = settings.validate()
    if config_problems:
        raise HTTPException(status_code=400, detail="; ".join(config_problems))

    result = _pipeline.answer_question(
        question=request.question,
        repo_name=request.repo_name,
        top_k=request.top_k,
    )
    return AskResponse(
        question=result["question"],
        answer=result["answer"],
        citations=result["citations"],
    )


@router.get("/status", response_model=StatusResponse)
def get_status() -> StatusResponse:
    status = _pipeline.status()
    return StatusResponse(
        total_chunks_indexed=status["total_chunks_indexed"],
        config_warnings=settings.validate(),
    )
