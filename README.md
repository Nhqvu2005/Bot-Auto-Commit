# 🤖 Bot Auto Commit

[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg?style=for-the-badge&logo=python)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/License-MIT-green.svg?style=for-the-badge)](LICENSE)
[![GitHub stars](https://img.shields.io/github/stars/Nhqvu2005/Bot-Auto-Commit?style=for-the-badge&logo=github)](https://github.com/Nhqvu2005/Bot-Auto-Commit/stargazers)
[![GitHub Actions](https://img.shields.io/badge/GitHub_Actions-Ready-brightgreen?style=for-the-badge&logo=github-actions)](.github/workflows/daily.yml)

> Automate GitHub commits with a simple Python script — perfect for activity streaks, contribution graphs, and scheduled updates.

[English](README.md) · [Vietnamese](README.vi.md)

<!-- TOC -->
- [Features](#-features)
- [Quick Start](#-quick-start)
- [Configuration](#-configuration)
- [GitHub Actions](#-github-actions)
- [Token Setup](#-token-setup)
- [FAQ](#-faq)

---

## ✨ Features

| Feature | Description |
|---------|-------------|
| **Token Flexibility** | Reads from `GITHUB_TOKEN` env var or `token.txt` |
| **Auto-Detection** | Automatically detects repo owner from token |
| **Branch Support** | Works with `main`, `master`, or custom branches |
| **GitHub Actions** | Includes ready-to-use workflow for daily automation |
| **Configurable Count** | Set how many commits to make per run |
| **Attribution Control** | Customize author name and email for contributions |

---

## 🚀 Quick Start

### 1. Clone & Install

```bash
git clone https://github.com/Nhqvu2005/Bot-Auto-Commit.git
cd Bot-Auto-Commit
pip install -r requirements.txt
```

### 2. Configure Token

**Option A: Environment Variable (Recommended)**

```bash
# Linux/macOS
export GITHUB_TOKEN="ghp_xxx_your_token_here"

# Windows PowerShell
$env:GITHUB_TOKEN="ghp_xxx_your_token_here"
```

**Option B: Token File**

Create `token.txt` in the same folder with your token:

```
ghp_xxx_your_token_here
```

### 3. Run

```bash
python bot-auto-commit.py
```

The script will:
1. Read your token and auto-detect your GitHub username
2. Ask how many times to update `log.txt`
3. Create a commit for each update (with 2-second delay between commits)

---

## ⚙️ Configuration

### Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `GITHUB_TOKEN` | *(required)* | Your GitHub personal access token |
| `REPO_OWNER` | *(auto-detected)* | Override repo owner |
| `REPO_NAME` | `Bot-Auto-Commit` | Target repository name |
| `REPO_BRANCH` | `main` | Target branch |

### Example: Custom Configuration

```bash
# Windows PowerShell
$env:REPO_NAME="MyActivityRepo"
$env:REPO_BRANCH="master"
python bot-auto-commit.py
```

---

## 🔄 GitHub Actions

This repo includes a ready-to-use workflow at `.github/workflows/daily.yml`.

### Enable

1. Fork this repository
2. Go to **Actions** tab → Enable GitHub Actions
3. The workflow runs daily at **00:00 UTC**

### Configure Schedule

Edit `.github/workflows/daily.yml`:

```yaml
on:
  schedule:
    # Run at 17:00 Vietnam time (UTC+7)
    - cron: '0 10 * * *'
```

### Set Commit Count

In the workflow, modify:

```yaml
- name: Run bot-auto-commit
  env:
    GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
    TIMES: 1  # Number of commits per run
```

### Attribution (Optional)

Want commits attributed to you instead of `github-actions[bot]`?

```yaml
- name: Run bot-auto-commit
  env:
    GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
    AUTHOR_NAME: "Your Name"
    AUTHOR_EMAIL: "you@example.com"
```

Find your noreply email: **GitHub → Settings → Emails → Copy address ending with `@users.noreply.github.com`**

---

## 🔑 Token Setup

### Required Permissions

| Token Type | Permissions Needed |
|------------|-------------------|
| **Fine-grained** (Recommended) | Repository: Contents → Read and write; Metadata → Read |
| **Classic (Public)** | `public_repo` scope |
| **Classic (Private)** | `repo` scope |
| **Org Repos** | Also requires `read:org` |

### Quick Permission Check

Test your token with these endpoints:

```bash
# Should return your user info
curl -H "Authorization: token $GITHUB_TOKEN" \
  https://api.github.com/user

# Should return repo contents
curl -H "Authorization: token $GITHUB_TOKEN" \
  https://api.github.com/repos/OWNER/REPO/contents/log.txt

# Should create/update a file
curl -X PUT -H "Authorization: token $GITHUB_TOKEN" \
  -d '{"message":"test", "content":"dGVzdA=="}' \
  https://api.github.com/repos/OWNER/REPO/contents/test.txt
```

---

## ❓ FAQ

**Q: Rate limits?**
> The script adds a 2-second delay between commits to avoid GitHub API rate limits.

**Q: Protected branches?**
> Can't push directly to protected branches. Use another branch and open a PR.

**Q: Private repos?**
> Use a token with `repo` scope (not `public_repo`).

**Q: Wrong attribution?**
> Set `AUTHOR_NAME` and `AUTHOR_EMAIL` in your environment or GitHub Actions.

---

## 📄 License

MIT License — feel free to use and modify.

---

*README optimized with [Gingiris README Generator](https://gingiris.github.io/github-readme-generator/)*
