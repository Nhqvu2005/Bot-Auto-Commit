from urllib.parse import urlencode
import os
import sys
import base64
import json
import time
from datetime import datetime
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError
from dotenv import load_dotenv

GITHUB_API = "https://api.github.com"  # Base URL của GitHub REST API

def read_github_token() -> str:
    """Đọc GitHub token từ biến môi trường hoặc file token.txt

    Ưu tiên lấy từ biến môi trường `GITHUB_TOKEN`. Nếu không có, đọc từ file
    `token.txt` (cùng thư mục script). Nếu không tìm thấy, thoát với thông báo lỗi.
    """
    token = os.environ.get("GITHUB_TOKEN")
    if token:
        return token.strip()
    if os.path.exists("token.txt"):
        with open("token.txt", "r", encoding="utf-8") as f:
            return f.read().strip()
    print("Lỗi: Không tìm thấy token. Hãy đặt biến môi trường GITHUB_TOKEN hoặc tạo file token.txt", file=sys.stderr)
    sys.exit(1)

def github_request(method: str, url: str, token: str, data: dict | None = None) -> tuple[int, dict | str]:
    """Gửi request tới GitHub API với header xác thực.

    - method: "GET" | "PUT" | ...
    - url: endpoint đầy đủ
    - token: PAT (personal access token)
    - data: payload (sẽ được JSON encode nếu có)
    Trả về (status_code, body_json_or_text)
    """
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
        "User-Agent": "bot-auto-commit-script"
    }
    body = None
    if data is not None:
        body = json.dumps(data).encode("utf-8")
        headers["Content-Type"] = "application/json"

    req = Request(url, data=body, headers=headers, method=method)
    try:
        with urlopen(req) as resp:
            status = resp.getcode()
            content_type = resp.headers.get("Content-Type", "")
            raw = resp.read()
            if "application/json" in content_type:
                return status, json.loads(raw.decode("utf-8"))
            return status, raw.decode("utf-8")
    except HTTPError as e:
        # Trả về body lỗi (JSON nếu có) để tiện debug
        try:
            err_body = e.read().decode("utf-8")
            try:
                return e.code, json.loads(err_body)
            except Exception:
                return e.code, err_body
        except Exception:
            return e.code, ""
    except URLError as e:
        print(f"Lỗi mạng: {e}", file=sys.stderr)
        sys.exit(1)

def get_file_sha(owner: str, repo: str, path: str, token: str, branch: str = "main") -> str | None:
    """Lấy SHA hiện tại của file để cập nhật nội dung qua API.

    - Nếu file tồn tại: trả về sha (dùng để PUT cập nhật).
    - Nếu file chưa tồn tại: trả về None (API sẽ tạo mới khi không có sha).
    """
    url = f"{GITHUB_API}/repos/{owner}/{repo}/contents/{path}?ref={branch}"
    status, resp = github_request("GET", url, token)
    if status == 200 and isinstance(resp, dict):
        return resp.get("sha")
    if status == 404:
        return None
    print(f"Lỗi lấy SHA ({status}): {resp}", file=sys.stderr)
    sys.exit(1)

def put_file_content(owner: str, repo: str, path: str, content_text: str, commit_message: str, token: str, branch: str = "main"):
    """Ghi đè toàn bộ nội dung file bằng `content_text` và tạo commit.

    API `PUT /repos/{owner}/{repo}/contents/{path}` yêu cầu nội dung base64.
    Nếu `sha` được cung cấp, đó là update; nếu không, sẽ tạo file mới.
    """
    sha = get_file_sha(owner, repo, path, token, branch)
    content_b64 = base64.b64encode(content_text.encode("utf-8")).decode("utf-8")
    url = f"{GITHUB_API}/repos/{owner}/{repo}/contents/{path}"
    author_name = os.environ.get("AUTHOR_NAME")
    author_email = os.environ.get("AUTHOR_EMAIL")
    payload = {
    "message": commit_message,
    "content": content_b64,
    "branch": branch
    }
    if author_name and author_email:
        payload["author"] = {"name": author_name, "email": author_email}
        payload["committer"] = {"name": author_name, "email": author_email}
    if sha:
        payload["sha"] = sha
    status, resp = github_request("PUT", url, token, payload)
    if status in (200, 201):
        return resp
    print(f"Lỗi cập nhật file ({status}): {resp}", file=sys.stderr)
    sys.exit(1)

