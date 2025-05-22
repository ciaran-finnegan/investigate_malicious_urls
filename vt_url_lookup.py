#!/usr/bin/env python3
"""
Bulk-check a list of domains against VirusTotal reputation data.
Reads the VT API key from a .env file in the same directory.
"""

import os
import requests
from dotenv import load_dotenv
from urllib.parse import urlparse

# --------------------------------------------------------------------------- #
# 0. Load API key from .env
# --------------------------------------------------------------------------- #
load_dotenv()                              # reads .env into environment
API_KEY = os.getenv("VT_API_KEY")          # -> str | None

if not API_KEY:
    raise SystemExit("Error: VT_API_KEY not found in environment / .env file")

# --------------------------------------------------------------------------- #
# 1. Domains to check – now read from target_urls.txt
# --------------------------------------------------------------------------- #
URLS_FILE = "target_urls.txt"
with open(URLS_FILE, "r") as f:
    DOMAINS = []
    for line in f:
        line = line.strip()
        if not line or line.startswith("#"): continue
        parsed = urlparse(line)
        if parsed.hostname:
            DOMAINS.append(parsed.hostname)
        else:
            DOMAINS.append(line)  # fallback: treat as domain if not a URL

# --------------------------------------------------------------------------- #
# 2. Query VT and show a compact verdict per domain
# --------------------------------------------------------------------------- #
VT_ENDPOINT = "https://www.virustotal.com/api/v3/domains/{}"
HEADERS = {"x-apikey": API_KEY}

for dom in DOMAINS:
    try:
        r = requests.get(VT_ENDPOINT.format(dom), headers=HEADERS, timeout=15)
    except requests.RequestException as e:
        print(f"{dom:25}  ⚠️  connection error: {e}")
        continue

    if r.status_code != 200:
        print(f"{dom:25}  ⚠️  VT error {r.status_code}")
        continue

    stats = r.json()["data"]["attributes"]["last_analysis_stats"]
    mal, susp, harm = stats["malicious"], stats["suspicious"], stats["harmless"]

    if mal:
        verdict = "🚫 MALICIOUS"
    elif susp:
        verdict = "❓ SUSPICIOUS"
    else:
        verdict = "✅ Clean"

    print(f"{dom:25}  {verdict}  "
          f"(engines: {mal}⛔  {susp}⚠️  {harm}✅)")