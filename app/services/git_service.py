import subprocess
import tempfile
import os
from typing import AsyncGenerator

async def clone_repo_to_temp(repo_url: str) -> str:
    """
    Clone a repository to a temporary directory.
    
    Args:
        repo_url: The URL of the repository to clone
        
    Returns:
        Path to the temporary directory containing the cloned repo
        
    Raises:
        Exception: If git clone fails
    """
    # Create a temporary directory that won't be automatically cleaned up
    temp_dir = tempfile.mkdtemp()
    
    try:
        result = subprocess.run(
            ["git", "clone", str(repo_url), temp_dir],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=True,
            text=True,
        )
        return temp_dir
    except subprocess.CalledProcessError as e:
        # Clean up the temp directory if clone fails
        import shutil
        shutil.rmtree(temp_dir, ignore_errors=True)
        raise Exception(f"Git clone failed: {e.stderr.strip()}")

def stream_clone_progress(repo_url: str) -> AsyncGenerator[str, None]:
    """
    Stream the progress of cloning a repository.
    
    Args:
        repo_url: The URL of the repository to clone
        
    Yields:
        Server-sent event formatted strings
    """
    async def _stream():
        yield "event: message\ndata: Starting clone...\n\n"
        
        try:
            temp_dir = await clone_repo_to_temp(repo_url)
            yield f"event: message\ndata: Cloned to {temp_dir}\n\n"
            yield f"event: done\ndata: {temp_dir}\n\n"
        except Exception as e:
            yield f"event: error\ndata: {str(e)}\n\n"
    
    return _stream()