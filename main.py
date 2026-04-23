import os
from datetime import datetime, timezone
from typing import Optional

import httpx
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from dotenv import load_dotenv

load_dotenv()

# ── Config ────────────────────────────────────────────────────────────────────
TMDB_KEY  = os.getenv("TMDB_API_KEY")
if not TMDB_KEY:
    raise ValueError("Missing TMDB_API_KEY in environment variables.")

TMDB_BASE = "https://api.tmdb.org/3"
WEB_NETWORKS = "213|1024|453|2739|2552|49|3353"   # Netflix, Prime, Disney+, etc.

# ── App ───────────────────────────────────────────────────────────────────────
app = FastAPI(
    title="CineVault API",
    description="Python/FastAPI proxy for TMDB — keeps your API key server-side.",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["GET"],
    allow_headers=["*"],
)

# ── TMDB helper ───────────────────────────────────────────────────────────────
async def tmdb_get(path: str, params: dict) -> dict:
    """Fetch from TMDB, injecting the API key and stripping None/empty values."""
    clean = {k: v for k, v in params.items() if v is not None and v != ""}
    clean["api_key"] = TMDB_KEY

    async with httpx.AsyncClient(timeout=30.0) as client:
        r = await client.get(f"{TMDB_BASE}{path}", params=clean)

    if r.status_code != 200:
        raise HTTPException(status_code=r.status_code, detail=r.text)
    return r.json()


# ── Health ────────────────────────────────────────────────────────────────────
@app.get("/api/health", tags=["Meta"])
async def health():
    return {"status": "ok", "timestamp": datetime.now(timezone.utc).isoformat()}


# ── Movies ────────────────────────────────────────────────────────────────────
@app.get("/api/movies/discover", tags=["Movies"])
async def movies_discover(
    sort_by: str = Query("popularity.desc"),
    page: int = Query(1, ge=1),
    with_genres: Optional[str] = None,
):
    return await tmdb_get("/discover/movie", {
        "sort_by": sort_by,
        "page": page,
        "with_genres": with_genres,
        "vote_count.gte": 50,
        "include_adult": "false",
    })


@app.get("/api/movies/search", tags=["Movies"])
async def movies_search(
    query: str = Query(..., min_length=1),
    page: int = Query(1, ge=1),
):
    return await tmdb_get("/search/movie", {
        "query": query,
        "page": page,
        "include_adult": "false",
    })


# ── TV Series ─────────────────────────────────────────────────────────────────
@app.get("/api/series/discover", tags=["Series"])
async def series_discover(
    sort_by: str = Query("popularity.desc"),
    page: int = Query(1, ge=1),
    with_genres: Optional[str] = None,
):
    return await tmdb_get("/discover/tv", {
        "sort_by": sort_by,
        "page": page,
        "with_genres": with_genres,
        "vote_count.gte": 20,
        "include_adult": "false",
    })


@app.get("/api/series/search", tags=["Series"])
async def series_search(
    query: str = Query(..., min_length=1),
    page: int = Query(1, ge=1),
):
    return await tmdb_get("/search/tv", {
        "query": query,
        "page": page,
        "include_adult": "false",
    })


# ── Anime ─────────────────────────────────────────────────────────────────────
@app.get("/api/anime/discover", tags=["Anime"])
async def anime_discover(
    sort_by: str = Query("popularity.desc"),
    page: int = Query(1, ge=1),
    with_genres: Optional[str] = None,
):
    # Anime = Japanese language + Animation (16), plus optional extra genre
    genre_param = (
        f"16,{with_genres}"
        if with_genres and with_genres not in ("0", "16")
        else "16"
    )
    return await tmdb_get("/discover/tv", {
        "sort_by": sort_by,
        "page": page,
        "with_genres": genre_param,
        "with_original_language": "ja",
        "vote_count.gte": 20,
        "include_adult": "false",
    })


@app.get("/api/anime/search", tags=["Anime"])
async def anime_search(
    query: str = Query(..., min_length=1),
    page: int = Query(1, ge=1),
):
    return await tmdb_get("/search/tv", {
        "query": query,
        "page": page,
        "include_adult": "false",
    })


# ── Tamil Cinema ──────────────────────────────────────────────────────────────
@app.get("/api/tamil/discover", tags=["Tamil"])
async def tamil_discover(
    sort_by: str = Query("popularity.desc"),
    page: int = Query(1, ge=1),
    with_genres: Optional[str] = None,
):
    return await tmdb_get("/discover/movie", {
        "sort_by": sort_by,
        "page": page,
        "with_genres": with_genres,
        "with_original_language": "ta",
        "vote_count.gte": 5,
        "include_adult": "false",
    })


@app.get("/api/tamil/search", tags=["Tamil"])
async def tamil_search(
    query: str = Query(..., min_length=1),
    page: int = Query(1, ge=1),
):
    return await tmdb_get("/search/movie", {
        "query": query,
        "page": page,
        "include_adult": "false",
    })


# ── Web Series ────────────────────────────────────────────────────────────────
@app.get("/api/webseries/discover", tags=["Web Series"])
async def webseries_discover(
    sort_by: str = Query("popularity.desc"),
    page: int = Query(1, ge=1),
    with_genres: Optional[str] = None,
):
    return await tmdb_get("/discover/tv", {
        "sort_by": sort_by,
        "page": page,
        "with_genres": with_genres,
        "with_networks": WEB_NETWORKS,
        "vote_count.gte": 20,
        "include_adult": "false",
    })


@app.get("/api/webseries/search", tags=["Web Series"])
async def webseries_search(
    query: str = Query(..., min_length=1),
    page: int = Query(1, ge=1),
):
    return await tmdb_get("/search/tv", {
        "query": query,
        "page": page,
        "include_adult": "false",
    })


# ── Detail pages ──────────────────────────────────────────────────────────────
@app.get("/api/movie/{movie_id}", tags=["Detail"])
async def movie_detail(movie_id: int):
    return await tmdb_get(f"/movie/{movie_id}", {"append_to_response": "credits"})


@app.get("/api/tv/{tv_id}", tags=["Detail"])
async def tv_detail(tv_id: int):
    return await tmdb_get(f"/tv/{tv_id}", {"append_to_response": "credits"})


# ── Trailers ──────────────────────────────────────────────────────────────────
@app.get("/api/trailer/{media_type}/{media_id}", tags=["Trailer"])
async def get_trailer(media_type: str, media_id: int):
    """Return the best YouTube trailer URL for a movie or TV show."""
    if media_type not in ("movie", "tv"):
        raise HTTPException(status_code=400, detail="media_type must be 'movie' or 'tv'")

    data = await tmdb_get(f"/{media_type}/{media_id}/videos", {})
    videos = data.get("results", [])

    # Prefer official YouTube Trailers, fall back to Teasers
    for vtype in ("Trailer", "Teaser"):
        for v in videos:
            if v.get("site") == "YouTube" and v.get("type") == vtype:
                return {
                    "youtube_key": v["key"],
                    "youtube_url": f"https://www.youtube.com/watch?v={v['key']}",
                    "name": v.get("name", ""),
                    "type": v.get("type", ""),
                }

    raise HTTPException(status_code=404, detail="No YouTube trailer found for this title.")


# ── Serve frontend (must be last) ─────────────────────────────────────────────
app.mount("/", StaticFiles(directory="public", html=True), name="static")
