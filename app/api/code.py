from fastapi import APIRouter
from fastapi.responses import JSONResponse
from app.schemas.request import CodeRequest
from app.services.git_service import clone_repo_to_temp
from app.agents.prompt_chain import run_prompt_chain
from app.agents.git_ops import create_branch, commit_changes, push_branch
from app.agents.pr_ops import create_pull_request
import os
import tempfile
import shutil

router = APIRouter()


@router.post("/code/agent")
async def run_code_agent(req: CodeRequest):
    """
    Main endpoint to run the code agent on a repository.
    """
    temp_dir = None
    try:
        # Step 1: Clone repo
        repo_path = await clone_repo_to_temp(req.repoUrl)
        temp_dir = repo_path

        # Step 2: Create a timestamped branch
        branch_name = generate_timestamped_branch_name("ai-edits")
        create_branch(repo_path, branch_name)

        # Step 3: Apply prompt chain
        result = run_prompt_chain(repo_path, req.prompt)

        # Step 4: Commit + push
        commit_changes(repo_path, "AI: Applied edits to improve functionality")
        push_branch(repo_path, branch_name)

        # Step 5: Create PR
        owner, repo = parse_repo_owner_and_name(req.repoUrl)
        pr_url = create_pull_request(owner, repo, branch_name)

        return JSONResponse(content={
            "modified": result.get("modified_files", []),
            "pull_request": pr_url,
            "plan": result.get("plan", ""),
            "summary": result.get("summary", "")
        })

    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"error": f"Failed to process request: {str(e)}"}
        )
    finally:
        if temp_dir and os.path.exists(temp_dir):
            shutil.rmtree(temp_dir, ignore_errors=True)


@router.post("/code")  # Optional alias
async def run_code_agent_alias(req: CodeRequest):
    return await run_code_agent(req)


def parse_repo_owner_and_name(url: str) -> tuple[str, str]:
    """
    Extracts owner and repo name from a GitHub URL.
    """
    clean_url = url.rstrip(".git")
    parts = clean_url.split("/")

    if len(parts) < 2:
        raise ValueError(f"Invalid GitHub URL format: {url}")

    return parts[-2], parts[-1]


def generate_timestamped_branch_name(prefix: str = "ai-edits") -> str:
    from datetime import datetime
    ts = datetime.now().strftime("%Y%m%d-%H%M%S")
    return f"{prefix}-{ts}"
