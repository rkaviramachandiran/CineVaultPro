import os
import httpx
import json
from dotenv import load_dotenv

load_dotenv()

TMDB_KEY = os.getenv("TMDB_API_KEY")
TMDB_BASE = "https://api.tmdb.org/3"

async def get_all_providers():
    async with httpx.AsyncClient() as client:
        results = {}
        for ptype in ["movie", "tv"]:
            r = await client.get(f"{TMDB_BASE}/watch/providers/{ptype}", params={
                "api_key": TMDB_KEY,
                "watch_region": "IN"
            })
            providers = r.json().get("results", [])
            for p in providers:
                results[p["provider_id"]] = p
        
        with open("scratch/all_providers_debug.json", "w", encoding="utf-8") as f:
            json.dump(list(results.values()), f, indent=2)

if __name__ == "__main__":
    import asyncio
    asyncio.run(get_all_providers())
