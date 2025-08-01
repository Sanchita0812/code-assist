# app/agent/code_agent.py

import os
from app.agents.llm_utils import call_llm  # This should wrap your LLM calls (e.g., OpenAI, Claude)
from app.utils.fs import list_files, read_file, write_file  # Utility functions you should define

def run_prompt_on_repo(repo_path: str, prompt: str) -> dict:
    # Step 1: List files
    all_files = list_files(repo_path)

    # Step 2: Read content of all files
    codebase = {path: read_file(path) for path in all_files}

    # Step 3: Generate plan + changes using LLM
    llm_input = f"You are an AI coding agent. User prompt: {prompt}\n\nCodebase files:\n" + "\n".join(all_files)
    response = call_llm(llm_input)

    # Step 4: Parse response and apply edits
    modified_files = []
    for file in response.get("edits", []):
        file_path = os.path.join(repo_path, file["path"])
        write_file(file_path, file["new_content"])
        modified_files.append(file["path"])

    return {
        "modified_files": modified_files,
        "plan": response.get("plan", ""),
        "summary": response.get("summary", "")
    }
