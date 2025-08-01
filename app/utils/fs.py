import os

def list_files(repo_path):
    return [
        os.path.join(dp, f)
        for dp, dn, filenames in os.walk(repo_path)
        for f in filenames
        if f.endswith((".js", ".ts", ".tsx", ".py"))  # Extend based on your stack
    ]

def read_file(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

def write_file(path, content):
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
