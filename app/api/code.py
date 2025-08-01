# app/api/code_agent.py

from fastapi import APIRouter
from fastapi.responses import JSONResponse
from app.schemas.request import CodeRequest
from app.services.git_service import clone_repo_to_temp
from app.agents.prompt_chain import run_prompt_chain
from app.agents.steps.apply_edits import apply_edits
from app.agents.git_ops import create_branch, commit_changes, push_branch
from app.agents.pr_ops import create_pull_request
import os

router = APIRouter()

@router.post("/code/agent")
async def run_code_agent(req: CodeRequest):
    repo_path = await clone_repo_to_temp(req.repoUrl)
    branch_name = "ai-generated-edits"

    create_branch(repo_path, branch_name)

    # Plan + Edit
    plan = run_prompt_chain(repo_path, req.prompt)
    from app.agents.llm_utils import gemini_llm
    modified_files = apply_edits(repo_path, plan, gemini_llm)

    # Commit & push
    commit_changes(repo_path, "AI: Applied edits to improve functionality")
    push_branch(repo_path, branch_name)

    # Parse repo owner/name
    owner, repo = parse_repo_owner_and_name(req.repoUrl)

    pr_url = create_pull_request(owner, repo, branch_name)

    return JSONResponse(content={"modified": modified_files, "pull_request": pr_url})


def parse_repo_owner_and_name(url: str) -> tuple[str, str]:
    # Example: https://github.com/user/repo.git
    parts = url.rstrip(".git").split("/")
    return parts[-2], parts[-1]
