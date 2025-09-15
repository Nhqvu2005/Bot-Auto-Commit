## Bot Auto Commit



Script Python cập nhật `log.txt` trong repo GitHub theo số lần bạn nhập vào. Mỗi lần chạy sẽ xóa toàn bộ nội dung cũ và ghi một dòng thời gian, tạo commit hợp lệ qua GitHub API.

### Tính năng
- Đọc token GitHub từ biến môi trường `GITHUB_TOKEN` hoặc file `token.txt`.
- Tự động phát hiện `owner` của repo `Bot-Auto-Commit` bằng token (có thể override qua biến môi trường).
- Ghi đè `log.txt` và commit lên nhánh chỉ định, lặp lại theo số lần nhập.

### Yêu cầu
- Python 3.9+
- Token GitHub hợp lệ
- Quyền (scopes/permissions):
  - Fine‑grained token (khuyến nghị):
    - Repository access: chọn repo `Bot-Auto-Commit`
    - Repository permissions: Contents → Read and write; Metadata → Read (mặc định)
  - Classic token:
    - Repo public: `public_repo`
    - Repo private: `repo`
    - Nếu cần liệt kê repo private trong tổ chức: thêm `read:org`

### Cài đặt
1. Cài phụ thuộc:
```bash
pip install -r requirements.txt
```
Nội dung `requirements.txt` tối thiểu:
```text
python-dotenv>=1.0.1
```

2. Cấu hình token:
- Cách 1: Biến môi trường (khuyên dùng)
```powershell
$env:GITHUB_TOKEN="ghp_xxx_your_token_here"
```
- Cách 2: File `token.txt` (đặt cùng thư mục với script), chứa một dòng token.

3. Tuỳ chọn: tạo file `.env` để khai báo biến môi trường:
```env
REPO_NAME=Bot-Auto-Commit
REPO_BRANCH=main
```

### Sử dụng
Chạy script:
```powershell
python .\bot-auto-commit.py
```
- Script sẽ tự phát hiện `owner` bằng token. Nếu cần chỉ định thủ công, đặt biến môi trường `REPO_OWNER`.
- Nhập số lần sửa `log.txt` khi được hỏi. Mỗi lần sẽ tạo một commit.

#### Tuỳ biến
- Nhánh: nếu repo dùng `master`, đặt biến môi trường:
```powershell
$env:REPO_BRANCH="master"
```
- Tên repo: nếu không phải `Bot-Auto-Commit`:
```powershell
$env:REPO_NAME="TenRepoKhac"
```

### Kiểm tra quyền token nhanh
- Thử gọi các API sau (hoặc đơn giản là chạy script):
  - `GET /user`
  - `GET /repos/{owner}/{repo}/contents/log.txt`
  - `PUT /repos/{owner}/{repo}/contents/log.txt`
- Nếu nhận 403/404 do quyền, dùng Classic `repo` hoặc Fine‑grained Contents: Read and write.

### Lưu ý
- Nếu repo bật branch protection, có thể cần commit qua nhánh khác rồi mở PR.
- Script nghỉ 2 giây giữa các commit để tránh giới hạn tốc độ; có thể điều chỉnh.

## Chạy tự động trên GitHub (cron)

Repo đã có sẵn workflow tại `.github/workflows/daily.yml` chạy hằng ngày lúc 00:00 UTC.

### Bật và chạy
- Push repo lên GitHub và bật Actions.
- Workflow sẽ tự chạy theo lịch, cũng có thể chạy thủ công (Run workflow).

### Cấu hình
- Đổi tần suất: sửa `cron` trong `.github/workflows/daily.yml`.
  - Ví dụ chạy 17:00 Việt Nam (UTC+7): `0 10 * * *`.
- Đổi số lần cập nhật mỗi lượt chạy: đặt `TIMES` trong bước “Run bot-auto-commit”.
- Nhánh mặc định: đặt `REPO_BRANCH` (ví dụ `main` hoặc `master`).

### Dùng danh tính của bạn (tuỳ chọn)
Mặc định commit sẽ đứng tên `github-actions[bot]` và có thể không tính vào đóng góp cá nhân.
- Để commit đứng tên bạn, đặt biến:
  - `AUTHOR_NAME`: tên hiển thị GitHub của bạn
  - `AUTHOR_EMAIL`: email đã xác thực hoặc `yourusername@users.noreply.github.com`
  
Cách lấy:
- AUTHOR_NAME: GitHub → Settings → Profile → Name (không có thì dùng `username`).
- AUTHOR_EMAIL (noreply): GitHub → Settings → Emails → sao chép địa chỉ kết thúc bằng `@users.noreply.github.com`.
- AUTHOR_EMAIL (email thật): phải là email đã xác thực trong tài khoản GitHub. Nếu bật ẩn email, nên dùng địa chỉ noreply.

