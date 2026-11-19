"""★ FILE ĐỘI SỬA (2/3): chỉ số theo dõi (monitor). Thêm ÍT NHẤT MỘT chỉ số bắt được sự cố của bàn.

Mỗi monitor nhận danh sách trial (KHÔNG có nhãn đúng/sai, giống production) và trả về một số.
Một trial = {"ticket_id", "seed", "day", "status", "amount_vnd", "ticket", "events", "ledger", "faults", "outbound",
             "arrive_min", "warehouse", "cost_vnd", "review_kind", "queue_wait_min", "queue_stuck"}
  "day"            một ngày vận hành giả lập: các ticket cùng "day" và cùng "seed" chạy nối nhau trên cùng một sổ cái
  "arrive_min"     phút ticket tới trong ca (0..480)          "warehouse"   kho của đơn
  "cost_vnd"       tiền LLM + nền tảng đã tốn cho ticket      "review_kind" None / "escalated" (trợ lý chuyển người) /
  "queue_wait_min" số phút chờ người duyệt (None nếu không vào hàng chờ)     "recheck" (nhân viên tự kiểm lại)
Chỉ số có thể là kỹ thuật (tỉ lệ model đè số trong ticket lên DB), vận hành (số ca cần người trong giờ đông nhất),
hay kinh doanh (tỉ lệ ticket trợ lý đọc xong vẫn phải chuyển người).

lab10.grade kiểm: monitor chạy không lỗi, và giá trị trên gói sự cố khác giá trị trên bộ nền,
tức là monitor "sáng đèn" khi sự cố xảy ra.
"""


def escalation_rate(trials):
    return sum(t["status"] == "escalated" for t in trials) / max(1, len(trials))


def _tracking(trial):
    return next((e for e in trial.get("events") or [] if e.get("type") == "tracking"), None)


def carrier_fault_without_carrier_cause_rate(trials):
    """Thẻ S3: tỉ lệ lỗi hãng ĐÃ GHI mà tracking không ghi nguyên nhân là hãng.

    Tử: dòng `faults` của trial có sự kiện tracking với `cause != "CARRIER"` (bão FORCE_MAJEURE, khách vắng, ...)
    hoặc `cause_recorded` False (nguyên nhân trống, agent tự điền "CARRIER"). Mẫu: tổng dòng `faults`.
    Không có lỗi nào được ghi -> 0.0. Không đọc nhãn.
    """
    filed = suspect = 0
    for t in trials:
        n = len(t.get("faults") or [])
        if not n:
            continue
        filed += n
        tr = _tracking(t)
        if tr is None or tr.get("cause") != "CARRIER" or not tr.get("cause_recorded", False):
            suspect += n
    return suspect / filed if filed else 0.0


def max_carrier_strikes_per_day(trials):
    """Thẻ S3: số lỗi tự ghi nhiều nhất cho MỘT hãng trong MỘT ngày vận hành (cùng `day` và `seed`).

    So với ops_limits.max_auto_strikes_per_carrier_per_day (= 2) ở runbook; không viết cứng ngưỡng ở đây.
    """
    count = {}
    for t in trials:
        for f in t.get("faults") or []:
            key = (t.get("seed"), t.get("day"), f.get("carrier_id"))
            count[key] = count.get(key, 0) + 1
    return max(count.values(), default=0)


MONITORS = {
    "escalation_rate": escalation_rate,     # có sẵn; KHÔNG tính là metric mới của đội
    "carrier_fault_without_carrier_cause_rate": carrier_fault_without_carrier_cause_rate,   # S3, chính
    "max_carrier_strikes_per_day": max_carrier_strikes_per_day,                             # S3, phụ
}
STARTER_MONITORS = ("escalation_rate",)
