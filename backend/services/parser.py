import csv
from io import StringIO
from models.transaction import Transaction


def parse_csv(fileobj: StringIO, kind: str) -> list[Transaction]:
    reader = csv.DictReader(fileobj)
    transactions = []
    for row in reader:
        transactions.append(
            Transaction(
                date=row["date"],
                description=row.get("description", ""),
                amount=float(row["amount"]),
                category=row.get("category", "uncategorized"),
                kind=kind,
            )
        )
    return transactions
