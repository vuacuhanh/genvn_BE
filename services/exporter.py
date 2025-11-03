from typing import Dict, Any
import io

print("LOADED exporter.py clean")

# -------------------- DOCX EXPORT --------------------
def paper_to_docx(paper: Dict[str, Any]) -> bytes:
    try:
        from docx import Document
    except ImportError as e:
        raise RuntimeError("Thiếu dependency `python-docx`. Cài: pip install python-docx") from e

    doc = Document()
    meta = paper.get("meta", {})
    doc.add_heading(f"ĐỀ TIẾNG VIỆT - LỚP {meta.get('grade','')}", level=1)
    doc.add_paragraph(f"Độ khó: {meta.get('difficulty','')}")
    doc.add_paragraph(f"Chủ điểm: {meta.get('theme','')}")
    doc.add_paragraph(" ")

    items = paper.get("items", [])
    for idx, item in enumerate(items, start=1):
        p = doc.add_paragraph()
        run = p.add_run(f"Câu {idx} ({item.get('score',1)}đ) [{item.get('type')}]: ")
        run.bold = True
        p.add_run(item.get("prompt",""))
        if item.get("type") == "mcq":
            opts = item.get("options", [])
            for opt_label, opt in zip(["A", "B", "C", "D"], opts):
                doc.add_paragraph(f"{opt_label}. {opt}", style="List Bullet")
        doc.add_paragraph(" ")

    doc.add_page_break()
    doc.add_heading("ĐÁP ÁN", level=2)
    for ans in paper.get("answer_sheet", []):
        doc.add_paragraph(f"{ans.get('id')}: {ans.get('key')}")

    f = io.BytesIO()
    doc.save(f)
    f.seek(0)
    return f.read()

# -------------------- TXT EXPORT --------------------
def paper_to_txt(paper: Dict[str, Any]) -> str:
    lines = []
    meta = paper.get("meta", {})
    lines.append(f"DE TIENG VIET - LOP {meta.get('grade','')}")
    lines.append(f"Do kho: {meta.get('difficulty','')}")
    lines.append("")
    for idx, item in enumerate(paper.get("items", []), start=1):
        lines.append(f"Cau {idx} ({item.get('score',1)}d) [{item.get('type')}]: {item.get('prompt','')}")
        if item.get("type") == "mcq":
            for opt_label, opt in zip(["A","B","C","D"], item.get("options", [])):
                lines.append(f"  {opt_label}. {opt}")
        lines.append("")
    lines.append("Dap an:")
    for ans in paper.get("answer_sheet", []):
        lines.append(f"- {ans.get('id')}: {ans.get('key')}")
    return "\n".join(lines)

# -------------------- PDF EXPORT --------------------
def paper_to_pdf(paper: Dict[str, Any]) -> bytes:
    try:
        from reportlab.lib.pagesizes import A4
        from reportlab.lib.styles import getSampleStyleSheet
        from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
        from reportlab.lib.units import cm
    except ImportError as e:
        raise RuntimeError("Thiếu dependency `reportlab`. Cài: pip install reportlab") from e

    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4, leftMargin=2 * cm, rightMargin=2 * cm)
    styles = getSampleStyleSheet()
    story = []

    meta = paper.get("meta", {})
    story.append(Paragraph(f"<b>ĐỀ TIẾNG VIỆT - LỚP {meta.get('grade','')}</b>", styles["Title"]))
    story.append(Paragraph(f"Độ khó: {meta.get('difficulty','')} | Chủ điểm: {meta.get('theme','')}", styles["Normal"]))
    story.append(Spacer(1, 12))

    for idx, item in enumerate(paper.get("items", []), start=1):
        story.append(Paragraph(
            f"<b>Câu {idx}</b> ({item.get('score',1)}đ) [{item.get('type')}]: {item.get('prompt','')}",
            styles["Normal"]
        ))
        if item.get("type") == "mcq":
            opts = item.get("options", [])
            for opt_label, opt in zip(["A", "B", "C", "D"], opts):
                story.append(Paragraph(f"{opt_label}. {opt}", styles["Normal"]))
        story.append(Spacer(1, 8))

    story.append(Spacer(1, 16))
    story.append(Paragraph("<b>ĐÁP ÁN</b>", styles["Heading2"]))
    for ans in paper.get("answer_sheet", []):
        story.append(Paragraph(f"{ans.get('id')}: {ans.get('key')}", styles["Normal"]))

    doc.build(story)
    pdf_data = buffer.getvalue()
    buffer.close()
    return pdf_data
