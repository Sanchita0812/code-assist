import os
import time
import tempfile
from urllib.parse import urlparse

from app.agents.git_ops import clone_repo, create_timestamped_branch, commit_changes, push_branch
from app.agents.pr_ops import create_pull_request
from app.agents.code_agent import run_prompt_on_repo  # You’ll need to implement this

def run_code_edit_flow(repo_url: str, prompt: str) -> str:
    # Parse repo info
    parsed = urlparse(repo_url)
    path_parts = parsed.path.strip("/").split("/")
    if len(path_parts) < 2:
        raise ValueError("Invalid GitHub URL")
    owner, repo = path_parts[0], path_parts[1].replace(".git", "")

    # Temp clone directory
    with tempfile.TemporaryDirectory() as tmpdir:
        repo_path = os.path.join(tmpdir, repo)
        clone_repo(repo_url, repo_path)

        # Create timestamped branch
        timestamp = time.strftime("%Y%m%d-%H%M%S")
        branch_name = f"ai-edits-{timestamp}"
        create_timestamped_branch(repo_path, branch_name)

        # Run AI agent on repo
        run_prompt_on_repo(repo_path, prompt)  # Implement this to apply AI changes

        # Commit and push changes
        commit_changes(repo_path, message=f"AI: {prompt}")
        push_branch(repo_path, branch_name)

        # Create PR
        pr_url = create_pull_request(
            owner=owner,
            repo=repo,
            head=branch_name,
            title=f"AI: {prompt} [{timestamp}]",
            body=f"This PR includes AI-generated code changes based on the prompt: '{prompt}'"
        )

        return pr_url
