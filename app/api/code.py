from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from app.schemas.request import CodeRequest
from app.services.git_service import clone_repo_sse

router = APIRouter()

@router.post("/code")
async def process_code(request_data: CodeRequest):
    repo_url = request_data.repoUrl
    return StreamingResponse(
        clone_repo_sse(repo_url),
        media_type="text/event-stream"
    )
