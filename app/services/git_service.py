import subprocess
import tempfile
from typing import Generator

def clone_repo_sse(repo_url: str) -> Generator[str, None, None]:
    yield "event: message\ndata: Starting clone...\n\n"

    with tempfile.TemporaryDirectory() as tmpdirname:
        try:
            result = subprocess.run(
                ["git", "clone", repo_url, tmpdirname],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                check=True,
                text=True,
            )
            yield f"event: message\ndata: Cloned to temp dir.\n\n"
        except subprocess.CalledProcessError as e:
            yield f"event: error\ndata: Git error: {e.stderr}\n\n"
            return  # Exit early on error

    yield "event: done\ndata: Cloning complete\n\n"
