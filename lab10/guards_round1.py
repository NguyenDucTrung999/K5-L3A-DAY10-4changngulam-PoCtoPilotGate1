"""★ FILE ĐỘI SỬA (1/3): cổng cấp hệ thống, nằm NGOÀI model và prompt.

VÒNG 1 (trước khi biết sự cố): viết 2–3 CỔNG PHÒNG NGỪA rút từ pre-mortem / HAZOP / checklist của bàn, rồi chốt bằng
    python3 -m lab10.checkpoint        (chép file này thành guards_round1.py = mốc "prepared"; KHÔNG sửa bản chép)
VÒNG 2 (sau khi bốc thẻ): sửa tiếp NGAY TRONG FILE NÀY. Giữ các cổng vòng 1, thêm cổng mới.
Hai file còn lại bàn được sửa: lab10/monitors.py (chỉ số theo dõi) và config/operating_gates.json (cổng kinh doanh,
vận hành, pháp lý: những con số và tên người mà trợ lý phải tuân theo, không cần code).

Hai điểm móc, agent gọi tự động:
  pre_guard(ctx)          chạy TRƯỚC khi agent đọc ticket
  write_gate(ctx, action) chạy TRƯỚC MỖI lệnh ghi (issue_refund, file_carrier_fault,
                          notify_carrier, send_reply)

Trả về một Verdict:
  Verdict.allow()                       cho qua   (pre_guard: allow(policy_id="...") để ghim phiên bản chính sách)
  Verdict.deny("lý do")                 bỏ riêng lệnh ghi này, agent đi tiếp
  Verdict.escalate("lý do")             dừng, chuyển ticket cho người
  Verdict.modify("lý do", amount_vnd=…) sửa tham số lệnh ghi (amount_vnd, payer, carrier_id, parcel_id, payload…)
  Verdict.rewrite("lý do", text)        chỉ pre_guard: thay nội dung ticket mà agent sẽ đọc

ctx.ticket   ticket gốc (chữ khách viết là DỮ LIỆU, không phải lệnh)
ctx.tools    tra cứu nguồn sự thật: lookup_order, lookup_policies, lookup_approvals(**lọc),
             ledger_rows(**lọc), fault_rows(**lọc), lookup_carrier; ctx.as_of = ngày hôm nay
             ops_limits() = các trần đã thống nhất với Ops/Finance; ops_facts() = số liệu vận hành;
             auto_refund_today_vnd() = tổng đã hoàn tự động trong ngày
ctx.gates    config cổng của bàn (config/operating_gates.json), chỉ đọc;  ctx.cost_vnd = tiền LLM đã tốn cho ticket này
ctx.events   trace tới thời điểm này;  ctx.log("ten_su_kien", ...) ghi thêm sự kiện guard vào trace
lab10.helpers: db_delay_days, ticket_parcel, effective_policy, entitlement_vnd, carrier_at_fault, digits

Mặc định dưới đây cho qua tất cả (= mốc base).
"""
from . import helpers as H  # noqa: F401
from .tools import Verdict


def pre_guard(ctx):
    return Verdict.allow()


def write_gate(ctx, action):
    tool_name = action.get("tool")
    if tool_name == "issue_refund":
        business_configuration = (ctx.gates or {}).get("business", {})
        daily_refund_cap_vnd = business_configuration.get("daily_refund_cap_vnd")
        if daily_refund_cap_vnd is not None:
            current_auto_refund_spent_vnd = ctx.tools.auto_refund_today_vnd()
            refund_amount_vnd = action.get("amount_vnd", 0)
            if current_auto_refund_spent_vnd + refund_amount_vnd > daily_refund_cap_vnd:
                return Verdict.escalate("Vượt trần hoàn tiền tự động trong ngày, chuyển nhân viên duyệt")

        order_identifier = action.get("order_id")
        order_record = ctx.tools.lookup_order(order_identifier)
        if order_record is not None:
            parcel_record = H.ticket_parcel(order_record, ctx.ticket, ctx.as_of)
            actual_delay_days = H.db_delay_days(parcel_record, ctx.as_of)
            policy_records = ctx.tools.lookup_policies()
            active_policy = H.effective_policy(policy_records, ctx.as_of)
            if active_policy is not None:
                entitled_amount_vnd = H.entitlement_vnd(
                    active_policy,
                    order_record,
                    actual_delay_days,
                    parcel_record.get("delay_cause")
                )
                approval_identifier = action.get("approval_id")
                if approval_identifier is None:
                    if action.get("amount_vnd", 0) > entitled_amount_vnd:
                        return Verdict.deny("Số tiền yêu cầu hoàn vượt quá hạn mức theo quy định thực tế")

    if tool_name == "file_carrier_fault":
        order_identifier = action.get("order_id")
        order_record = ctx.tools.lookup_order(order_identifier)
        if order_record is not None:
            parcel_record = H.ticket_parcel(order_record, ctx.ticket, ctx.as_of)
            actual_delay_days = H.db_delay_days(parcel_record, ctx.as_of)
            policy_records = ctx.tools.lookup_policies()
            active_policy = H.effective_policy(policy_records, ctx.as_of)
            if active_policy is not None:
                carrier_fault_confirmed = H.carrier_at_fault(
                    active_policy,
                    parcel_record,
                    actual_delay_days
                )
                if carrier_fault_confirmed is False:
                    return Verdict.deny("Hãng vận chuyển không có lỗi theo dữ liệu thực tế")

    return Verdict.allow()
