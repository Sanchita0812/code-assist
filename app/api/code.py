from fastapi import APIRouter, Request
from fastapi.responses import StreamingResponse, JSONResponse
from app.schemas.request import CodeRequest
from app.services.git_service import clone_repo_sse, clone_repo_to_temp
from app.agents.prompt_chain import run_prompt_chain
import asyncio

router = APIRouter()

@router.post("/code/stream")
def stream_clone(request_data: CodeRequest):
    repo_url = request_data.repoUrl

    def event_generator():
        for message in clone_repo_sse(repo_url):
            yield message

    return StreamingResponse(event_generator(), media_type="text/event-stream")


@router.post("/code")
async def run_code_agent(req: CodeRequest):
    repo_path = await clone_repo_to_temp(req.repoUrl)
    result = run_prompt_chain(repo_path, req.prompt)
    return JSONResponse(content=result)
