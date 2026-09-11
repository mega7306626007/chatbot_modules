#!/usr/bin/env python3
"""Download ~100 CC photos into cached_online_images/ grouped by theme label."""
import os, json, time, pathlib, urllib.request, urllib.parse
from PIL import Image

# Use same themes as OfflineSceneGenerator
THEMES = ["sunset","sunrise","ocean","forest","space","city","mountain","desert","aurora","rainy","garden","winter","waterfall","autumn","savanna","canyon","volcano","tundra","meadow","river"]
QUERIES = {
    "sunset": "sunset beach",
    "sunrise": "sunrise mountain",
    "ocean": "tropical ocean beach",
    "forest": "misty forest",
    "space": "galaxy stars",
    "city": "city skyline night",
    "mountain": "snowy mountain",
    "desert": "desert dunes",
    "aurora": "aurora borealis",
    "rainy": "rainy street",
    "garden": "flower garden",
    "winter": "snow winter cabin",
    "waterfall": "waterfall jungle",
    "autumn": "autumn forest",
    "savanna": "african savanna",
    "canyon": "grand canyon",
    "volcano": "volcano eruption",
    "tundra": "arctic tundra",
    "meadow": "wildflower meadow",
    "river": "river valley",
}
CACHE_ROOT = pathlib.Path(__file__).parent / "cached_online_images"
IMAGES_PER_THEME = 5  # 20*5=100

def fetch_openverse(query, page_size=5):
    params = urllib.parse.urlencode({"q": query, "page_size": page_size, "category": "photograph", "license_type": "commercial,modification"})
    url = f"https://api.openverse.org/v1/images/?{params}"
    req = urllib.request.Request(url, headers={"User-Agent": "offline-chatbot/1.0"})
    with urllib.request.urlopen(req, timeout=12) as r:
        return json.loads(r.read().decode("utf-8"))

def download_image(url, dest):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "Accept": "image/avif,image/webp,image/*,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
    }
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=12) as r:
            data = r.read()
    except urllib.error.HTTPError as e:
        if e.code == 403:
            # retry with offline-chatbot UA as fallback
            req2 = urllib.request.Request(url, headers={"User-Agent": "offline-chatbot/1.0"})
            with urllib.request.urlopen(req2, timeout=12) as r:
                data = r.read()
        else:
            raise
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_bytes(data)
    # validate and re-save capped at 1024
    try:
        im = Image.open(dest).convert("RGB")
        w,h = im.size
        if max(w,h) > 1024:
            scale = 1024 / max(w,h)
            im = im.resize((int(w*scale), int(h*scale)), Image.LANCZOS)
        im.save(dest, quality=92, optimize=True)
        return True
    except Exception as e:
        print(f"Invalid image {url}: {e}")
        try: dest.unlink()
        except: pass
        return False

def main():
    CACHE_ROOT.mkdir(exist_ok=True)
    for theme in THEMES:
        q = QUERIES[theme]
        print(f"[{theme}] query '{q}' ...")
        try:
            data = fetch_openverse(q, page_size=IMAGES_PER_THEME)
        except Exception as e:
            print(f"  fetch failed: {e}")
            continue
        results = data.get("results") or []
        print(f"  got {len(results)} results")
        theme_dir = CACHE_ROOT / theme
        theme_dir.mkdir(exist_ok=True)
        saved = 0
        for idx, item in enumerate(results[:IMAGES_PER_THEME]):
            url = item.get("url")
            if not url: continue
            title = item.get("title","")
            creator = item.get("creator","unknown")
            lic = (item.get("license") or "").upper()
            dest = theme_dir / f"{theme}_{idx:02d}.jpg"
            meta = theme_dir / f"{theme}_{idx:02d}.json"
            if dest.exists(): 
                saved +=1
                continue
            ok = download_image(url, dest)
            if ok:
                meta.write_text(json.dumps({"title": title, "creator": creator, "license": lic, "query": q, "url": url}, ensure_ascii=False, indent=2), encoding="utf-8")
                saved+=1
                print(f"  saved {dest.name} ({lic})")
            time.sleep(0.4)
        print(f"  -> {saved} cached for {theme}")
        time.sleep(0.6)
    # summary
    total = sum(1 for p in CACHE_ROOT.rglob("*.jpg"))
    print(f"TOTAL cached images: {total}")
    for theme in THEMES:
        print(f" {theme}: {len(list((CACHE_ROOT/theme).glob('*.jpg')))}")

if __name__ == "__main__":
    main()
