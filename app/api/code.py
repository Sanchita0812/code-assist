from fastapi import APIRouter, Request
from fastapi.responses import StreamingResponse
from app.schemas.request import CodeRequest
from app.utils.sse import stream_events

router = APIRouter()

@router.post("/code")
async def process_code(request_data: CodeRequest):
    return StreamingResponse(stream_events(), media_type="text/event-stream")
