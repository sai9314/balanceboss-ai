from fastapi import APIRouter, UploadFile, File, HTTPException
from services.parser import parse_csv
from datetime import datetime, timezone
import db
import io

router = APIRouter()


async def _insert_transactions(contents: bytes, kind: str) -> int:
    transactions = parse_csv(io.StringIO(contents.decode("utf-8")), kind=kind)
    docs = []
    for t in transactions:
        doc = t.model_dump()
        doc["date"] = datetime(doc["date"].year, doc["date"].month, doc["date"].day, tzinfo=timezone.utc)
        doc["uploaded_at"] = datetime.now(timezone.utc)
        docs.append(doc)
    if docs:
        collection = db.get_db()["transactions"]
        await collection.insert_many(docs)
    return len(docs)


@router.post("/sales")
async def upload_sales(file: UploadFile = File(...)):
    if not file.filename.endswith(".csv"):
        raise HTTPException(status_code=400, detail="Only CSV files are supported")
    count = await _insert_transactions(await file.read(), kind="sale")
    return {"uploaded": count, "type": "sales"}


@router.post("/expenses")
async def upload_expenses(file: UploadFile = File(...)):
    if not file.filename.endswith(".csv"):
        raise HTTPException(status_code=400, detail="Only CSV files are supported")
    count = await _insert_transactions(await file.read(), kind="expense")
    return {"uploaded": count, "type": "expenses"}
