import db
from models.report import ReconciliationReport


async def reconcile() -> ReconciliationReport:
    collection = db.get_db()["transactions"]

    # Aggregate totals and per-category breakdown in one pass
    pipeline = [
        {
            "$group": {
                "_id":   {"kind": "$kind", "category": "$category"},
                "total": {"$sum": "$amount"},
            }
        }
    ]

    sales_by_cat: dict[str, float] = {}
    expense_by_cat: dict[str, float] = {}

    async for doc in collection.aggregate(pipeline):
        kind     = doc["_id"]["kind"]
        category = doc["_id"]["category"]
        total    = doc["total"]
        if kind == "sale":
            sales_by_cat[category] = total
        else:
            expense_by_cat[category] = total

    total_sales    = sum(sales_by_cat.values())
    total_expenses = sum(expense_by_cat.values())

    discrepancies: list[str] = []
    for category, expense in expense_by_cat.items():
        revenue = sales_by_cat.get(category, 0.0)
        if expense > revenue and revenue > 0:
            discrepancies.append(
                f"'{category}': expenses (${expense:,.2f}) exceed sales (${revenue:,.2f})"
            )
        elif revenue == 0 and expense > 0:
            discrepancies.append(
                f"'{category}': ${expense:,.2f} in expenses with no matching sales"
            )

    return ReconciliationReport(
        total_sales=round(total_sales, 2),
        total_expenses=round(total_expenses, 2),
        net=round(total_sales - total_expenses, 2),
        discrepancies=discrepancies,
    )
