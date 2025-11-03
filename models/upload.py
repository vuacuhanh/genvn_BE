from pydantic import BaseModel

class UploadSummary(BaseModel):
    summary: str
