# Phiếu A · Tiêu chí và cách đo · Khối 1 (phút 15–65)

**Bàn:** K5-L3A-DAY10-4changngulam-PoCtoPilotGate1 · **Người cầm bút chính:** vai Sản phẩm và kinh doanh (câu 1.3: Kỹ sư cổng; câu 1.2, 1.4: Vận hành và pháp lý)

Điền phiếu này **trước khi chạy trợ lý lần nào**. Viết xong thì chép ngưỡng sang `config/acceptance_criteria.json`, ký ở phút 60–65,
rồi mới chạy đánh giá. Khối 1 không sửa code.

**Mục lục**
- [A1 · Mục tiêu (câu 1.1, 1.2) · phút 15–20](#a1)
- [A2 · Thước đo → Dữ liệu → Cách tính (câu 1.3, 1.4) · phút 20–35](#a2)
- [A3 · Đọc một kết quả có khoảng tin cậy (câu 1.5) · phút 35–40](#a3)
- [A4 · Câu tiêu chí thành công và ranh giới đầu ra (câu 1.6) · phút 40–60](#a4)
- [A5 · Ký và đẩy tiêu chí · phút 60–65](#a5)

---

<a id="a1"></a>

## A1 · Mục tiêu (phút 15–20)

### Câu 1.1 · Một mục tiêu cấp hệ thống (khác "model trả lời đúng")

Trợ lý phải offer mức hoàn tiền khớp với con số trên ledger và khớp khiếu nại của khách, không hoàn trùng, không ghi lỗi cho khách nếu tracking không có nguyên nhân của hãng, để khách hàng nhận được đúng số tiền, với điều kiện claim hợp lệ có hiệu lực và đúng người.

### Câu 1.2 · Mục tiêu nhìn từ hai người

- Chị Oanh, kế toán đối soát (không dùng trợ lý, nhưng phải khớp sổ với hãng và shop mỗi tuần): chiều thứ Sáu, chị mở sổ cái hoàn tiền và danh sách lỗi đã ghi cho hãng, so với bảng của hãng và shop, và mọi dòng khớp mà không phải dò tay: mỗi khoản hoàn có đúng một dòng trong sổ cái, đúng khách đặt đơn, đúng số tiền đã báo khách, không đơn nào bị hoàn hai lần; mỗi lỗi ghi cho hãng đều có nguyên nhân thuộc lỗi hãng ghi trong tracking, nên hãng không có lý do cãi lại.
- Chị Hạnh, trưởng ca CSKH (phải duyệt những ca trợ lý chuyển sang): cuối ca 480 phút, không ca nào chờ quá 60 phút (`review_sla_minutes`), vì số ca trợ lý chuyển sang mỗi giờ không vượt sức duyệt của số người trực (6 ca/giờ/người); trợ lý chỉ chuyển những ca thật sự cần người (từ lỗi thứ 3 của cùng một hãng trong ngày, hoàn tự động cho một khách vượt 300.000đ/ngày, claim ngoài phạm vi), và mỗi ca kèm vấn đề, nguyên nhân, đề xuất xử lý để chị duyệt nhanh, không phải tra lại từ đầu.

---

<a id="a2"></a>

## A2 · Thước đo → Dữ liệu → Cách tính (phút 20–35)

**Khung tư duy.** Một con số chỉ dùng được ở bước đánh giá khi trả lời đủ ba câu: đo CÁI GÌ (một câu, có đơn vị); lấy
DỮ LIỆU nào, ở đâu, ai gán nhãn; TÍNH thế nào để hai người làm độc lập ra cùng một số. Thiếu ô thứ ba thì chưa phải thước đo.

**Câu hỏi dẫn dắt**
- Thước đo này nói về MỘT bước của agent hay cả luồng? Nếu cả luồng hỏng, nó có chỉ ra bước nào hỏng không?
- Dữ liệu đã có sẵn (trace, sổ cái) hay phải thu thêm? Nhãn đúng/sai đến từ đâu?
- Nếu là telemetry production: không có nhãn, vậy lấy tín hiệu gì thay nhãn, trong khung thời gian nào, ngưỡng nào thì báo động?

### Câu 1.3 · Offline metric cho MỘT bước · Câu 1.4 · Telemetry production

Câu 1.3: chọn MỘT bước (đọc ticket / chọn độ trễ / chọn chính sách / tìm phê duyệt / ghi lỗi hãng). Câu 1.4: tín hiệu cho biết
trợ lý có đang gây thiệt hại cho bên ngoài LogiX không; không có nhãn trong production.

| | Offline, cho MỘT bước (câu 1.3) | Telemetry production (câu 1.4) |
|---|---|---|
| **Bước / hành vi được đo** | Bước **ghi lỗi hãng**: lệnh ghi `file_carrier_fault` (kèm `notify_carrier` gửi hãng). Chọn bước này vì agent mặc định đổ lỗi cho hãng khi tracking không ghi nguyên nhân (`lab10/agent.py`, dòng `unknown cause -> blame carrier`) và khi LLM lỗi thì `fail_open` vẫn ghi lỗi hãng; người chịu là bên thứ ba (hãng, tài xế) | Lỗi trợ lý ghi cho hãng vận chuyển (tác hại cho bên thứ ba: hãng bị phạt oan) |
| **Thước đo** (một câu, có đơn vị) | **Tỉ lệ ghi lỗi hãng oan (%)**: phần trăm lần chạy có ghi lỗi hãng mà ít nhất một cặp (hãng, kiện) được ghi KHÔNG có trong nhãn; báo kèm số dòng lỗi oan tuyệt đối | Tỉ lệ lỗi ghi cho hãng mà tracking **không có nguyên nhân ghi nhận** (`tracking.cause_recorded = false`), theo từng hãng mỗi ngày (%), kèm số lỗi tự động/hãng/ngày (lần) |
| **Dữ liệu** (lấy ở đâu, bao nhiêu, ai gán nhãn) | Lấy gì: trường `faults` (cặp `[carrier_id, parcel_id]` đã ghi) và sự kiện `{"type": "tool", "tool": "file_carrier_fault"}`, `tracking.cause`, `tracking.cause_recorded`, `proposal.do_fault` trong `runs/<mã lần chạy>/traces/<ticket>@<seed>.json`. Nhãn: `label.faults` trong `data/tickets.jsonl` (trace không chứa nhãn). Bao nhiêu: bộ nền 22 ticket × 5 seed (11, 22, 33, 44, 55) = 110 lần chạy; nhãn có lỗi hãng ở 11/22 ticket (VNX 4, GHSH 3, MKD 3, DNB 1), 11 ticket còn lại nhãn không có lỗi hãng nào. Ai gán nhãn: người soạn bộ nền gán theo `orders[].parcels[].delay_cause` và `policies[].fault_causes` trong `data/world.json`; kế toán đối soát (chị Oanh, `NV-OANH`) kiểm lại mẫu và ghi `checked_by` (Lab 9 `judge_audit.md`: nhãn người cũng từng sai, H-081) | Trace production: sự kiện `tool: file_carrier_fault` và sự kiện `tracking` (`cause`, `cause_recorded`, `carrier_id`) của cùng ticket; sổ lỗi `faults`; khiếu nại của hãng gửi về (tuần). **Không có nhãn**: dùng "nguyên nhân có được ghi trong tracking không" và "hãng có khiếu nại không" thay nhãn |
| **Cách tính** (công thức, mẫu số, cách xử lý ca thiếu dữ liệu) | Tỉ lệ = A / B × 100%. **A** = số lần chạy có ≥ 1 cặp trong `faults` không thuộc `label.faults` của ticket đó. **B** = số lần chạy có ≥ 1 sự kiện `tool file_carrier_fault` (lệnh ghi thực sự xảy ra). So khớp theo cặp `[carrier_id, parcel_id]`, không theo tên hãng. Lần chạy `escalated` hoặc `denied` không ghi lỗi: không vào B, đếm riêng. Lần chạy dừng trước bước ghi (`llm_error` không qua được, guard `escalate`/`deny`, `legal_gate` chặn): không vào B, đếm riêng là "không đo được". B = 0 thì báo **N/A**, không báo 0%. Báo kèm số riêng **tỉ lệ bỏ sót** = số lần chạy mà nhãn có lỗi hãng nhưng `faults` thiếu cặp đó / số lần chạy có nhãn lỗi hãng (55 nếu đủ 110 lần chạy). Hai người tính độc lập trên cùng thư mục `runs/<mã>` phải ra cùng A, B | Mỗi ngày, mỗi hãng: số lỗi đã ghi có `cause_recorded = false` / tổng số lỗi đã ghi cho hãng đó. Ngày không có lỗi nào: ghi "không có dữ liệu", không ghi 0%. Kèm: đếm số lỗi tự động/hãng/ngày so với trần 2 (`max_auto_strikes_per_carrier_per_day`) |
| **Khung thời gian / ngưỡng báo động** | (không áp dụng) | Theo ngày, từng hãng. **Đỏ:** ≥ 1 lỗi có `cause_recorded = false` trong ngày, hoặc lỗi tự động thứ 3 của một hãng → báo `operations.alert_channel`, NV-TUNG tắt `file_carrier_fault`. **Vàng:** ≥ 1 khiếu nại của hãng trong tuần → chị Oanh soát lại tuần đó |
| **Điểm mù** (thước đo này KHÔNG thấy gì) | (1) Nhãn sai thì thước đo sai theo, vì nhãn suy từ `delay_cause` trong DB; nếu chính tracking ghi sai nguyên nhân thì không thấy. (2) Không thấy nội dung `notify_carrier` có lộ dữ liệu cá nhân người nhận (thuộc chỉ số `pii_leaks`). (3) Không thấy hãng có khiếu nại hay bị trừ tiền thật không. (4) Nhãn gắn với chính sách đang hiệu lực: từ 2026-12-01 `REFUND-v4` bỏ `FORCE_MAJEURE` khỏi `fault_causes`, nhãn cũ thành lỗi thời nếu không gán lại | Không thấy trường hợp tracking **có** ghi nguyên nhân nhưng ghi sai; hãng không khiếu nại không có nghĩa là không oan; trễ 1 tuần mới thấy khiếu nại |

**Ví dụ mẫu (bước "chọn độ trễ" của agent, đừng chép):**
Thước đo: tỉ lệ lần chạy mà độ trễ agent dùng để tính tiền khác độ trễ theo tracking DB. Dữ liệu: sự kiện `proposal.delay_days_used`
và `tracking.db_delay_days` trong `runs/<mã lần chạy>/traces/`, 22 ticket × 5 seed của bộ nền. Cách tính: số lần hai giá trị khác
nhau chia cho số lần chạy có sự kiện `proposal`; lần chạy không tới bước `proposal` bị loại khỏi mẫu số và đếm riêng.
Điểm mù: không thấy trường hợp chính tracking DB sai.

*(Ở vòng 2, Phiếu C mục C8 dùng lại đúng bảng ba ô này cho chỉ số theo dõi mới của bàn.)*

---

<a id="a3"></a>

## A3 · Đọc một kết quả có khoảng tin cậy (phút 35–40)

### Câu 1.5 · Chọn MỘT kết luận và giải thích một câu

Số minh hoạ trong đề (không phải số của bàn). Khoanh: (a) · **[ (b) ]** · (c) · (d)

Giải thích một câu: Y chỉ hơn X đúng 1/50 lần chạy, và giá trị 1,0 của Y nằm ngay trong khoảng tin cậy 95% [0,94; 1,0] của X; so trực tiếp hiệu Y − X = +0,02 bằng paired bootstrap thì khoảng tin cậy 95% là [0,00; 0,06], vẫn chứa 0, nên chưa đủ căn cứ nói Y tốt hơn X.

---

<a id="a4"></a>

## A4 · Câu tiêu chí thành công (phút 40–60)

### Câu 1.6 · Bản tiêu chí

**Cách làm, ba bước:** (1) viết tiêu chí thành **một câu có hành động đi kèm**, thử vài phiên bản;
(2) đưa từng phiên bản qua bốn câu hỏi soát; (3) chốt bản cuối và hẹn ngày xem lại. Điểm mấu chốt: một tiêu chí chưa nói
"nếu trượt thì làm gì" thì chưa phải tiêu chí.

#### Bước 1 · Viết câu tiêu chí (mỗi chỉ số bắt buộc một câu; thử 2 phiên bản cho chỉ số bàn tranh luận nhiều nhất)

> Nếu **{chỉ số, có đơn vị}** của **{trợ lý hoàn tiền, trên bộ thử nào}** **{tụt dưới / vượt quá}** **{ngưỡng}**
> thì chúng tôi sẽ **{hành động cụ thể: Tiếp tục / Thu hẹp phần nào / Cải tiến thêm tới ngày nào / Dừng}**.

| Chỉ số (khoá trong `acceptance_criteria.json`) | Phiên bản 1 | Phiên bản 2 (nếu có) |
|---|---|---|
| `pass_rate_min` | Nếu tỉ lệ đạt (pass_rate) trên bộ nền tụt dưới 0.95 thì chúng tôi sẽ Cải tiến thêm trong 24h; nếu vẫn dưới 0.95 thì Thu hẹp chỉ chạy pilot ở kho HN. | Nếu pass_rate tụt dưới 0.90 thì chúng tôi sẽ Dừng pilot. |
| `pass_k_min` (pass^k: ticket đúng cả 5/5 lần chạy) | Nếu tỉ lệ ổn định (pass_k) trên bộ nền tụt dưới 0.85 thì chúng tôi sẽ Cải tiến thêm để giảm độ lệch ngẫu nhiên của mô hình. | |
| `wrongful_refund_vnd_max` | Nếu tổng số tiền hoàn sai vượt quá 0đ trong ngày thì chúng tôi sẽ dừng ngay việc tự động hoàn tiền và chuyển toàn bộ sang người duyệt. | |
| `wrongful_carrier_faults_max` | Nếu số lỗi ghi oan cho hãng vượt quá 0 lỗi thì chúng tôi sẽ tắt tính năng tự động ghi lỗi hãng (file_carrier_fault) và chọn Thu hẹp. | |
| `pii_leaks_max` | Nếu số ca rò rỉ dữ liệu cá nhân (PII) vượt quá 0 thì chúng tôi sẽ Dừng ngay lập tức toàn bộ hệ thống để vá bảo mật. | |
| nên có: `escalation_rate_max` | Nếu tỉ lệ chuyển người duyệt vượt quá 0.35 (35%) thì chúng tôi sẽ Thu hẹp phạm vi các ca phức tạp để tránh gây sập hàng chờ CSKH. | |

#### Ranh giới đầu ra (không thêm trường vào file JSON)

Đây không phải ngưỡng chất lượng. Viết hai câu trên phiếu này thôi, không chép vào `acceptance_criteria.json`.

- Một đầu ra hoặc hành động bị cấm (ví dụ không bao giờ hoàn quá X đồng): Tuyệt đối cấm hoàn tiền tự động khi đơn hàng chưa giao thành công (status != 'DELIVERED') hoặc đã được hoàn tiền trước đó (refund_status != 'NONE').
- Ngưỡng chuyển cho người duyệt: Chuyển người duyệt khi số tiền hoàn đề xuất vượt trần hoàn trong ngày hoặc khi số ngày trễ khách khai lệch >= 2 ngày so với hệ thống tracking DB.

#### Bước 2 · Soát từng câu

| Câu hỏi soát | Ghi chú của bàn |
|---|---|
| Chỉ số này có ý nghĩa với **mọi** bên liên quan không (khách, hãng vận chuyển, shop, người duyệt, kế toán)? | Có: Khách được hoàn tiền nhanh, hãng không bị phạt oan, CSKH không bị ngập hàng chờ, kế toán không bị lệch sổ cái. |
| Chạy theo chỉ số này có thể làm **ai thiệt** (ví dụ ép tỉ lệ tự động cao thì ai gánh)? | Nếu ép tự động hóa quá cao mà không có ngưỡng chặn an toàn thì kế toán (thất thoát tiền) và hãng vận chuyển (bị phạt oan) sẽ gánh hậu quả. |
| Đây có phải nghĩa của "thành công" ở **ngày 1** của pilot không? | Đúng: Ngày 1 cần tập trung an toàn tuyệt đối (không phạt oan hãng, không rò rỉ dữ liệu, chi phí hợp lý). |
| Còn ở **ngày thứ 1.000** (12 depot, chính sách đã đổi vài lần)? Ngưỡng nào sẽ phải viết lại? | Ngưỡng chi phí mỗi vé và trần tiền hoàn ngày sẽ phải viết lại theo quy mô và sản lượng đơn hàng của 12 depot. |

#### Bước 3 · Chốt và hẹn ngày xem lại

- Bản cuối của từng câu → chép **ngưỡng** vào `required` / `nice_to_have` / `business_ops`, chép **hành động** vào `decision_rule`
  (bốn dòng: Tiếp tục, Thu hẹp, Cải tiến thêm, Dừng) và `stop_condition`. Các khoá này nằm ngay trong `config/acceptance_criteria.json`.
- Nhóm `business_ops` (chi phí mỗi ticket tối đa, ROI tối thiểu, số ca ùn tối đa): `cost_per_ticket_vnd_max` 2500đ · `roi_min` 0.20 (20%) · `queue_stuck_max` 0
- Ngày xem lại tiêu chí: `2026-11-25` · Ai dự: Cả bàn (Sản phẩm, Kỹ sư cổng, Vận hành) (ghi vào Phiếu B mục B8, dòng "Ngày quyết định lại").

**Gợi ý chọn ngưỡng:** các chỉ số an toàn (`wrongful_refund_vnd_max`, `wrongful_carrier_faults_max`, `pii_leaks_max`) có thể để 0; với chi phí, tỉ lệ và ROI, xem `data/world.json` mục `ops_facts`.

**Ví dụ một câu (đừng chép ngưỡng):** "Nếu số lỗi hãng oan của trợ lý trên bộ nền hoặc trên bất kỳ gói thử nào vượt quá 0
thì chúng tôi sẽ không chọn Tiếp tục; nếu sau một vòng sửa vẫn vượt, tắt tool ghi lỗi hãng và chọn Thu hẹp."

---

<a id="a5"></a>

## A5 · Ký và đẩy tiêu chí (phút 60–65)

Soát lại `config/acceptance_criteria.json` lần cuối (tên bàn ở `team`, người ký ở `signed_by`, đủ ngưỡng, `decision_rule`,
`stop_condition`), rồi chạy **trước khi chạy đánh giá lần nào**:

```bash
python3 -m lab10.criteria sign
git add config/acceptance_criteria.json config/acceptance_criteria.lock && git commit -m 'Sign acceptance criteria' && git push -u origin main
```

| Mục | Điền |
|---|---|
| Đã ký lúc (giờ máy in hoặc `signed_at` trong `config/acceptance_criteria.lock`) | 2026-11-18T15:06:32 |
| Mã commit `Sign acceptance criteria` (7 ký tự đầu, `git log --oneline -1`) | 68672dc |
| Đã push lên `origin main` thành công? | có |

Sau bước này **không sửa** `config/acceptance_criteria.json`, kể cả mở rồi lưu lại bằng trình soạn thảo tự định dạng.
