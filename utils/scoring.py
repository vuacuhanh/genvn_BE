def normalize_scores_weighted(paper: dict, total_score: float = 10.0) -> dict:
    """
    Phân bổ điểm có trọng số:
      - Trắc nghiệm (mcq, short_answer, fill_in_blank): 50% tổng điểm
      - Viết (writing): 50% tổng điểm
    """
    items = paper.get("items", [])
    if not items:
        return paper

    # Tách nhóm
    trắc_nghiệm = [i for i in items if i.get("type") in ["mcq", "short_answer", "fill_in_blank"]]
    viết = [i for i in items if i.get("type") == "writing"]

    # Nếu không có writing
    if not viết:
        base_score = total_score / len(items)
        for i in items:
            i["score"] = round(base_score, 2)
        return paper

    # Nếu không có trắc nghiệm
    if not trắc_nghiệm:
        base_score = total_score / len(items)
        for i in items:
            i["score"] = round(base_score, 2)
        return paper

    # ✅ Có cả hai nhóm
    # Phân bổ 50/50
    total_mcq_score = total_score * 0.5
    total_writing_score = total_score * 0.5

    mcq_score_each = total_mcq_score / len(trắc_nghiệm)
    writing_score_each = total_writing_score / len(viết)

    mcq_score_each = round(mcq_score_each, 2)
    writing_score_each = round(writing_score_each, 2)

    # Gán điểm
    for i in trắc_nghiệm:
        i["score"] = mcq_score_each
    for i in viết:
        i["score"] = writing_score_each

    # Nếu làm tròn khiến tổng lệch → chỉnh câu cuối
    current_total = sum(i.get("score", 0) for i in items)
    diff = round(total_score - current_total, 2)
    if abs(diff) > 0.01:
        items[-1]["score"] = round(items[-1].get("score", 0) + diff, 2)

    return paper
