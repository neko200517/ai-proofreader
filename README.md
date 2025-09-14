# AI Proofreader (MVP)

- Frontend: Next.js (SSG)
- Backend: FastAPI (local dev) → later Lambda via SAM
- Infra: SAM (API Gateway + Lambda), S3 + CloudFront (later)

## Dev

- Front: `cd frontend && npm run dev` → http://localhost:3000
- Back: `cd backend && uvicorn app.main:app --reload --port 8000` → /health
- Infra: `cd infra && sam build` (no deploy yet)
