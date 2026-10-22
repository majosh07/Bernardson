import json, time
import requests
from bs4 import BeautifulSoup   # pip install requests beautifulsoup4
import re

HEADERS = {"User-Agent": "Mozilla/5.0"}

# def resolve(page_url: str) -> str | None:
#     r = requests.get(page_url, headers=HEADERS, timeout=15)
#     print(r)
#     r.raise_for_status()
#     soup = BeautifulSoup(r.text, "html.parser")
#     tag = soup.find("meta", property="og:image")
#     if tag and tag.get("content"):
#         return tag["content"]
#     # fallback: the img inside your .Gif container
#     box = soup.select_one(".Gif img")
#     return box["src"] if box else None

with open("gifs.json", encoding="utf-8") as f:
    gifs = json.load(f)

PATTERN = re.compile(r"tenor\.com/(?:m/)?([^/]+)/[^/]+\.gif$")

fixed, failed = 0, []
for g in gifs:
    old = g.get("media_url")
    m = PATTERN.search(old) if old else None
    if not m:          # resumable: skip ones already done
        failed.append(g["id"])
        continue
    g["media_url"] = f"https://c.tenor.com/{m.group(1)}/tenor.gif"    
    fixed += 1


with open("gifs.json", "w", encoding="utf-8") as f:   # save as you go
    json.dump(gifs, f, indent=2)
print(f"rewrote {fixed}, couldn't parse {len(failed)}: {failed}")
