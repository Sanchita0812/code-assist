from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from app.schemas.request import CodeRequest
from app.services.git_service import clone_repo_sse

router = APIRouter()

@router.post("/code")
def process_code(request_data: CodeRequest):
    repo_url = request_data.repoUrl

    def event_generator():
        for message in clone_repo_sse(repo_url):
            yield message

    return StreamingResponse(event_generator(), media_type="text/event-stream")