def load_env():
    """Nạp biến môi trường từ file .env (nếu có)."""
    load_dotenv()

def main():
    # Token trước (dùng cho auto detect)
    token = read_github_token()

    # Cấu hình repo: ưu tiên biến môi trường của GitHub Actions
    # GITHUB_REPOSITORY có dạng owner/repo
    gh_repo = os.environ.get("GITHUB_REPOSITORY") or ""
    owner_from_env = os.environ.get("REPO_OWNER")
    name_from_env = os.environ.get("REPO_NAME")
    parsed_owner = gh_repo.split("/")[0] if "/" in gh_repo else None
    parsed_name = gh_repo.split("/")[1] if "/" in gh_repo else None

    repo_name = name_from_env or parsed_name or "Bot-Auto-Commit"
    if owner_from_env:
        repo_owner = owner_from_env
    elif parsed_owner:
        # Trên GitHub Actions, dùng owner từ GITHUB_REPOSITORY để tránh gọi /user
        repo_owner = parsed_owner
    else:
        # Local: tự phát hiện owner bằng token
        repo_owner = auto_detect_owner(token, repo_name)

    branch = os.environ.get("REPO_BRANCH") or "main"  # Đổi nếu repo dùng "master"
    path_in_repo = "log.txt"

    # Số lần sửa (tạo commit). Mỗi lần sẽ ghi 1 dòng timestamp, xoá hết nội dung cũ.
    times_env = os.environ.get("TIMES")
    if times_env is not None:
        try:
            times = int(times_env)
        except Exception:
            print("TIMES không hợp lệ. Vui lòng đặt TIMES là số nguyên.", file=sys.stderr)
            sys.exit(1)
    else:
        try:
            times = int(input("Nhập số lần sửa file log.txt: ").strip())
        except Exception:
            print("Giá trị không hợp lệ. Vui lòng nhập số nguyên.", file=sys.stderr)
            sys.exit(1)
    if times <= 0:
        print("Số lần phải > 0.", file=sys.stderr)
        sys.exit(1)

    for i in range(1, times + 1):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        line = f"{timestamp} — log updated ({i}/{times})\n"
        commit_message = f"chore: update log.txt at {timestamp} ({i}/{times})"
        resp = put_file_content(
            owner=repo_owner,
            repo=repo_name,
            path=path_in_repo,
            content_text=line,          # Ghi đè toàn bộ nội dung chỉ 1 dòng thời gian
            commit_message=commit_message,
            token=token,
            branch=branch
        )
        print(f"Đã commit {i}/{times}: {resp.get('commit', {}).get('sha', '')}")
        # Nghỉ nhẹ để tránh giới hạn tốc độ/abuse (có thể giảm xuống 1-2s)
        time.sleep(2)

def auto_detect_owner(token: str, repo_name: str) -> str:
    """Tự động xác định owner của repo bằng token.

    B1: Lấy username từ /user
    B2: Kiểm tra repo có thuộc user này không
    B3: Nếu không, duyệt tất cả repos mà token có quyền truy cập để tìm owner
    """
    # 1) Lấy username của token
    status, me = github_request("GET", f"{GITHUB_API}/user", token)
    if status != 200 or not isinstance(me, dict) or "login" not in me:
        print(f"Lỗi lấy user từ token ({status}): {me}", file=sys.stderr)
        sys.exit(1)
    candidate = me["login"]

    # 2) Thử repo thuộc user cá nhân
    status, _ = github_request("GET", f"{GITHUB_API}/repos/{candidate}/{repo_name}", token)
    if status == 200:
        return candidate

    # 3) Nếu không, tìm trong tất cả repos mà token truy cập được
    page = 1
    while True:
        q = urlencode({"per_page": 100, "page": page, "visibility": "all", "affiliation": "owner,collaborator,organization_member"})
        status, repos = github_request("GET", f"{GITHUB_API}/user/repos?{q}", token)
        if status != 200 or not isinstance(repos, list):
            print(f"Lỗi liệt kê repos ({status}): {repos}", file=sys.stderr)
            sys.exit(1)
        if not repos:
            break
        for r in repos:
            if r.get("name") == repo_name:
                return r.get("owner", {}).get("login", candidate)
        page += 1

    print(f"Không tìm thấy repo '{repo_name}' với token hiện tại.", file=sys.stderr)
    sys.exit(1)
if __name__ == "__main__":
    load_env()
    main()
