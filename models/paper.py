# models/paper.py
from pydantic import BaseModel, Field
from typing import List, Literal, Optional, Any

class Counts(BaseModel):
    mcq: int = 0
    short_answer: int = 0
    writing: int = 0

class Meta(BaseModel):
    grade: int = Field(ge=1, le=5)
    focus: List[Literal["danh_tu", "dong_tu","tinh_tu","trang_tu"]]
    difficulty: Literal["easy", "medium", "hard"]
    counts: Counts                      # ← dùng model thay vì dict
    theme: Optional[str] = None
    estimated_time_minutes: int = 0     # ← tránh vỡ nếu model không trả

class BaseItem(BaseModel):
    id: str
    type: str
    prompt: str
    score: float
    provenance: Literal["generated", "inspired_by_upload"]
    rationale: Optional[str] = None
    tags: Optional[List[str]] = None

class Paper(BaseModel):
    meta: Meta
    items: List[Any]
    rubrics: dict | None = None
    answer_sheet: List[dict]