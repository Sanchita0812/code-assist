import os
from app.utils.file_utils import read_file, write_file
from app.utils.diff_utils import show_diff

def apply_edit(file_path: str, new_content: str, show_changes: bool = True):
    old_content = read_file(file_path)

    if show_changes:
        diff = show_diff(old_content, new_content)
        print(f"Changes in {file_path}:\n{diff}\n")

    write_file(file_path, new_content)

def apply_edits(repo_path: str, plan: str, llm) -> list[str]:
    from app.agents.prompt_chain import extract_files_from_plan, get_change_for_file

    modified_files = []

    for rel_path in extract_files_from_plan(plan):
        abs_path = os.path.join(repo_path, rel_path)
        old_code = read_file(abs_path)

        change_prompt = f"""You're modifying `{rel_path}`.

Old Code:
{old_code}

Planned Change:
{get_change_for_file(rel_path, plan)}

Return ONLY the complete updated file code."""
        new_code = llm(change_prompt)
        apply_edit(abs_path, new_code)
        modified_files.append(rel_path)

    return modified_files
