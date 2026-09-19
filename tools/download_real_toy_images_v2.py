import os
import re
import html
import mimetypes
import requests
from urllib.parse import urljoin
from catalog.models import Toy

BASE = "https://"
MEDIA_DIR = os.path.join("media", "toys")
os.makedirs(MEDIA_DIR, exist_ok=True)

PAGES = {
    13: "https://www.avayebaran.ir/product/",
    17: "https://www.avayebaran.ir/product/%D8%A8%D9%88%D9%84%DB%8C%D9%86%DA%AF-%D9%88-%D8%AD%D9%84%D9%82%D9%87-%D9%BE%D8%B1%D8%AA%D8%A7%D8%A8-%DA%A9%DB%8C%D9%81%DB%8C-%D8%A8%D8%B2%D8%B1%DA%AF-%D9%84%D8%A8%D8%AE%D9%86%D8%AF/",
    20: "https://iepm.ir/%D8%B3%D8%AA-%D8%A7%D8%B3%D8%A8%D8%A7%D8%A8-%D8%A8%D8%A7%D8%B2%DB%8C-%D8%A2%D8%B4%D9%BE%D8%B2%D8%AE%D8%A7%D9%86%D9%87-wd-p37",
    24: "https://bazitahrir.com/%D9%BE%D8%A7%D8%B2%D9%84-%D8%A8%D8%B2%D8%B1%DA%AF-%D8%AC%D9%86%DA%AF%D9%84-%D8%AD%DB%8C%D9%88%D8%A7%D9%86%D8%A7%D8%AA",
    29: "https://iepm.ir/index.php?limit=25&order=ASC&path=20&route=product%2Fcategory&sort=p.price",
    32: "https://iepm.ir/index.php?path=20&route=product%2Fcategory",
    34: "https://iepm.ir/%D8%AA%D9%88%D9%86%D9%84-%D9%87%D8%B2%D8%A7%D8%B1-%D9%BE%D8%A7-%D8%AF%D9%88-%D8%AA%DB%8C%DA%A9%D9%87",
    35: "https://iepm.ir/%D8%B7%D9%86%D8%A7%D8%A8-%D9%88%D8%B1%D8%B2%D8%B4%DB%8C-%D9%85%D8%AF%D9%84-JAK7",
    36: "https://sadattoys.com/product/%D9%BE%DB%8C%D9%86%DA%AF%D9%88-%D8%A8%D8%A7%D9%84%D8%A7%D9%86%D8%B3/",
    37: "https://tameshk.ariatheme.ir/product/%D8%A8%D8%A7%D8%B2%DB%8C-%D9%81%DA%A9%D8%B1%DB%8C-%D9%87%D9%88%DA%AF%D8%B1-%D9%85%D8%AF%D9%84-%D8%A8%D8%B2%D8%B1%DA%AF%D8%B1%D8%A7%D9%87-4-%D9%86%D9%81%D8%B1%D9%87/",
    38: "https://www.vinatahrir.com/product/arya-5-colors-bucket-play-dough-with-tools/",
    39: "https://www.avayebaran.ir/product/",
    40: "https://sayantoys.com/product/%D9%BE%D8%A7%D8%B2%D9%84-%D8%A2%D9%85%D9%88%D8%B2%D8%B4%DB%8C-%D8%A8%D8%AF%D9%86/",
    41: "https://fluteshop.org/product/nino-percussion-ninoset012-wb/",
}

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/140 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
    "Accept-Language": "fa-IR,fa;q=0.9,en;q=0.8",
}

session = requests.Session()
session.headers.update(HEADERS)
session.trust_env = False

def image_candidates(page_url, text):
    result = []

    # og:image
    for m in re.findall(
        r'<meta[^>]+property=["\']og:image["\'][^>]+content=["\']([^"\']+)["\']',
        text, re.I
    ):
        result.append(urljoin(page_url, html.unescape(m)))

    # twitter image
    for m in re.findall(
        r'<meta[^>]+name=["\']twitter:image["\'][^>]+content=["\']([^"\']+)["\']',
        text, re.I
    ):
        result.append(urljoin(page_url, html.unescape(m)))

    # src / data-src / data-lazy-src
    for m in re.findall(
        r'(?:src|data-src|data-lazy-src)=["\']([^"\']+)["\']',
        text, re.I
    ):
        u = html.unescape(m)
        if re.search(r'\.(?:jpg|jpeg|png|webp)(?:\?|$)', u, re.I):
            result.append(urljoin(page_url, u))

    # srcset
    for block in re.findall(r'(?:srcset|data-srcset)=["\']([^"\']+)["\']', text, re.I):
        for item in block.split(","):
            u = item.strip().split(" ")[0]
            if re.search(r'\.(?:jpg|jpeg|png|webp)(?:\?|$)', u, re.I):
                result.append(urljoin(page_url, html.unescape(u)))

    # remove duplicates and obvious site assets
    clean = []
    seen = set()

    for u in result:
        u = u.replace("\\/", "/")
        low = u.lower()

        if any(x in low for x in [
            "logo", "icon", "favicon", "flag", "language",
            "gift_box", "placeholder", "loading"
        ]):
            continue

        if u not in seen:
            seen.add(u)
            clean.append(u)

    return clean

def download_image(toy_id, page_url):
    r = session.get(page_url, timeout=30, verify=False)
    r.raise_for_status()

    candidates = image_candidates(page_url, r.text)

    if not candidates:
        raise RuntimeError("image candidates not found")

    for idx, img_url in enumerate(candidates[:20]):
        try:
            x = session.get(
                img_url,
                timeout=30,
                verify=False,
                headers={"Referer": page_url}
            )

            if x.status_code != 200:
                continue

            data = x.content
            ctype = x.headers.get("Content-Type", "").lower()

            # واقعی بودن فایل تصویر
            is_image = (
                ctype.startswith("image/")
                or data.startswith(b"\xff\xd8\xff")
                or data.startswith(b"\x89PNG")
                or data.startswith(b"RIFF")
            )

            if not is_image or len(data) < 5000:
                continue

            ext = ".jpg"
            if "png" in ctype or data.startswith(b"\x89PNG"):
                ext = ".png"
            elif "webp" in ctype or data.startswith(b"RIFF"):
                ext = ".webp"

            path = os.path.join(MEDIA_DIR, f"toy-{toy_id}{ext}")

            with open(path, "wb") as f:
                f.write(data)

            return path

        except Exception:
            continue

    raise RuntimeError("no valid product image found")

for toy_id, page_url in PAGES.items():
    try:
        toy = Toy.objects.get(id=toy_id)
        path = download_image(toy_id, page_url)

        rel = os.path.relpath(path, "media").replace("\\", "/")
        toy.image = rel
        toy.save(update_fields=["image"])

        print(f"OK {toy_id}: {rel}")

    except Exception as e:
        print(f"FAIL {toy_id}: {e}")
