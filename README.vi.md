# Bot Auto Commit

[English README](README-auto-commit.md)

Một bot tự động đơn giản để tự động commit thay đổi vào repository theo lịch hàng ngày sử dụng GitHub Actions.

## Tổng quan

Dự án này bao gồm:
- Một script Python (`bot-auto-commit.py`) cập nhật file log với timestamp
- Một workflow GitHub Actions (`.github/workflows/auto-commit.yml`) chạy script hàng ngày và commit thay đổi

## Tính năng

- **Cập nhật tự động hàng ngày**: Chạy mỗi ngày lúc nửa đêm UTC
- **Kích hoạt thủ công**: Có thể kích hoạt thủ công qua GitHub Actions
- **Ghi log đơn giản**: Thêm các mục timestamp vào `log.txt`
- **Thao tác Git tự động**: Tự động xử lý git add, commit và push

## Cấu trúc dự án

```
├── .github/
│   └── workflows/
│       └── auto-commit.yml    # Workflow GitHub Actions
├── bot-auto-commit.py         # Script Python để cập nhật
├── log.txt                    # File log được tạo tự động
```

## Mô tả các file

### 1. Workflow GitHub Actions (`.github/workflows/auto-commit.yml`)

```yaml
name: Bot Auto Commit
on:
  schedule:
    - cron: '0 0 * * *'  # Chạy hàng ngày lúc nửa đêm UTC
  workflow_dispatch:     # Cho phép kích hoạt thủ công

jobs:
  update-file:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout Repository
        uses: actions/checkout@v3
      
      - name: Set Up Python
        uses: actions/setup-python@v3
        with:
          python-version: '3.x'
      
      - name: Run Update Script
        run: python bot-auto-commit.py
      
      - name: Commit and Push Changes
        run: |
          git config --local user.email "github-actions[bot]@users.noreply.github.com"
          git config --local user.name "GitHub Action Bot"
          git add log.txt
          git commit -m "Automated update: $(date +'%Y-%m-%d %H:%M:%S')"
          git push
```

### 2. Script Python (`bot-auto-commit.py`)

```python
from datetime import datetime

with open("log.txt", "a") as file:
    file.write(f"Updated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
```

## Hướng dẫn cài đặt

### 1. Tạo file Workflow

1. Tạo cấu trúc thư mục: `.github/workflows/`
2. Thêm file `auto-commit.yml` với cấu hình workflow ở trên

### 2. Thêm Script Python

1. Tạo `bot-auto-commit.py` trong thư mục gốc repository
2. Copy code Python ở trên vào file

### 3. Kích hoạt GitHub Actions

1. Vào repository trên GitHub
2. Chuyển đến tab **Actions**
3. Kích hoạt GitHub Actions nếu chưa được bật
4. Workflow sẽ tự động bắt đầu chạy theo lịch

### 4. Kích hoạt thủ công (Tùy chọn)

Để kích hoạt bot thủ công:
1. Vào tab **Actions** trong repository
2. Chọn workflow "Bot Auto Commit"
3. Nhấn nút "Run workflow"
4. Chọn branch và nhấn "Run workflow"

## Cách hoạt động

1. **Thực thi theo lịch**: GitHub Actions chạy workflow hàng ngày lúc nửa đêm UTC
2. **Thực thi Script**: Script Python thêm mục timestamp vào `log.txt`
3. **Thao tác Git**: Workflow commit thay đổi với message tự động
4. **Push thay đổi**: Thay đổi được push trở lại repository

## Định dạng Log được tạo

File `log.txt` sẽ chứa các mục như:
```
Updated on 2024-01-15 00:00:01
Updated on 2024-01-16 00:00:01
Updated on 2024-01-17 00:00:01
```

## Tùy chỉnh

### Thay đổi lịch
Sửa biểu thức cron trong file workflow:
- `'0 0 * * *'` - Hàng ngày lúc nửa đêm UTC
- `'0 */6 * * *'` - Mỗi 6 giờ
- `'0 0 * * 1'` - Hàng tuần vào thứ Hai

### Sửa nội dung Log
Chỉnh sửa script Python để thay đổi nội dung ghi vào log:
```python
# Ví dụ: Thêm thông tin khác
with open("log.txt", "a") as file:
    file.write(f"Bot update: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - Status: OK\n")
```

### Thay đổi message commit
Sửa message commit trong workflow:
```bash
git commit -m "Cập nhật tự động hàng ngày: $(date +'%Y-%m-%d %H:%M:%S')"
```

## Khắc phục sự cố

### Workflow không chạy
- Kiểm tra xem GitHub Actions đã được kích hoạt cho repository chưa
- Xác minh file workflow ở đúng vị trí (`.github/workflows/`)
- Kiểm tra tab Actions để xem có thông báo lỗi nào không

### Vấn đề quyền
- Đảm bảo repository có quyền ghi cho GitHub Actions
- Kiểm tra xem workflow có quyền cần thiết để push thay đổi không

### Lỗi Script Python
- Xác minh cú pháp script Python đúng
- Kiểm tra log Actions để xem có lỗi liên quan đến Python không

## Ghi chú bảo mật

- Bot sử dụng user `github-actions[bot]` có sẵn của GitHub để commit
- Không nên bao gồm thông tin nhạy cảm trong file log
- Workflow chạy với quyền GitHub Actions tiêu chuẩn

## Giấy phép

Dự án này là mã nguồn mở và có sẵn dưới [MIT License](LICENSE).
