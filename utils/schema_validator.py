# backend/utils/schema_validator.py
from pydantic import ValidationError
from models.paper import Paper

__all__ = ["validate_paper"]

def validate_paper(data: dict) -> Paper:
    """
    Validate JSON từ OpenAI -> Paper (Pydantic v2).
    Nếu lỗi sẽ raise ValidationError cho FastAPI xử lý.
    """
    try:
        return Paper.model_validate(data)
    except ValidationError as e:
        # Có thể log ra file nếu cần
        raise e
