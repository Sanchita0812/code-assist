from app.agents.steps.analyze_repo import analyze_repo
from app.agents.steps.plan_changes import plan_changes
from app.agents.steps.apply_edits import apply_edits
from .llm_utils import call_llm  # wrapper for GPT/Groq/Claude/Gemini

def run_prompt_chain(repo_path: str, prompt: str) -> dict:
    summary = analyze_repo(repo_path)
    plan = plan_changes(summary, prompt, call_llm)
    modified_files = apply_edits(repo_path, plan, call_llm)

    return {
        "summary": summary,
        "plan": plan,
        "modified_files": modified_files
    }
