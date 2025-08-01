from app.agents.steps.analyze_repo import analyze_repo
from app.agents.steps.plan_changes import plan_changes
from app.agents.steps.apply_edits import apply_edits
from .llm_utils import call_llm  # wrapper for GPT/Groq/Claude/Gemini
import re
def run_prompt_chain(repo_path: str, prompt: str) -> dict:
    summary = analyze_repo(repo_path)
    plan = plan_changes(summary, prompt, call_llm)
    modified_files = apply_edits(repo_path, plan, call_llm)

    return {
        "summary": summary,
        "plan": plan,
        "modified_files": modified_files
    }
def extract_files_from_plan(plan: str) -> list[str]:
    # Naive example: assume each line starts with filename:
    return [line.split(":")[0].strip() for line in plan.splitlines() if line.strip().endswith(".py")]

def get_change_for_file(file: str, plan: str) -> str:
    pattern = re.compile(rf"{re.escape(file)}:(.*)", re.IGNORECASE)
    for line in plan.splitlines():
        match = pattern.match(line)
        if match:
            return match.group(1).strip()
    return "No specific change found."