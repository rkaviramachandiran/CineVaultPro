# 🎬 CineVault — Python / FastAPI Backend

A Python/FastAPI backend that proxies TMDB API calls server-side, keeping your API key out of the browser. Includes auto-generated interactive API docs at `/docs`.

> **Note:** I am using my full project in Antigravity IDE with AI.

---

## Project Structure

```
cinevault-python/
├── main.py              ← FastAPI app (all routes)
├── requirements.txt     ← Python dependencies
├── .env.example         ← Copy to .env with your TMDB key
└── public/
    └── index.html       ← CineVault frontend (served statically)
```

---

## Quick Start

### 1. Create a virtual environment
```bash
python -m venv venv
source venv/bin/activate        # macOS / Linux
venv\Scripts\activate           # Windows
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Set your TMDB API key
```bash
cp .env.example .env
# Edit .env:
# TMDB_API_KEY=your_tmdb_api_key_here
```
> Get a free key at https://www.themoviedb.org/settings/api

### 4. Run the server
```bash
# Development (auto-reload on file changes)
uvicorn main:app --reload --port 8000

# Production
uvicorn main:app --host 0.0.0.0 --port 8000
```

### 5. Open in browser
| URL | What |
|-----|------|
| `http://localhost:8000` | CineVault app |
| `http://localhost:8000/docs` | Interactive Swagger UI |
| `http://localhost:8000/redoc` | ReDoc API reference |

---

## API Endpoints

| Method | Route | Description |
|--------|-------|-------------|
| GET | `/api/health` | Server health check |
| GET | `/api/movies/discover` | Discover movies |
| GET | `/api/movies/search?query=` | Search movies |
| GET | `/api/series/discover` | Discover TV series |
| GET | `/api/series/search?query=` | Search TV series |
| GET | `/api/anime/discover` | Discover anime |
| GET | `/api/anime/search?query=` | Search anime |
| GET | `/api/tamil/discover` | Discover Tamil movies |
| GET | `/api/tamil/search?query=` | Search Tamil movies |
| GET | `/api/webseries/discover` | Discover web series |
| GET | `/api/webseries/search?query=` | Search web series |
| GET | `/api/movie/{id}` | Movie detail |
| GET | `/api/tv/{id}` | TV show detail |

### Common query parameters (discover routes)
| Param | Default | Description |
|-------|---------|-------------|
| `sort_by` | `popularity.desc` | TMDB sort field |
| `page` | `1` | Page number (≥ 1) |
| `with_genres` | — | Genre ID filter |

---

## Requirements

- Python **3.10+**
- A free [TMDB API key](https://www.themoviedb.org/settings/api)
