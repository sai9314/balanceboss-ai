from fastapi import APIRouter
from pydantic import BaseModel
from agents.financial_agent import ask_agent

router = APIRouter()


class ChatRequest(BaseModel):
    question: str
    context: str = ""


@router.post("/")
async def chat(req: ChatRequest):
    answer = ask_agent(req.question, req.context)
    return {"answer": answer}
