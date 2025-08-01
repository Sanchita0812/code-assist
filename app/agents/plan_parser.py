import re

def extract_files_from_plan(plan: str) -> list[str]:
    pattern = r"- ([\w./]+\.py)"
    return re.findall(pattern, plan)

def get_change_for_file(file: str, plan: str) -> str:
    lines = plan.splitlines()
    changes = []

    capture = False
    for line in lines:
        if line.strip().startswith(f"- {file}"):
            capture = True
            changes.append(line)
        elif capture:
            if line.strip().startswith("- ") and not line.strip().startswith(f"- {file}"):
                break
            changes.append(line)
    return "\n".join(changes)
