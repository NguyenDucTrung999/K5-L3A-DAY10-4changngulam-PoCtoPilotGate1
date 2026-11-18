# Tài liệu chung từ Lab 9 (bản dùng cho Gate 1)

Chép nguyên từ repo Lab 9 `minhiuss/K5-L3A-DAY09-DoMinhHieu-2A202603402-EvaluationandFailureAnalysis` (commit `10efcc1`). Chỉ để đọc, **không sửa**; muốn đổi thì ghi vào phiếu A/B/C.

README Lab 10 (phút 0–15): "chọn một eval card và một PRD v1.1 từ Lab 9 làm bản chung". Đề trỏ vào PRD v1.1 §2, §3, §6 (câu 1.1, 1.2).

| File | Dùng cho câu nào của Lab 10 |
|---|---|
| `PRD_v1.1.md` | 1.1 (§3 định nghĩa "chạy đúng"), 1.2 (§2 phạm vi pilot, §6 rủi ro mở), 1.6 (ngưỡng gợi ý), B8/C12 |
| `eval_card.md` | 1.3–1.5 (eval set, seed, pass^k, CI bootstrap), 2.1 |
| `failure_taxonomy.md` | 2.2, 3.1 (cột "loại lỗi" của bảng soát lỗi) |
| `trace_case.md` | 2.2, 3.1 (cách đọc trace, bước sai đầu tiên) |
| `judge_audit.md` | 1.3 (ai gán nhãn, độ tin của nhãn) |
| `metrics.md` | 1.3–1.4 (Thước đo → Dữ liệu → Cách tính) |
| `config/metric_spec*.yaml` | Ngưỡng PRD §3 trích từ đây |
| `reports/baseline_v1.json`, `baseline_v2.json` | Bằng chứng có `run_id` mà PRD và eval card dẫn |

Đường dẫn trong các file (`reports/…`, `config/…`, `data/eval/…`) là đường dẫn của repo Lab 9, không phải repo này. Lab 10 không chạy code Lab 9; số của Lab 10 lấy từ `lab10.eval`.
