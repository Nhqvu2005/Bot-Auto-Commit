# Bot Auto Commit

[![GitHub stars](https://img.shields.io/github/stars/Nhqvu2005/Bot-Auto-Commit?style=social)](https://github.com/Nhqvu2005/Bot-Auto-Commit/stargazers)
[![GitHub last commit](https://img.shields.io/github/last-commit/Nhqvu2005/Bot-Auto-Commit)](https://github.com/Nhqvu2005/Bot-Auto-Commit/commits/main)
[![License](https://img.shields.io/github/license/Nhqvu2005/Bot-Auto-Commit)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.9+-3776AB?style=flat&logo=python&logoColor=white)](https://www.python.org/)

> A Python script that automatically commits to your GitHub repository a user-defined number of times. Each iteration updates `log.txt` with a timestamp.

[English](README.md) · [Vietnamese](README.vi.md)

## ✨ Features

| Feature | Description |
|---------|-------------|
| 🔑 **Flexible Auth** | Read token from `GITHUB_TOKEN` env var or `token.txt` |
| 🤖 **Auto-detect** | Automatically detect repo owner from your token |
| ⏱️ **Rate Limit Protection** | Built-in 2-second delay between commits |
| 🌐 **GitHub Actions** | Includes workflow for automatic daily commits |
| 🔄 **Custom Branch** | Support for custom branch names |
| 👤 **Identity Control** | Attribute commits to your profile |

## 📋 Requirements

| Requirement | Version | Notes |
|-------------|---------|-------|
| Python | 3.9+ | [Download](https://www.python.org/downloads/) |
| GitHub Token | - | Fine-grained or Classic |

### Token Permissions

**Fine-grained token (recommended):**
- Repository access: select your repo
- Contents → Read and write
- Metadata → Read

**Classic token:**
- Public repo: `public_repo`
- Private repo: `repo`
- For org repos: `read:org`

## 🚀 Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

**requirements.txt:**
```text
python-dotenv>=1.0.1
```

### 2. Configure Token

**Option A - Environment Variable (recommended):**
```bash
export GITHUB_TOKEN="ghp_xxx_your_token_here"
```

**Option B - token.txt file:**
```bash
echo "ghp_xxx_your_token_here" > token.txt
```

### 3. Optional Configuration

Create `.env` file:
```env
REPO_NAME=Bot-Auto-Commit
REPO_BRANCH=main
REPO_OWNER=your_username  # Optional, auto-detected
```

### 4. Run

```bash
python bot-auto-commit.py
```

Enter how many times to update `log.txt`. Each update produces a commit.

## ⏰ Run Automatically on GitHub

This repo includes a GitHub Actions workflow at `.github/workflows/daily.yml` that runs daily at 00:00 UTC.

### Enable

1. Fork this repository
2. Go to **Actions** tab
3. Enable workflows
4. The workflow runs automatically or can be triggered manually

### Configure

| Variable | Description | Default |
|----------|-------------|---------|
| `TIMES` | Commits per run | 1 |
| `REPO_BRANCH` | Target branch | main |

### Attribute Commits to Your Profile

By default, commits use `github-actions[bot]`. To attribute to yourself:

```yaml
- name: Run bot-auto-commit
  env:
    AUTHOR_NAME: Your Name
    AUTHOR_EMAIL: yourusername@users.noreply.github.com
  run: python bot-auto-commit.py
```

Find your noreply email: GitHub → Settings → Emails

## 🔧 Customization

### Change Frequency

Edit `.github/workflows/daily.yml`:
```yaml
schedule:
  - cron: '0 10 * * *'  # 17:00 UTC+7
```

### Protected Branches

For protected branches, commit via a separate branch and open a PR:
```bash
export REPO_BRANCH="feature/temp"
# Then create PR manually
```

## 🧪 API Quick Check

Test your token permissions:
```bash
# Check auth
curl -H "Authorization: token $GITHUB_TOKEN" https://api.github.com/user

# Check repo access
curl -H "Authorization: token $GITHUB_TOKEN" \
  https://api.github.com/repos/{owner}/{repo}/contents/log.txt

# Create/update file
curl -X PUT -H "Authorization: token $GITHUB_TOKEN" \
  -d '{"message": "update", "content": "base64_content"}' \
  https://api.github.com/repos/{owner}/{repo}/contents/log.txt
```

## ⚠️ Notes

- Default 2-second delay between commits (rate limit protection)
- Adjust delay in `bot-auto-commit.py` if needed
- For private repos, ensure token has `repo` scope

---

README optimized with [Gingiris README Generator](https://gingiris.github.io/github-readme-generator/)
