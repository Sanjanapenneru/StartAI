# GRAMAI

**GRAMAI – AI-Powered Hyper-Local Business Advisor & Smart Scheme Calculator**

> Plan your business before you borrow.

GRAMAI transforms the existing StartAI multi-agent foundation into a Smart India
Hackathon 2026 prototype for rural and semi-urban entrepreneurs. A user enters
their location, margin capital, and business category. GRAMAI returns a
prototype market brief, feasibility score, deterministic financing plan, scheme
recommendation, repayment information, risks, and next steps.

## What is implemented

- Entrepreneur assessment for village, block, district, state, capital, and business category.
- LangGraph pipeline:
  - Market Intelligence Agent
  - Business Feasibility Agent
  - Competitor & Opportunity Agent
  - Finance Agent
  - Scheme Recommendation Agent
- Deterministic finance and scheme rules; Gemini cannot override them.
- Quarterly repayment schedule and clearly labelled **Illustrative Monthly EMI**.
- Prototype market dataset with transparent estimate labels.
- Gemini integration with deterministic **Prototype Demo Mode** fallback.
- React flow from landing page → assessment → analysis → financial planner → final recommendation.
- Print-friendly final report.
- English UI with Telugu and Hindi selector scaffolding.
- Optional browser speech input when supported.

## Financial rules

| Rule | Micro Finance Scheme | Term Loan |
|---|---:|---:|
| Project cost | Up to ₹1,40,000 | More than ₹1,40,000 and up to ₹50,00,000 |
| Maximum loan | ₹1,25,000 | ₹45,00,000 |
| Interest | 6.5% p.a. | 8% p.a. |
| Repayment | 3 years | 7 years |
| Moratorium | 3 months | 6 months |

The backend calculates:

```text
Project cost = available margin capital / 0.10
Calculated financing = project cost × 0.90
Supported loan = min(calculated financing, scheme maximum)
```

Projects above ₹50,00,000 are not assigned an unsupported scheme.

## Architecture

```text
React + Vite
  ↓
FastAPI /api endpoints
  ↓
LangGraph EntrepreneurContext
  ├─ Market Intelligence
  ├─ Business Feasibility
  ├─ Competitor & Opportunity
  ├─ Deterministic Finance
  └─ Deterministic Scheme Recommendation
  ↓
SQLAlchemy + PostgreSQL (or local SQLite demo fallback)
```

## Environment variables

Copy the templates:

```bash
cp backend/.env.example backend/.env
cp frontend/.env.example frontend/.env
```

Backend:

- `DATABASE_URL` — PostgreSQL connection string. If omitted, local demo mode uses `gramai_demo.db`.
- `GEMINI_API_KEY` — optional. Missing or failed Gemini automatically uses Prototype Demo Mode.
- `GEMINI_MODEL` — optional Gemini model name.
- `FIREBASE_SERVICE_ACCOUNT_JSON` or `FIREBASE_SERVICE_ACCOUNT_PATH` — optional for authenticated legacy routes.

Frontend:

- `VITE_API_BASE_URL`
- `VITE_FIREBASE_API_KEY`
- `VITE_FIREBASE_AUTH_DOMAIN`
- `VITE_FIREBASE_PROJECT_ID`
- `VITE_FIREBASE_STORAGE_BUCKET`
- `VITE_FIREBASE_MESSAGING_SENDER_ID`
- `VITE_FIREBASE_APP_ID`
- `VITE_FIREBASE_MEASUREMENT_ID`

No credentials belong in source control. The original public StartAI repository
contained a database credential in source history; rotate that credential in
the database provider and use a replacement value only through environment
variables.

## Run locally or in Replit

### Backend

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload --host 0.0.0.0 --port 8007
```

Health check:

```bash
curl http://localhost:8007/api/health
```

### Frontend

```bash
cd frontend
npm install
npm run dev -- --host 0.0.0.0
```

Set `VITE_API_BASE_URL` to the backend URL used by the frontend.

## API

- `GET /api/health`
- `POST /api/assessment`
- `POST /api/analyze`
- `POST /api/financial-plan`
- `POST /api/recommend-scheme`
- `GET /api/assessment/{id}`

The GRAMAI assessment endpoints permit unauthenticated demo requests when
Firebase is not configured. Supplied Firebase bearer tokens are still verified;
production deployments should configure authentication and protect the routes
according to their deployment policy.

## Required demo checks

- ₹10,000 capital → ₹1,00,000 project cost → ₹90,000 supported financing → Micro Finance Scheme.
- ₹1,00,000 capital → ₹10,00,000 project cost → ₹9,00,000 supported financing → Term Loan.
- Project cost above ₹50,00,000 → no supported scheme recommendation.

All market insights in this prototype are seeded demo data or AI-generated
estimates. They are not official government statistics or live competitor data.