from fastapi import APIRouter, Depends
from app.schemas import ChatRequest, ChatResponse
from app.deps import get_toolkit
from app.services.chat_service import chat_reply, new_conversation_id

router = APIRouter(prefix="/chat", tags=["chat"])

@router.post("", response_model=ChatResponse)
def chat(req: ChatRequest, toolkit=Depends(get_toolkit)):
    reply = chat_reply(req.message, toolkit)
    conv_id = new_conversation_id(req.conversation_id)
    # TODO: persist conversation/messages if you enable DB
    return ChatResponse(conversation_id=conv_id, reply=reply)
