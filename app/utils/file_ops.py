import os

def get_file_tree(path: str) -> str:
    tree = ""
    for root, dirs, files in os.walk(path):
        level = root.replace(path, '').count(os.sep)
        indent = '  ' * level
        tree += f"{indent}{os.path.basename(root)}/\n"
        for f in files:
            tree += f"{indent}  {f}\n"
    return tree

def read_file(path: str, filename: str) -> str:
    full_path = os.path.join(path, filename)
    try:
        with open(full_path, 'r') as f:
            return f.read()
    except FileNotFoundError:
        return ""

def write_file(path: str, filename: str, content: str):
    full_path = os.path.join(path, filename)
    with open(full_path, 'w') as f:
        f.write(content)
