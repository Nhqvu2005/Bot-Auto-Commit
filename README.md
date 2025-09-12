# Bot Auto Commit

[README Tiếng Việt](README.vi.md)

A simple automation bot that automatically commits changes to a repository on a daily schedule using GitHub Actions.

## Overview

This project consists of:
- A Python script (`bot-auto-commit.py`) that updates a log file with timestamps
- A GitHub Actions workflow (`.github/workflows/auto-commit.yml`) that runs the script daily and commits changes

## Features

- **Automated Daily Updates**: Runs every day at midnight UTC
- **Manual Trigger**: Can be triggered manually via GitHub Actions
- **Simple Logging**: Appends timestamp entries to `log.txt`
- **Automatic Git Operations**: Handles git add, commit, and push automatically

## Project Structure

```
├── .github/
│   └── workflows/
│       └── auto-commit.yml    # GitHub Actions workflow
├── bot-auto-commit.py         # Python script for updates
├── log.txt                    # Generated log file (auto-created)
└── README-auto-commit.md      # This file
```

## Files Description

### 1. GitHub Actions Workflow (`.github/workflows/auto-commit.yml`)

```yaml
name: Bot Auto Commit
on:
  schedule:
    - cron: '0 0 * * *'  # Runs daily at midnight UTC
  workflow_dispatch:     # Allows manual trigger

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

### 2. Python Script (`bot-auto-commit.py`)

```python
from datetime import datetime

with open("log.txt", "a") as file:
    file.write(f"Updated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
```

## Setup Instructions

### 1. Create the Workflow File

#### Method 1: Using GitHub Web Interface (Recommended)

**Step-by-step guide to create workflow file:**

1. **Navigate to Actions:**
   - Go to your repository on GitHub
   - Click on the **Actions** tab (next to Code, Issues, Pull requests)

2. **Create new workflow:**
   - If this is your first workflow, click **"I understand my workflows, go ahead and enable them"**
   - Click **"New workflow"** or **"set up a workflow yourself"**

3. **Edit the workflow file:**
   - GitHub will create a new file at `.github/workflows/main.yml`
   - You'll see a default template - delete all content
   - Copy and paste the complete workflow configuration from above

4. **Rename the file:**
   - Click on the filename `main.yml` in the editor
   - Change it to `auto-commit.yml`
   - Press Enter to confirm

5. **Commit the file:**
   - Click **"Start commit"**
   - Add a commit message like "Add auto-commit workflow"
   - Click **"Commit new file"**

**Visual guide:**
```
Actions tab → New workflow → Delete template → Paste our YAML → Rename file → Commit
```

#### Method 2: Using Local Git

1. Create the directory structure: `.github/workflows/`
2. Add the `auto-commit.yml` file with the workflow configuration above
3. Commit and push to your repository

### 2. Add the Python Script

1. Create `bot-auto-commit.py` in your repository root
2. Copy the Python code above into the file

### 3. Enable GitHub Actions and Set Permissions

#### Enable GitHub Actions

1. Go to your repository on GitHub
2. Navigate to **Actions** tab
3. If GitHub Actions is not enabled, click **"I understand my workflows, go ahead and enable them"**
4. The workflow will automatically start running on the schedule

#### Set Repository Permissions (Important!)

**For Public Repositories:**
- GitHub Actions automatically has read/write permissions
- No additional setup required

**For Private Repositories:**
1. Go to your repository **Settings** tab
2. Scroll down to **Actions** section in the left sidebar
3. Click on **General**
4. Under **"Workflow permissions"**, select:
   - ✅ **"Read and write permissions"** (required for auto-commit)
   - ✅ **"Allow GitHub Actions to create and approve pull requests"** (optional)
5. Click **Save**

#### Alternative: Use Personal Access Token (Advanced)

If you need more control, you can use a Personal Access Token:

1. Go to GitHub **Settings** → **Developer settings** → **Personal access tokens** → **Tokens (classic)**
2. Click **"Generate new token"**
3. Select scopes: `repo` (full control of private repositories)
4. Copy the token
5. Go to your repository **Settings** → **Secrets and variables** → **Actions**
6. Click **"New repository secret"**
7. Name: `GITHUB_TOKEN`, Value: your token
8. Update the workflow to use the secret:

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

### 4. Manual Trigger (Optional)

To manually trigger the bot:
1. Go to **Actions** tab in your repository
2. Select "Bot Auto Commit" workflow
3. Click "Run workflow" button
4. Choose the branch and click "Run workflow"

## How It Works

1. **Scheduled Execution**: GitHub Actions runs the workflow daily at midnight UTC
2. **Script Execution**: The Python script appends a timestamp entry to `log.txt`
3. **Git Operations**: The workflow commits the changes with an automated message
4. **Push Changes**: The changes are pushed back to the repository

## Generated Log Format

The `log.txt` file will contain entries like:
```
Updated on 2024-01-15 00:00:01
Updated on 2024-01-16 00:00:01
Updated on 2024-01-17 00:00:01
```

## Customization

### Change Schedule
Modify the cron expression in the workflow file:
- `'0 0 * * *'` - Daily at midnight UTC
- `'0 */6 * * *'` - Every 6 hours
- `'0 0 * * 1'` - Weekly on Monday

### Modify Log Content
Edit the Python script to change what gets written to the log:
```python
# Example: Add more information
with open("log.txt", "a") as file:
    file.write(f"Bot update: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - Status: OK\n")
```

### Change Commit Message
Modify the commit message in the workflow:
```bash
git commit -m "Daily automated update: $(date +'%Y-%m-%d %H:%M:%S')"
```

## Troubleshooting

### Workflow Not Running
- Check if GitHub Actions is enabled for your repository
- Verify the workflow file is in the correct location (`.github/workflows/`)
- Check the Actions tab for any error messages
- Ensure the cron schedule is valid (use [crontab.guru](https://crontab.guru) to verify)

### Permission Issues

**Common permission errors and solutions:**

1. **"Permission denied" when pushing:**
   ```
   Error: fatal: could not read Username for 'https://github.com': terminal prompts disabled
   ```
   **Solution:** Set repository permissions to "Read and write permissions" (see Setup section)

2. **"Resource not accessible by integration":**
   - Go to repository Settings → Actions → General
   - Under "Workflow permissions", select "Read and write permissions"
   - Click Save

3. **For private repositories:**
   - Ensure you've set the correct permissions in Settings
   - Consider using Personal Access Token method if issues persist

**How to check current permissions:**
1. Go to repository Settings
2. Scroll to Actions → General
3. Check "Workflow permissions" section
4. Should show "Read and write permissions" for auto-commit to work

### Python Script Errors
- Verify the Python script syntax is correct
- Check the Actions logs for any Python-related errors
- Ensure the script creates/modifies files in the repository root

### Debugging Steps

1. **Check workflow runs:**
   - Go to Actions tab
   - Look for "Bot Auto Commit" workflow
   - Click on failed runs to see detailed logs

2. **Verify file structure:**
   ```
   .github/
   └── workflows/
       └── auto-commit.yml
   bot-auto-commit.py
   ```

3. **Test manually:**
   - Use "Run workflow" button in Actions tab
   - Check if manual runs work (indicates schedule vs permission issues)

## Security Notes

- The bot uses GitHub's built-in `github-actions[bot]` user for commits
- No sensitive information should be included in the log file
- The workflow runs with standard GitHub Actions permissions

## License

This project is open source and available under the [MIT License](LICENSE).
