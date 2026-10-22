import json, time
import requests
from bs4 import BeautifulSoup   # pip install requests beautifulsoup4

HEADERS = {"User-Agent": "Mozilla/5.0"}

def resolve(page_url: str) -> str | None:
    r = requests.get(page_url, headers=HEADERS, timeout=15)
    print(r)
    r.raise_for_status()
    soup = BeautifulSoup(r.text, "html.parser")
    tag = soup.find("meta", property="og:image")
    if tag and tag.get("content"):
        return tag["content"]
    # fallback: the img inside your .Gif container
    box = soup.select_one(".Gif img")
    return box["src"] if box else None

with open("gifs.json", encoding="utf-8") as f:
    gifs = json.load(f)

for g in gifs:
    if g.get("media_url"):          # resumable: skip ones already done
        continue
    try:
        g["media_url"] = resolve(g["url"])
    except Exception as e:
        print("FAILED", g["id"], g["url"], e)
        continue
    if not g["media_url"]:
        print("NO IMAGE", g["id"], g["url"])
    time.sleep(1)                   # be polite, avoid getting blocked

    with open("gifs.json", "w", encoding="utf-8") as f:   # save as you go
        json.dump(gifs, f, indent=2)
