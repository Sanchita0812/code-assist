from app.utils.file_ops import read_file, write_file
from app.agents.plan_parser import extract_files_from_plan, get_change_for_file

def apply_edits(path: str, plan: str, llm) -> list[str]:
    modified_files = []
    for file in extract_files_from_plan(plan):
        old_code = read_file(path, file)
        code_prompt = f"""You're modifying `{file}`.

Old Code:
{old_code}

Planned Change:
{get_change_for_file(file, plan)}

Return the new code."""
        new_code = llm(code_prompt)
        write_file(path, file, new_code)
        modified_files.append(file)
    return modified_files
