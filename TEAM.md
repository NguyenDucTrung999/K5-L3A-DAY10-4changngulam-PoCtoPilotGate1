# Team

## Thông tin nhóm

- Tên nhóm (`TenNhom`, không dấu, không khoảng trắng): `4changngulam`
- Lớp: `L3A`
- Repo của bàn: `K5-L3A-DAY10-4changngulam-PoCtoPilotGate1`
- Thẻ sự cố đã bốc (S1–S8): `S3`

## Thành viên

Họ tên đầy đủ và MSSV của **mọi** thành viên; thêm dòng nếu cần. Vai: Kỹ sư cổng · Sản phẩm và kinh doanh · Vận hành và pháp lý (README mục 3, phút 0–15).

| STT | Họ và tên | MSSV | Vai | Trưởng nhóm |
| --: | --------- | ---- | --- | :---------: |
|   1 | Nguyễn Đức Trung | | Kỹ sư cổng | x |
|   2 | Nguyễn Huy Thứ | | Kỹ sư cổng | |
|   3 | Đỗ Minh Hiếu | | Sản phẩm và kinh doanh | |
|   4 | Bùi Văn Lâm | 2A202603400 | Vận hành và pháp lý | |

Ghi `members` trong `submission/submission.json` theo dạng `"HoVaTen-MSSV"`, khớp bảng trên.

## Cá nhân

Mỗi thành viên tự viết một mục bên dưới (chép mẫu, đổi tiêu đề thành họ tên không dấu và MSSV, ví dụ `## NguyenVanAn-20241234`).

## BuiVanLam-2A202603400

### Phần việc phụ trách

Vai Vận hành và pháp lý: Cấu hình `config/operating_gates.json` (mục `operations` và `legal`); điền Phiếu C (`templates/form-c-incident.md`) các mục C1 (đối chiếu Pre-mortem), C3.5 (mở lại bản đồ dữ liệu policies và delay_cause), C4 (HAZOP thẻ S3 với hãng Mekong Delta Ship), C5 (Câu 3.3 - giả định môi trường), C10 (Risk register) và C11 (Checklist 9 việc & Runbook 4-5 đối soát khẩn cấp).

### Đóng góp cụ thể

- Cấu hình cổng pháp lý `carrier_fault_requires_recorded_cause = true` ngăn chặn AI tự ý phạt lỗi hãng khi thiếu nguyên nhân chính thức.
- Bổ sung 3 dòng HAZOP chi tiết cho tool `file_carrier_fault` với các guideword INVALID, INCOMPLETE, PERTURBED để bảo vệ hãng vận chuyển Mekong Delta Ship (MKD).
- Xây dựng quy trình ứng phó khủng hoảng trong Runbook 4-5: gửi thư xin lỗi và hoàn trả 120.000đ cho hãng MKD trong 2 giờ, kích hoạt kiểm tra delay_cause thiên tai.

### Bằng chứng

- File `config/operating_gates.json` mục `operations` và `legal`.
- File `templates/form-c-incident.md` các mục C1, C3.5, C4, C5 (3.3), C10, C11.

### Exit ticket

- Một điều học được: Hệ thống AI ngoài đời thực không chỉ phụ thuộc vào model mà phụ thuộc sống còn vào các cổng pháp lý và quy trình vận hành ngoại vi; khi bão lũ thiên tai xảy ra, giả định về dữ liệu tracking thời gian thực sẽ bị sụp đổ nếu không có điều khoản miễn trừ Force Majeure.
- Một điều còn chưa chắc: Làm thế nào để tự động hóa việc đồng bộ cảnh báo thiên tai từ cơ quan khí tượng thủy văn vào hệ thống AI theo thời gian thực mà không cần người trực ca can thiệp thủ công.
