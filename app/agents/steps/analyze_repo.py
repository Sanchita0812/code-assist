def analyze_repo(path: str) -> str:
    from app.utils.file_ops import get_file_tree, read_file
    readme = read_file(path, "README.md")
    file_tree = get_file_tree(path)
    return f"README:\n{readme}\n\nFile Tree:\n{file_tree}"
#Input: path to repo
#Action: Read README.md, file tree, and key files
#Output: Summary of the project