import os
import shutil
import subprocess
import tempfile
from typing import Generator

def clone_repo_sse(repo_url: str) -> Generator[str, None, None]:
    yield "event: message\ndata: Cloning repo...\n\n"

    with tempfile.TemporaryDirectory() as tmpdirname:
        try:
            result = subprocess.run(
                ["git", "clone", repo_url, tmpdirname],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                check=True,
                text=True,
            )
            yield f"event: message\ndata: Cloned repo to {tmpdirname}\n\n"
        except subprocess.CalledProcessError as e:
            yield f"event: error\ndata: Failed to clone repo: {e.stderr}\n\n"
            return
