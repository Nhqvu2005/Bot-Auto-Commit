## Bot Auto Commit

English documentation. For Vietnamese, see [README.vi.md](README.vi.md).

### Overview
This Python script updates `log.txt` in a GitHub repository a user-defined number of times. Each iteration wipes the file and writes a single timestamp line, committing via the GitHub REST API.

### Features
- Reads GitHub token from `GITHUB_TOKEN` env var or `token.txt`.
- Auto-detects repo owner for `Bot-Auto-Commit` via the token (override with env vars).
- Overwrites `log.txt` and commits to the specified branch, repeated N times.

### Requirements
- Python 3.9+
- A valid GitHub token
- Permissions:
  - Fine‑grained token (recommended):
    - Repository access: select `Bot-Auto-Commit`
    - Repository permissions: Contents → Read and write; Metadata → Read
  - Classic token:
    - Public repo: `public_repo`
    - Private repo: `repo`
    - If listing private org repos: `read:org`

### Setup
1) Install dependencies:
```bash
pip install -r requirements.txt
```
`requirements.txt` minimal content:
```text
python-dotenv>=1.0.1
```

2) Configure token:
- Env var (recommended):
```powershell
$env:GITHUB_TOKEN="ghp_xxx_your_token_here"
```
- Or create `token.txt` (same folder) with the token on one line.

3) Optional `.env` file:
```env
REPO_NAME=Bot-Auto-Commit
REPO_BRANCH=main
```

### Usage
Run the script:
```powershell
python .\bot-auto-commit.py
```
- The script auto-detects `owner` using your token. To force a value, set `REPO_OWNER`.
- Enter how many times to update `log.txt`. Each update produces a commit.

#### Customization
- If your default branch is `master`:
```powershell
$env:REPO_BRANCH="master"
```
- If the repo name differs from `Bot-Auto-Commit`:
```powershell
$env:REPO_NAME="AnotherRepoName"
```

### Token quick check
- Try:
  - `GET /user`
  - `GET /repos/{owner}/{repo}/contents/log.txt`
  - `PUT /repos/{owner}/{repo}/contents/log.txt`
- If you get 403/404 due to permissions, use Classic `repo` scope or Fine‑grained Contents: Read and write.

### Notes
- For protected branches, commit via another branch and open a PR.
- The script sleeps 2 seconds between commits to avoid rate limits; adjust as needed.
