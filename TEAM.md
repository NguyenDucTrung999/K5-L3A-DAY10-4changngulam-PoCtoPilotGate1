# Team

## Thông tin nhóm

- Tên nhóm (`TenNhom`, không dấu, không khoảng trắng): 4changngulam
- Lớp: `L3A`
- Repo của bàn: `K5-L3A-DAY10-4changngulam-PoCtoPilotGate1`
- Thẻ sự cố đã bốc (S1–S8): S3

## Thành viên

Họ tên đầy đủ và MSSV của **mọi** thành viên; thêm dòng nếu cần. Vai: Kỹ sư cổng · Sản phẩm và kinh doanh · Vận hành và pháp lý (README mục 3, phút 0–15).

| STT | Họ và tên | MSSV | Vai | Trưởng nhóm |
| --: | --------- | ---- | --- | :---------: |
|   1 | Nguyễn Đức Trung | 2A202603423 | Kỹ sư cổng 1 | x |
|   2 | Nguyễn Huy Thứ | 2A202603356 | Kỹ sư cổng 2 | |
|   3 | Đỗ Minh Hiếu | 2A202603402 | Sản phẩm và kinh doanh | |
|   4 | Bùi Văn Lâm | 2A202603400 | Vận hành và pháp lý | |

Ghi `members` trong `submission/submission.json` theo dạng `"HoVaTen-MSSV"`, khớp bảng trên.

## Cá nhân

## NguyenDucTrung-2A202603423

### Phần việc phụ trách
Kỹ sư cổng 1; thiết lập môi trường Git, ký tiêu chí chấp nhận, lập trình 3 cổng phòng ngừa trong `lab10/guards.py`, thực hiện chốt cổng vòng 1 (checkpoint), chạy các mốc đo lường và quản trị kho lưu trữ.

### Đóng góp cụ thể
Viết hàm `write_gate` kiểm soát hoàn tiền theo dữ liệu tracking thực tế, kiểm tra trần ngân sách ngày và kiểm soát phạt lỗi hãng. Điền mục B0, B1, B7.1 trong Phiếu B.

### Bằng chứng
Mã commit `68672dc`, `c5d2ddf`; mã lần chạy `R-base-before-20261118-150653-b45eeb`, `R-base-prepared-20261118-150802-d22ede`.

### Exit ticket
Học được cách thiết lập cổng phòng ngừa cấp hệ thống để bảo vệ trợ lý AI khỏi việc bị đánh lừa bởi dữ liệu khách tự khai.

## NguyenHuyThu-2A202603356

### Phần việc phụ trách
Kỹ sư cổng 2; phân tích trace ticket lỗi, thiết kế offline metric và khoảng tin cậy ở Phiếu A; phân tích lỗi T-002, pre-mortem, chống rò rỉ dữ liệu và behavioral test ở Phiếu B.

### Đóng góp cụ thể
Điền câu 1.3 và 1.5 trong Phiếu A; điền mục B2, B6, B7.2, B7.3 trong Phiếu B; tạo 2 ticket hiểm kiểm thử tính chất bất biến.

### Bằng chứng
Mã commit `98f9e74`; nhánh `origin/NguyenHuyThu_2A202603356`.

### Exit ticket
Hiểu rõ sự khác biệt giữa lỗi ngữ cảnh và lỗi chìm trong hệ thống AI tự động hóa tác vụ ghi.

## DoMinhHieu-2A202603402

### Phần việc phụ trách
Sản phẩm và kinh doanh; thiết lập mục tiêu hệ thống, telemetry production trong Phiếu A; tích hợp tài liệu Lab 9 vào `docs/lab9/`.

### Đóng góp cụ thể
Điền câu 1.1, 1.2, 1.4 trong Phiếu A; chuẩn bị tài liệu PRD v1.1, taxonomy và eval card.

### Bằng chứng
Mã commit `a75d9f6`, `f9413f9`; nhánh `origin/po/lab9-tai-lieu-chung`.

### Exit ticket
Thấy rõ tầm quan trọng của việc xây dựng telemetry production khi không có nhãn kiểm thử trong môi trường thực tế.

## BuiVanLam-2A202603400

### Phần việc phụ trách
Vận hành và pháp lý; xây dựng Bản tiêu chí chấp nhận trong Phiếu A; xây dựng bản đồ dữ liệu và drift, cổng kinh doanh, HAZOP và Runbook trong Phiếu B.

### Đóng góp cụ thể
Điền câu 1.6 trong Phiếu A; điền mục B3, B4, B5, B7.4, B7.5, B7.6 trong Phiếu B.

### Bằng chứng
Mã commit `eb2c98a`; nhánh `origin/buivanlam`.

### Exit ticket
Nắm vững quy trình vận hành và cơ chế dừng khẩn cấp khi hệ thống AI phát sinh lỗi ngoài thực địa.
