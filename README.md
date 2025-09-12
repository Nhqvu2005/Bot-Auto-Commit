# Bot Auto Commit

[README Tiếng Việt](README-auto-commit.vi.md)

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

1. Create the directory structure: `.github/workflows/`
2. Add the `auto-commit.yml` file with the workflow configuration above

### 2. Add the Python Script

1. Create `bot-auto-commit.py` in your repository root
2. Copy the Python code above into the file

### 3. Enable GitHub Actions

1. Go to your repository on GitHub
2. Navigate to **Actions** tab
3. Enable GitHub Actions if not already enabled
4. The workflow will automatically start running on the schedule

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

### Permission Issues
- Ensure the repository has write permissions for GitHub Actions
- Check if the workflow has the necessary permissions to push changes

### Python Script Errors
- Verify the Python script syntax is correct
- Check the Actions logs for any Python-related errors

## Security Notes

- The bot uses GitHub's built-in `github-actions[bot]` user for commits
- No sensitive information should be included in the log file
- The workflow runs with standard GitHub Actions permissions

## License

This project is open source and available under the [MIT License](LICENSE).
