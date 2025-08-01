import difflib

def show_diff(original: str, modified: str) -> str:
    diff = difflib.unified_diff(
        original.splitlines(),
        modified.splitlines(),
        lineterm='',
        fromfile='original',
        tofile='modified'
    )
    return "\n".join(diff)
