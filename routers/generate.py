# routers/generate.py
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, ValidationError
from services.prompt_builder import MASTER_SYSTEM_PROMPT, build_user_prompt
from services.openai_client import call_openai_as_json
from utils.schema_validator import validate_paper
import logging, traceback, os
from utils.scoring import normalize_scores_weighted
router = APIRouter()
logger = logging.getLogger("uvicorn.error")
DEBUG = os.getenv("DEBUG", "false").lower() in ("1","true","yes")

class GenerateRequest(BaseModel):
    grade: int
    focus: list[str] | str
    counts: dict[str, int]
    difficulty: str
    theme: str | None = None
    teacher_pack_summary: str | None = None

@router.post("/generate")
def generate_paper(payload: GenerateRequest):
    system_prompt = MASTER_SYSTEM_PROMPT
    user_prompt = build_user_prompt(
        grade=payload.grade,
        focus=payload.focus,
        counts=payload.counts,
        difficulty=payload.difficulty,
        theme=payload.theme,
        teacher_pack_summary=payload.teacher_pack_summary,
    )
    try:
        raw = call_openai_as_json(system_prompt, user_prompt)
        paper = validate_paper(raw)

        # ✅ Áp dụng phân bổ điểm thông minh
        paper_dict = paper.model_dump()
        paper_dict = normalize_scores_weighted(paper_dict, total_score=10.0)
        return paper_dict

    except Exception as e:
        raise HTTPException(status_code=400, detail=f"LLM call failed: {e}")

    try:
        paper = validate_paper(raw)
    except ValidationError as ve:
        logger.error("Model output invalid: %s", ve)
        detail = {"message": "Model output invalid", "errors": ve.errors()}
        if DEBUG:
            detail["raw"] = raw  # chỉ kèm khi DEBUG=true
        raise HTTPException(status_code=422, detail=detail)

    return paper
