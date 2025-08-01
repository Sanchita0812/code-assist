import subprocess
import tempfile
from typing import Generator
from pydantic import HttpUrl  # only if you're explicitly using HttpUrl elsewhere

def clone_repo_sse(repo_url) -> Generator[str, None, None]:
    yield "event: message\ndata: Starting clone...\n\n"

    with tempfile.TemporaryDirectory() as tmpdirname:
        try:
            result = subprocess.run(
                ["git", "clone", str(repo_url), tmpdirname],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                check=True,
                text=True,
            )
            yield "event: message\ndata: Cloned to temp dir.\n\n"
        except subprocess.CalledProcessError as e:
            yield f"event: error\ndata: Git error: {e.stderr.strip()}\n\n"
            return

    yield "event: done\ndata: Cloning complete\n\n"
