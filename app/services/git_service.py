import os
import shutil
import subprocess
import tempfile
from typing import Generator

def clone_repo_sse(repo_url: str) -> Generator[str, None, None]:
    yield "event: message\ndata: 🔄 Starting repo clone...\n\n"

    # Create a temporary directory
    try:
        temp_dir = tempfile.mkdtemp(prefix="backspace_")
        yield f"event: message\ndata: 📁 Cloning into temp folder: {temp_dir}\n\n"

        result = subprocess.run(
            ["git", "clone", repo_url, temp_dir],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

        if result.returncode == 0:
            yield "event: message\ndata: ✅ Repo cloned successfully.\n\n"
        else:
            yield f"event: error\ndata: ❌ Failed to clone repo. Error:\n{result.stderr}\n\n"

    except Exception as e:
        yield f"event: error\ndata: ❌ Exception during cloning: {str(e)}\n\n"

    finally:
        # (optional for debug: keep it) - otherwise clean it up
        # shutil.rmtree(temp_dir)
        pass
