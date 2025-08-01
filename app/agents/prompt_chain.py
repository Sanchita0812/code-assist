from app.agents.analyser import analyze_repo
from app.agents.steps.plan_changes import plan_changes
from app.agents.steps.apply_edits import apply_edits
from app.agents.llm_utils import call_llm
import re

def run_prompt_chain(repo_path: str, prompt: str) -> dict:
    """
    Run the complete prompt chain: analyze -> plan -> apply
    
    Args:
        repo_path: Path to the repository
        prompt: User's prompt for changes
        
    Returns:
        Dictionary containing summary, plan, and modified files
    """
    summary = analyze_repo(repo_path)
    plan = plan_changes(summary, prompt, call_llm)
    modified_files = apply_edits(repo_path, plan, call_llm)

    return {
        "summary": summary,
        "plan": plan,
        "modified_files": modified_files
    }

def extract_files_from_plan(plan: str) -> list[str]:
    """
    Extract Python file paths from the plan text.
    
    Args:
        plan: The plan text containing file references
        
    Returns:
        List of Python file paths found in the plan
    """
    # Look for patterns like "- filename.py" or "filename.py:"
    patterns = [
        r"- ([\w./]+\.py)",  # Lines starting with "- filename.py"
        r"([\w./]+\.py):",   # Lines with "filename.py:"
        r"`([\w./]+\.py)`",  # Files in backticks
    ]
    
    files = []
    for pattern in patterns:
        files.extend(re.findall(pattern, plan))
    
    # Remove duplicates while preserving order
    return list(dict.fromkeys(files))

def get_change_for_file(file: str, plan: str) -> str:
    """
    Extract the specific changes planned for a given file.
    
    Args:
        file: The filename to look for
        plan: The plan text
        
    Returns:
        The change description for the file
    """
    lines = plan.splitlines()
    changes = []
    capture = False
    
    for line in lines:
        # Start capturing when we find the file
        if file in line and (line.strip().startswith(f"- {file}") or line.strip().startswith(f"{file}:")):
            capture = True
            changes.append(line)
        elif capture:
            # Stop capturing when we hit another file or section
            if (line.strip().startswith("- ") and ".py" in line and file not in line) or \
               (line.strip().endswith(".py:") and file not in line):
                break
            changes.append(line)
    
    return "\n".join(changes) if changes else f"No specific change found for {file}."