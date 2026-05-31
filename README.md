# 📊 Portfolio Analyzer

A GitHub Portfolio Analyzer that connects to your GitHub account, analyzes selected repositories, and generates a professional CV/portfolio report with real engineering depth.

## Tech Stack

| Layer           | Technology                                      |
| --------------- | ----------------------------------------------- |
| **Frontend**    | Next.js 14 (App Router) + Tailwind CSS          |
| **Backend**     | FastAPI + Python 3.12                            |
| **Queue**       | Celery + Redis                                  |
| **Database**    | PostgreSQL 16 + SQLAlchemy (async)               |
| **Vector Store**| Qdrant                                           |
| **Code Parser** | Tree-sitter                                      |
| **Embeddings**  | BGE-M3 (sentence-transformers)                   |
| **LLM**         | Anthropic Claude (claude-sonnet-4-20250514) / Ollama fallback |
| **Auth**        | GitHub OAuth → JWT                               |

## Repository Structure

```
portfolio-analyzer/
├── apps/
│   ├── web/                # Next.js frontend
│   └── api/                # FastAPI backend
├── workers/                # Celery workers
├── docker/
│   ├── docker-compose.yml  # Local dev services (Postgres, Redis, Qdrant)
│   └── .env.example        # Environment variable template
├── scripts/
│   ├── seed_test_repos.sh  # Seed test data
│   └── verify.sh           # Infrastructure health check
└── README.md
```

## Quick Start

### 1. Configure Environment

```bash
cp docker/.env.example docker/.env
# Edit docker/.env and fill in your secrets (GITHUB_CLIENT_ID, ANTHROPIC_API_KEY, etc.)
```

### 2. Start Infrastructure

```bash
docker compose -f docker/docker-compose.yml up -d
```

This starts:
- **PostgreSQL 16** on `localhost:5432` (db=`portfolio`, user=`dev`, password=`dev`)
- **Redis 7** on `localhost:6379`
- **Qdrant** on `localhost:6333`

### 3. Verify Services

```bash
chmod +x scripts/verify.sh
./scripts/verify.sh
```

You should see `OK` for each service. If any show `FAIL`, make sure Docker Compose is running.

### 4. Start the API

```bash
cd apps/api
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

The API will be available at [http://localhost:8000](http://localhost:8000) and docs at [http://localhost:8000/docs](http://localhost:8000/docs).

### 5. Start the Frontend

```bash
cd apps/web
npm install
npm run dev
```

The frontend will be available at [http://localhost:3000](http://localhost:3000).

## Development

### Running Celery Workers

```bash
cd workers
celery -A tasks worker --loglevel=info
```

### Environment Variables

See [`docker/.env.example`](docker/.env.example) for the full list of required environment variables.

| Variable               | Description                                    |
| ---------------------- | ---------------------------------------------- |
| `DATABASE_URL`         | PostgreSQL async connection string              |
| `REDIS_URL`            | Redis connection URL                            |
| `QDRANT_URL`           | Qdrant REST API URL                             |
| `GITHUB_CLIENT_ID`     | GitHub OAuth App client ID                      |
| `GITHUB_CLIENT_SECRET` | GitHub OAuth App client secret                  |
| `JWT_SECRET_KEY`       | Secret key for JWT token signing                |
| `TOKEN_ENCRYPTION_KEY` | Key for encrypting stored tokens                |
| `LLM_PROVIDER`         | `anthropic` or `ollama`                         |
| `ANTHROPIC_API_KEY`    | Anthropic API key (if using Claude)             |
| `OLLAMA_BASE_URL`      | Ollama server URL (if using Ollama)             |
| `NEXT_PUBLIC_API_URL`  | Backend API URL visible to the browser          |
| `NEXTAUTH_SECRET`      | NextAuth.js session secret                      |
| `NEXTAUTH_URL`         | Canonical URL for NextAuth.js                   |

## License

See [LICENSE](LICENSE) for details.