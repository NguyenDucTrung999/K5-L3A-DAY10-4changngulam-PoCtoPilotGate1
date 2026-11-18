# Trace case: từ trace tới quyết định sai đầu tiên

Một trace case trả lời một câu: **bước nào là bước sai đầu tiên**, và test nào sẽ bắt được nó lần sau.

```bash
cd src
python -m lab9.trace_case --shape seeded_regression --claim C-014 --seed 11
python -m lab9.trace_case --shape fixed --claim C-014 --seed 11   # đối chứng
```

## Case: `seeded_regression C-014@11` (FM-05 pre_deducted)

| Trường | Nội dung |
|---|---|
| Trial | `seeded_regression C-014@11`, run `E-seeded_regression-20261117-0129` (eval set `0129b3828eed`), item `E-014` |
| Triệu chứng | Grader Lab 8: `FAIL (proposal_mismatch)`. `refund_amount_correct` False (ledger 90000 ≠ nhãn 120000), `proposal_matches_quote` False (120000 ≠ 150000), `reply_matches_ledger` False (reply "đã hoàn 120.000đ" nhưng ledger 90000) |
| Bước sai đầu tiên | **Event 5 `proposal` `{"amount_vnd": 120000}`** |
| Vì sao là bước *đầu tiên* | Event 1 `handoff`, 2 `investigator` (order O-515, `damage_verified` True, ship 30000), 3 `quote` 150000 (max của SHIP-LATE-03 30000 và DMG-04 150000) giống hệt bản `fixed`. Event 4 `refund_history` (đã hoàn 30000) chỉ là bước đọc. Event 5 là chỗ đầu tiên shape **dùng** số đã hoàn để tự trừ: 150000 − 30000 = 120000. Host (`durability.issue_refund`) lại trừ 30000 lần nữa, nên ledger chỉ còn 90000 |
| Failure mode | **FM-05** pre_deducted (gốc). FM-08 misreport là hệ quả: reply báo số tự tính 120000, không phải số host ghi |
| Đối chứng | `fixed C-014@11`: không có event `refund_history` / `proposal`. Quote đầy đủ 150000 đi thẳng vào host, host trừ 1 lần → ledger 120000 = nhãn, reply 120000 khớp ledger |
| Regression test | `src/tests/test_lab9_trace_case.py`: `test_lab9_trace_case_first_wrong_step_is_proposal` và `test_lab9_trace_case_graders_flag_pre_deduct`. Ba grader `ProposalMatchesQuote`, `RefundAmountCorrect`, `ReplyMatchesLedger` trả False trên `seeded_regression` và True trên `fixed` (đã chạy: pass). Test có tên chứa `lab9` nên job CI `-k "lab9 and not advanced"` chạy nó |
| Chưa chắc chắn | Trace không cho biết shape thật (không phải variant) có lặp lỗi này không. Mới thấy trên 2 claim có hoàn trước (C-013, C-014); claim có trần approval thấp hơn quote chưa kiểm cùng lúc với hoàn trước |

## Quy tắc

- Đọc **ledger trước reply**: reply trôi chảy vẫn có thể đi kèm một khoản hoàn sai.
- "Bước sai đầu tiên" phải dẫn số event cụ thể, không phải "agent bị nhầm".
- Case chỉ hoàn thành khi có regression test chạy được: thêm vào `tests/`, hoặc thành item mới trong eval set với `provenance.from_trace`.
