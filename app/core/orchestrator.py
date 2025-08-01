import os
import time
import tempfile
from urllib.parse import urlparse

from e2b_code_interpreter import Sandbox

from app.agents.git_ops import clone_repo, create_timestamped_branch, commit_changes, push_branch
from app.agents.pr_ops import create_pull_request
from app.agents.code_agent import run_prompt_on_repo  # your existing logic, updated for sandbox use

def run_code_edit_flow(repo_url: str, prompt: str) -> str:
    # Parse GitHub info
    parsed = urlparse(repo_url)
    path_parts = parsed.path.strip("/").split("/")
    if len(path_parts) < 2:
        raise ValueError("Invalid GitHub URL")
    owner, repo = path_parts[0], path_parts[1].replace(".git", "")

    # Use temp directory to clone repo
    with tempfile.TemporaryDirectory() as tmpdir:
        local_repo_path = os.path.join(tmpdir, repo)
        clone_repo(repo_url, local_repo_path)

        # Create timestamped branch locally
        timestamp = time.strftime("%Y%m%d-%H%M%S")
        branch_name = f"ai-edits-{timestamp}"
        create_timestamped_branch(local_repo_path, branch_name)

        # Start sandbox
        sandbox = Sandbox()

        try:
            # Copy repo into sandbox (optional: compress + extract for large repos)
            sandbox.upload(local_repo_path, remote_path="/sandbox/repo")
            sandbox.run_code("cd /sandbox/repo")

            # Run AI agent to edit code in sandbox
            run_prompt_on_repo(sandbox, "/sandbox/repo", prompt)

            # Download changes back to local repo path
            sandbox.download(remote_path="/sandbox/repo", local_path=local_repo_path)

        finally:
            sandbox.kill()

        # Commit, push, and create PR
        commit_changes(local_repo_path, message=f"AI: {prompt}")
        push_branch(local_repo_path, branch_name)

        pr_url = create_pull_request(
            owner=owner,
            repo=repo,
            head=branch_name,
            title=f"AI: {prompt} [{timestamp}]",
            body=f"This PR includes AI-generated code changes based on the prompt: '{prompt}'"
        )

        return pr_url
