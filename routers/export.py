#D:\vn-primary-generator\backend\routers\export.py
from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse, PlainTextResponse
from pydantic import BaseModel
from services.exporter import paper_to_docx, paper_to_txt, paper_to_pdf
import io

router = APIRouter()

class ExportPayload(BaseModel):
    paper: dict
    format: str  # "docx" | "txt" | "pdf"

@router.post("/export")
def export_paper(payload: ExportPayload):
    fmt = payload.format.lower()
    if fmt == "docx":
        data = paper_to_docx(payload.paper)
        return StreamingResponse(
            io.BytesIO(data),
            media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            headers={"Content-Disposition": "attachment; filename=de-tieng-viet.docx"},
        )
    elif fmt == "txt":
        txt = paper_to_txt(payload.paper)
        return PlainTextResponse(
            txt,
            headers={"Content-Disposition": "attachment; filename=de-tieng-viet.txt"},
        )
    elif fmt == "pdf":
        pdf_data = paper_to_pdf(payload.paper)
        return StreamingResponse(
            io.BytesIO(pdf_data),
            media_type="application/pdf",
            headers={"Content-Disposition": "attachment; filename=de-tieng-viet.pdf"},
        )
    else:
        raise HTTPException(400, "Định dạng không hỗ trợ (chỉ docx, txt hoặc pdf)")
