# BalanceBoss AI

> Your retail store's AI finance manager — upload a CSV, get instant P&L clarity and a chat agent that answers "why did I lose money last month?"

---

## The Problem

Small retail owners drown in receipts. They don't have a CFO, they don't want accounting software, and they definitely don't have time to reconcile sales against expenses every week. Mistakes go unnoticed, cash flow surprises kill momentum, and the only "analysis" they get is a stressed spreadsheet at tax season.

**BalanceBoss AI fixes this in under 60 seconds:**
- Drop in your sales CSV and expense CSV
- Get an instant reconciliation report with flagged discrepancies
- Ask plain-English questions and get direct answers backed by your own numbers

---

## How It Works

```
Upload CSV ──► FastAPI parser ──► MongoDB Atlas (persisted)
                                       │
                              Gemini 1.5 Pro agent
                                       │
                    ◄── Chat answer / reconciliation report
```

1. **Upload** — sales and expense CSVs are parsed, validated, and stored as structured documents in MongoDB Atlas
2. **Reconcile** — the service layer computes net P&L, flags categories where expenses exceed expected ratios, and surfaces month-over-month changes
3. **Chat** — a Gemini-powered agent receives the user's question plus a context snapshot of their financials and returns a plain-English answer with specific figures

---

## Tech Stack

| Layer | Technology | Why |
|---|---|---|
| Frontend | React 18 + Vite + React Router | Fast HMR, zero config, lightweight |
| Backend | FastAPI (Python 3.12) | Async-native, auto OpenAPI docs |
| AI Agent | Google Gemini 1.5 Pro | Long context window fits full financial history |
| Database | **MongoDB Atlas** | Flexible document model for variable CSV schemas |
| ODM / Driver | Motor (async) | Non-blocking Atlas queries in FastAPI |
| Container | Docker Compose | One-command local setup for judges |

---

## MongoDB Atlas Integration

MongoDB Atlas is the persistence backbone — not an afterthought.

### Why Atlas over a relational DB

Financial CSVs from different POS systems have inconsistent columns. A document model stores whatever columns arrive without a migration, and Atlas Search lets the AI agent query transactions by natural-language category names.

### What gets stored

**`transactions` collection** — one document per CSV row:

```json
{
  "_id": "ObjectId(...)",
  "date": "2024-03-01",
  "description": "Service Contract - Client X",
  "amount": 3500.00,
  "category": "service",
  "kind": "sale",
  "uploaded_at": "2024-05-27T10:32:00Z"
}
```

**`reports` collection** — one document per reconciliation run:

```json
{
  "_id": "ObjectId(...)",
  "generated_at": "2024-05-27T10:33:00Z",
  "total_sales": 16220.50,
  "total_expenses": 10650.95,
  "net": 5569.55,
  "discrepancies": [
    "Marketing spend up 9% vs prior month with no corresponding sales lift"
  ]
}
```

### Atlas features used

| Feature | Usage |
|---|---|
| Atlas Cluster (M0 free tier) | Stores all transactions and reconciliation reports |
| Motor async driver | All DB calls are non-blocking — no thread stalls under load |
| Indexes on `date` + `kind` | Fast aggregation for monthly P&L queries |
| Atlas connection string via env | `MONGO_URI` in `.env` — never hardcoded |

---

## Setup & Run

### Prerequisites

- Docker + Docker Compose, **or** Python 3.12 + Node 20
- [MongoDB Atlas account](https://www.mongodb.com/atlas) — free M0 cluster works
- Google Cloud project with the **Vertex AI API** enabled
- Application Default Credentials set up on your machine (one-time):

```bash
bash <(curl -sSL https://storage.googleapis.com/cloud-samples-data/adc/setup_adc.sh)
# or, if you have gcloud installed:
gcloud auth application-default login
```

### One-command (Docker)

```bash
git clone https://github.com/your-handle/balanceboss-ai
cd balanceboss-ai
cp .env.example .env        # paste your keys
docker compose up --build
```

| Service | URL |
|---|---|
| Frontend | http://localhost:5173 |
| Backend API | http://localhost:8000 |
| Interactive API docs | http://localhost:8000/docs |

### Local dev (no Docker)

**Backend**
```bash
cd backend
python -m venv .venv && source .venv/bin/activate
pip install -r ../requirements.txt
cp ../.env.example ../.env   # fill in GEMINI_API_KEY + MONGO_URI
uvicorn main:app --reload
```

**Frontend**
```bash
cd frontend
npm install
npm run dev
```

### Environment variables

```bash
# .env.example — no API keys; auth is handled by ADC
GOOGLE_CLOUD_PROJECT=your-gcp-project-id
GOOGLE_CLOUD_LOCATION=us-central1
MONGO_URI=mongodb+srv://<user>:<pass>@cluster0.mongodb.net
MONGO_DB=balanceboss
```

> **Auth note:** ADC credentials are read from `~/.config/gcloud/application_default_credentials.json` automatically. When running via Docker, `docker-compose.yml` mounts that file into the container — no secrets ever enter an image or env var.

---

## Demo

Sample CSVs are in `data/samples/` — ready to drag-and-drop on first launch:

| File | Contents |
|---|---|
| `sales_sample.csv` | 10 sale transactions, Q1 2024, 4 categories |
| `expenses_sample.csv` | 12 expense transactions, Q1 2024, 5 categories |

**Try these chat prompts after uploading:**
- *"What was my net profit in February?"*
- *"Which expense category grew the most month over month?"*
- *"Are my marketing costs justified by sales growth?"*

---

## License

MIT — see [LICENSE](LICENSE)
