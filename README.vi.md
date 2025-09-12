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
└── README-auto-commit.vi.md   # File này
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

#### Cách 1: Sử dụng giao diện web GitHub (Khuyến nghị)

**Hướng dẫn từng bước tạo file workflow:**

1. **Vào phần Actions:**
   - Vào repository trên GitHub
   - Nhấn vào tab **Actions** (bên cạnh Code, Issues, Pull requests)

2. **Tạo workflow mới:**
   - Nếu đây là workflow đầu tiên, nhấn **"I understand my workflows, go ahead and enable them"**
   - Nhấn **"New workflow"** hoặc **"set up a workflow yourself"**

3. **Chỉnh sửa file workflow:**
   - GitHub sẽ tạo file mới tại `.github/workflows/main.yml`
   - Bạn sẽ thấy template mặc định - xóa toàn bộ nội dung
   - Copy và dán cấu hình workflow hoàn chỉnh từ phần trên

4. **Đổi tên file:**
   - Nhấn vào tên file `main.yml` trong editor
   - Đổi thành `auto-commit.yml`
   - Nhấn Enter để xác nhận

5. **Commit file:**
   - Nhấn **"Start commit"**
   - Thêm message commit như "Add auto-commit workflow"
   - Nhấn **"Commit new file"**

**Hướng dẫn trực quan:**
```
Actions tab → New workflow → Xóa template → Dán YAML của chúng ta → Đổi tên file → Commit
```

#### Cách 2: Sử dụng Git local

1. Tạo cấu trúc thư mục: `.github/workflows/`
2. Thêm file `auto-commit.yml` với cấu hình workflow ở trên
3. Commit và push lên repository

### 2. Thêm Script Python

1. Tạo `bot-auto-commit.py` trong thư mục gốc repository
2. Copy code Python ở trên vào file

### 3. Kích hoạt GitHub Actions và thiết lập quyền

#### Kích hoạt GitHub Actions

1. Vào repository trên GitHub
2. Chuyển đến tab **Actions**
3. Nếu GitHub Actions chưa được kích hoạt, nhấn **"I understand my workflows, go ahead and enable them"**
4. Workflow sẽ tự động bắt đầu chạy theo lịch

#### Thiết lập quyền Repository (Quan trọng!)

1. Vào tab **Settings** của repository
2. Cuộn xuống phần **Actions** ở thanh bên trái
3. Nhấn vào **General**
4. Trong **"Workflow permissions"**, chọn:
   - ✅ **"Read and write permissions"** (bắt buộc cho auto-commit)
   - ✅ **"Allow GitHub Actions to create and approve pull requests"** (tùy chọn)
5. Nhấn **Save**

#### Phương án thay thế: Sử dụng Personal Access Token (Nâng cao)

Nếu bạn cần kiểm soát nhiều hơn, có thể sử dụng Personal Access Token:

1. Vào GitHub **Settings** → **Developer settings** → **Personal access tokens** → **Tokens (classic)**
2. Nhấn **"Generate new token"**
3. Chọn scopes: `repo` (toàn quyền kiểm soát repository private)
4. Copy token
5. Vào repository **Settings** → **Secrets and variables** → **Actions**
6. Nhấn **"New repository secret"**
7. Tên: `GITHUB_TOKEN`, Giá trị: token của bạn
8. Cập nhật workflow để sử dụng secret:

```yaml
- name: Commit and Push Changes
  env:
    GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
  run: |
    git config --local user.email "github-actions[bot]@users.noreply.github.com"
    git config --local user.name "GitHub Action Bot"
    git add log.txt
    git commit -m "Automated update: $(date +'%Y-%m-%d %H:%M:%S')"
    git push https://${{ secrets.GITHUB_TOKEN }}@github.com/${{ github.repository }}.git
```

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
- Đảm bảo lịch cron hợp lệ (dùng [crontab.guru](https://crontab.guru) để kiểm tra)

### Vấn đề quyền

**Các lỗi quyền thường gặp và cách khắc phục:**

1. **"Permission denied" khi push:**
   ```
   Error: fatal: could not read Username for 'https://github.com': terminal prompts disabled
   ```
   **Giải pháp:** Thiết lập quyền repository thành "Read and write permissions" (xem phần Setup)

2. **"Resource not accessible by integration":**
   - Vào repository Settings → Actions → General
   - Trong "Workflow permissions", chọn "Read and write permissions"
   - Nhấn Save

3. **Đối với repository private:**
   - Đảm bảo đã thiết lập quyền đúng trong Settings
   - Cân nhắc sử dụng phương pháp Personal Access Token nếu vẫn gặp vấn đề

**Cách kiểm tra quyền hiện tại:**
1. Vào repository Settings
2. Cuộn đến Actions → General
3. Kiểm tra phần "Workflow permissions"
4. Phải hiển thị "Read and write permissions" để auto-commit hoạt động

### Lỗi Script Python
- Xác minh cú pháp script Python đúng
- Kiểm tra log Actions để xem có lỗi liên quan đến Python không
- Đảm bảo script tạo/sửa file trong thư mục gốc repository

### Các bước debug

1. **Kiểm tra workflow runs:**
   - Vào tab Actions
   - Tìm workflow "Bot Auto Commit"
   - Nhấn vào các lần chạy thất bại để xem log chi tiết

2. **Xác minh cấu trúc file:**
   ```
   .github/
   └── workflows/
       └── auto-commit.yml
   bot-auto-commit.py
   ```

3. **Test thủ công:**
   - Dùng nút "Run workflow" trong tab Actions
   - Kiểm tra xem chạy thủ công có hoạt động không (cho biết vấn đề lịch hay quyền)

## Ghi chú bảo mật

- Bot sử dụng user `github-actions[bot]` có sẵn của GitHub để commit
- Không nên bao gồm thông tin nhạy cảm trong file log
- Workflow chạy với quyền GitHub Actions tiêu chuẩn
