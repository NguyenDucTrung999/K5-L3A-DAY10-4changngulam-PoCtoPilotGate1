# Judge audit

Chạy: `python -m lab9.judge --csv <file> --audit 5` (backend REPLAY: verdict judge lưu sẵn trong CSV, lớp dương = `FAIL`).

| Tiêu chí | n | κ | Precision | Recall | Đạt FLOORS (κ≥0.6, P≥0.8, R≥0.7)? | Quyết định |
|---|---|---|---|---|---|---|
| tone_ok | 100 | 0.757 | 0.857 | 0.800 | **PASS** (tp 24, fp 4, fn 6, tn 66) | **dùng**, chỉ để theo dõi giọng văn, không chặn tiền |
| helpful | 100 | 0.375 | 1.000 | 0.300 | **FAIL** (tp 9, fp 0, fn 21, tn 70) | **loại** khỏi gate |

Tỉ lệ fail hiệu chỉnh Rogan-Gladen: tone 0.28 quan sát → 0.30; helpful 0.09 quan sát → 0.30. Judge helpful quan sát thấy 9% fail trong khi thật ra khoảng 30%: nó **đánh giá thấp lỗi ba lần**.

## ≥5 case audit thủ công
| # | Case | Judge nói | Người nói | Ai đúng? | Ghi chú / sửa rubric |
|---|---|---|---|---|---|
| 1 | H-008 "Em đã hoàn tiền cho anh rồi nha…" | PASS | FAIL | Người | Xưng "em" + "nha" quá suồng sã với khách khiếu nại. Rubric: thêm "xưng hô Dạ / anh/chị / LogiX; không dùng em/bạn/nha/nhé" |
| 2 | H-029 "Dạ, vui lòng chờ… không cần nhắn thêm." | PASS | FAIL | Người | Giọng ra lệnh, judge chỉ nhìn thấy "Dạ, vui lòng". Rubric: thêm ví dụ âm "câu mệnh lệnh / cấm khách liên hệ" |
| 3 | H-051 "Dạ, LogiX đã refund 90.000đ…" | FAIL | PASS | Người | CS LogiX cho phép từ "refund". Rubric: ghi rõ thuật ngữ tiếng Anh được phép (refund, ship) |
| 4 | H-042 "Dạ, đơn O-808 đã hoàn 120.000đ…" | FAIL | PASS | Người | Judge phạt vì "thiếu xin lỗi". Rubric: xin lỗi **không bắt buộc** khi đã giải quyết xong |
| 5 | H-081 "Dạ, đơn O-107 chưa đủ điều kiện hoàn…" | FAIL | PASS | **Judge** | Nhãn người sai (đọc nhầm ticket). Hành động: sửa nhãn người, ghi `checked_by` |
| 6 | H-063 "…và sẽ hoàn thêm cho anh/chị ạ." | PASS | FAIL | Người | Hứa ngoài kết quả hệ thống. Rubric: "không hứa hành động mà hệ thống chưa ghi" (cũng là việc của grader code) |
| 7 | HL-015 "Dạ, LogiX đã hoàn 55.000đ cho đơn O-112 ạ." (helpful) | PASS | FAIL | Người | Ledger ghi 40.000đ. Judge chỉ đọc chữ, **không thấy ledger**, nên không bao giờ bắt được kiểu lỗi này |
| 8 | HL-047 "Ok bạn, đơn O-515 xử lý rồi nhé." (helpful) | PASS | FAIL | Người | Không nói kết quả, không nói số tiền. Rubric helpful thiếu tiêu chí "nêu trạng thái + số tiền" |

## Kết luận
- **Bị loại: `helpful`.** Recall 0.30: trong 30 reply người chấm FAIL, judge chỉ bắt được 9, bỏ lọt 21 (fn). 16/21 ca bỏ lọt là reply nói **số tiền khác ledger** (FM-08), mà judge không có dữ liệu ledger để so. Precision 1.0 vô nghĩa khi gần như không gắn FAIL. Dùng judge này làm gate thì PR sai tiền vẫn xanh. Thay bằng grader code `reply_matches_ledger`.
- **Dùng: `tone_ok`** (κ 0.757) cho giọng văn, không chặn release về tiền. Sửa rubric theo audit #1–#4, #6 rồi calibrate lại.
- Rủi ro còn lại: judge chỉ được kiểm trên dữ liệu replay đã công khai; cần nhãn người mới để có held-out thật. Một nhãn người đã sai (H-081), nên nhãn cũng cần `checked_by`.
