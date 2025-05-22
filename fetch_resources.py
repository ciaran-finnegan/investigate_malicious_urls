#!/usr/bin/env python3
"""
Fetch each site with a macOS/Chrome UA, save HTML + JS responses to disk.

Directory layout:
  output/
    example.com/
      index.html
      js/
        001_bootstrap.js
        002_main.js
"""

import os, re, pathlib, asyncio, hashlib
from urllib.parse import urlparse, urljoin

from playwright.async_api import async_playwright
from dotenv import load_dotenv

# --------------------------------------------------------------------------- #
# Read target URLs from file
# --------------------------------------------------------------------------- #
URLS_FILE = "target_urls.txt"
with open(URLS_FILE, "r") as f:
    DOMAINS = [line.strip() for line in f if line.strip() and not line.strip().startswith("#")]

UA_MAC_CHROME = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/124.0.0.0 Safari/537.36"
)

SAVE_DIR = pathlib.Path("output")
SAVE_DIR.mkdir(exist_ok=True)

JS_CT_RE = re.compile(r"(application|text)/(x-)?javascript", re.I)

# --------------------------------------------------------------------------- #
async def fetch_site(play, url: str):
    parsed = urlparse(url)
    folder = SAVE_DIR / parsed.hostname.replace(".", "_")
    (folder / "js").mkdir(parents=True, exist_ok=True)

    browser = await play.chromium.launch(headless=True)
    try:
        ctx = await browser.new_context(user_agent=UA_MAC_CHROME)
        page = await ctx.new_page()

        js_counter = 0

        async def save_response(resp):
            nonlocal js_counter
            ct = resp.headers.get("content-type", "")
            if JS_CT_RE.search(ct):
                js_counter += 1
                try:
                    body = await resp.body()
                except Exception as e:
                    print(f"[!] Error getting body for {resp.url}: {e}")
                    return
                name = f"{js_counter:03d}_{hashlib.sha1(body).hexdigest()[:10]}.js"
                (folder / "js" / name).write_bytes(body)
            elif resp.url == url:
                try:
                    (folder / "index.html").write_bytes(await resp.body())
                except Exception as e:
                    print(f"[!] Error getting main document body for {resp.url}: {e}")

        page.on("response", save_response)
        try:
            await page.goto(url, wait_until="domcontentloaded", timeout=60000)
        except Exception as e:
            print(f"[!] {url}  —  error: {e}")
        finally:
            await ctx.close()
    finally:
        await browser.close()

# --------------------------------------------------------------------------- #
async def main():
    async with async_playwright() as play:
        for site in DOMAINS:
            print(f"[*] Fetching {site}")
            await fetch_site(play, site)

asyncio.run(main())