#!/usr/bin/env python3

"""
x0Vision Tools - FFScouter to JSON script
Run this script once to fetch FFScouter estimated stats for all target list players.
Paste your FFScouter API key when prompted.
outputs JSON for whatever you want it for.
"""

import urllib.request, json, time

ALL_IDS = [***PUT ALL TORN IDs HERE SEPARATED BY COMMA - 123456, 654231, 7894561]
CHUNK   = 200  # stay under 205 limit

def fetch_chunk(ids, key):
    targets = ",".join(str(i) for i in ids)
    url = f"https://ffscouter.com/api/v1/get-stats?key={key}&targets={targets}"
    req = urllib.request.Request(url, headers={"User-Agent": "lolno"})
    with urllib.request.urlopen(req, timeout=15) as r:
        return json.loads(r.read())

def main():
    key = input("Paste your FFScouter API key (16 chars): ").strip()
    if len(key) != 16:
        print("Key must be 16 characters.")
        return

    results = {}
    chunks = [ALL_IDS[i:i+CHUNK] for i in range(0, len(ALL_IDS), CHUNK)]
    print(f"Fetching {len(ALL_IDS)} players in {len(chunks)} requests...")

    for i, chunk in enumerate(chunks):
        print(f"  Batch {i+1}/{len(chunks)}...")
        data = fetch_chunk(chunk, key)
        if isinstance(data, list):
            for entry in data:
                pid = entry.get("player_id")
                if pid:
                    results[pid] = {
                        "bs":  entry.get("bs_estimate"),
                        "bsh": entry.get("bs_estimate_human"),
                        "ff":  entry.get("fair_fight"),
                        "lu":  entry.get("last_updated"),
                    }
        elif isinstance(data, dict) and "error" in data:
            print(f"  API error: {data}")
            return
        if i < len(chunks) - 1:
            time.sleep(1)  # be polite

    print(f"\nFetched {len(results)} results.")
    print("\n--- COPY EVERYTHING BELOW THIS LINE ---")
    print(json.dumps(results))
    print("--- END ---")

if __name__ == "__main__":
    main()
