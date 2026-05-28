from contextlib import asynccontextmanager
from dotenv import load_dotenv
load_dotenv()  # loads ../.env before any other import reads os.environ

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes import upload, chat, analytics
import db


@asynccontextmanager
async def lifespan(app: FastAPI):
    await db.connect()
    yield
    await db.close()


app = FastAPI(title="BalanceBoss AI", version="1.0.0", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(upload.router, prefix="/api/upload", tags=["upload"])
app.include_router(chat.router, prefix="/api/chat", tags=["chat"])
app.include_router(analytics.router, prefix="/api/analytics", tags=["analytics"])


@app.get("/health")
async def health():
    await db.get_client().admin.command("ping")
    return {"status": "ok"}
