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
    
    Args:
        req: CodeRequest containing repo URL and prompt
        
    Returns:
        JSON response with modified files and pull request URL
    """
    temp_dir = None
    try:
        # Clone repository
        repo_path = await clone_repo_to_temp(req.repoUrl)
        temp_dir = repo_path
        
        branch_name = "ai-generated-edits"
        
        # Create new branch
        create_branch(repo_path, branch_name)
        
        # Run the prompt chain to analyze and modify code
        result = run_prompt_chain(repo_path, req.prompt)
        
        # Commit and push changes
        commit_changes(repo_path, "AI: Applied edits to improve functionality")
        push_branch(repo_path, branch_name)
        
        # Parse repo owner/name and create PR
        owner, repo = parse_repo_owner_and_name(str(req.repoUrl))
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
        # Clean up temporary directory
        if temp_dir and os.path.exists(temp_dir):
            shutil.rmtree(temp_dir, ignore_errors=True)

def parse_repo_owner_and_name(url: str) -> tuple[str, str]:
    """
    Parse GitHub repository URL to extract owner and repo name.
    
    Args:
        url: GitHub repository URL
        
    Returns:
        Tuple of (owner, repo_name)
        
    Examples:
        https://github.com/user/repo.git -> ("user", "repo")
        https://github.com/user/repo -> ("user", "repo")
    """
    # Remove .git suffix and split by /
    clean_url = url.rstrip(".git")
    parts = clean_url.split("/")
    
    if len(parts) < 2:
        raise ValueError(f"Invalid GitHub URL format: {url}")
    
    return parts[-2], parts[-1]