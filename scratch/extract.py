import json

with open("scratch/all_providers_debug.json", "r", encoding="utf-8") as f:
    providers = json.load(f)

for p in providers:
    if "max" in p["provider_name"].lower():
        print(f"{p['provider_name']}: {p['provider_id']} ({p['logo_path']})")
