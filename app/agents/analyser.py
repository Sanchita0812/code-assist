import os
from app.utils.file_utils import list_python_files, read_file, save_json, load_json  # ✅ Make sure load_json is here
from app.agents.llm_utils import summarize_code  # ✅ Should return a string summary of a code block

def analyze_repo(repo_path: str, use_cache=True) -> dict:
    cache_path = os.path.join(repo_path, 'repo_map.json')
    
    # Use cache if it exists
    if use_cache and os.path.exists(cache_path):
        return load_json(cache_path)

    repo_map = {}
    py_files = list_python_files(repo_path)

    for path in py_files:
        try:
            code = read_file(path)
            summary = summarize_code(code)
            rel_path = os.path.relpath(path, repo_path)

            repo_map[rel_path] = {
                "summary": summary,
                "lines": len(code.splitlines())
            }

        except Exception as e:
            print(f"Error processing {path}: {e}")
    
    save_json(cache_path, repo_map)
    return repo_map
