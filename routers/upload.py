from fastapi import APIRouter, UploadFile, File, HTTPException
from models.upload import UploadSummary

router = APIRouter()

@router.post("/upload-teacher-pack", response_model=UploadSummary)
async def upload_teacher_pack(file: UploadFile = File(...)):
    """
    MVP: chưa OCR, chỉ đọc text & trả về 1 summary giả để nhét vào prompt.
    Bạn có thể thay bằng pipeline RAG sau.
    """
    if not file.filename:
        raise HTTPException(400, "No file uploaded")

    content = await file.read()
    text_preview = content[:500].decode("utf-8", errors="ignore")

    summary = (
        "Gói đề giáo viên: ưu tiên MCQ 4 lựa chọn, chủ điểm trường lớp, văn phong thân thiện. "
        "Ví dụ nội dung: " + text_preview.replace("\n", " ")[:200]
    )

    return UploadSummary(summary=summary)
