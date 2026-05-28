from fastapi import APIRouter
from services.reconciliation import reconcile
import db

router = APIRouter()


@router.get("/summary")
async def summary():
    collection = db.get_db()["transactions"]
    pipeline = [
        {
            "$group": {
                "_id": "$kind",
                "total": {"$sum": "$amount"},
            }
        }
    ]
    totals = {doc["_id"]: doc["total"] async for doc in collection.aggregate(pipeline)}
    sales    = totals.get("sale", 0.0)
    expenses = totals.get("expense", 0.0)
    return {
        "total_sales":    round(sales, 2),
        "total_expenses": round(expenses, 2),
        "net":            round(sales - expenses, 2),
    }


@router.get("/reconcile")
async def reconcile_report():
    return await reconcile()


@router.get("/by-category")
async def by_category():
    collection = db.get_db()["transactions"]
    pipeline = [
        {
            "$group": {
                "_id":   {"kind": "$kind", "category": "$category"},
                "total": {"$sum": "$amount"},
                "count": {"$sum": 1},
            }
        },
        {"$sort": {"total": -1}},
    ]
    return [
        {
            "kind":     doc["_id"]["kind"],
            "category": doc["_id"]["category"],
            "total":    round(doc["total"], 2),
            "count":    doc["count"],
        }
        async for doc in collection.aggregate(pipeline)
    ]
