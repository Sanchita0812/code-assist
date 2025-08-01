# app/agents/code_agent.py

import os
from app.agents.llm_utils import call_llm  # Wraps your LLM (OpenAI, Claude, etc.)
from app.utils.fs import list_files, read_file, write_file  # Utility functions to list, read, write files

def run_prompt_on_repo(repo_path: str, prompt: str) -> dict:
    # Step 1: List all files in the repo
    all_files = list_files(repo_path)

    # Step 2: Read content of all files
    codebase = {path: read_file(path) for path in all_files}

    # Step 3: Build LLM input with prompt and file list
    llm_input = (
        f"You are an AI coding assistant. Perform the following task on the repo:\n"
        f"'{prompt}'\n\n"
        f"The codebase contains the following files:\n" +
        "\n".join(all_files) +
        "\n\nSuggest edits as a list of JSON objects with 'path' and 'new_content'. Optionally, provide a 'plan' and 'summary'."
    )

    # Step 4: Query the LLM
    response = call_llm(llm_input)

    # Step 5: Apply edits
    modified_files = []
    for file in response.get("edits", []):
        file_path = os.path.join(repo_path, file["path"])
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        write_file(file_path, file["new_content"])
        modified_files.append(file["path"])

    # Step 6: Return useful metadata
    return {
        "modified_files": modified_files,
        "plan": response.get("plan", ""),
        "summary": response.get("summary", "")
    }
