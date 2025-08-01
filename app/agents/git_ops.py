import subprocess
import os
from datetime import datetime

def run_git_command(args, cwd):
    result = subprocess.run(["git"] + args, cwd=cwd, capture_output=True, text=True)
    if result.returncode != 0:
        raise Exception(f"Git error: {result.stderr}")
    return result.stdout.strip()

def create_timestamped_branch(repo_path: str, prefix: str = "ai-edits"):
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    branch_name = f"{prefix}-{timestamp}"
    run_git_command(["checkout", "-b", branch_name], cwd=repo_path)
    return branch_name

def create_branch(repo_path: str, branch: str):
    run_git_command(["checkout", "-b", branch], cwd=repo_path)

def commit_changes(repo_path: str, message: str = "AI: Applied code changes"):
    run_git_command(["add", "."], cwd=repo_path)
    run_git_command(["commit", "-m", message], cwd=repo_path)

def push_branch(repo_path: str, branch: str):
    run_git_command(["push", "origin", branch], cwd=repo_path)
