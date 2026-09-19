import os
import re
import html
import requests
from urllib.parse import urljoin
from catalog.models import Toy

BASE = "http://localhost"
OUT = os.path.join("media", "toys")
os.makedirs(OUT, exist_ok=True)

pages = {
    11: "https://basalam.com/mana_kids/product/4651930",
    12: "https://centersara.ir/product/henectus-tincidunt/",
    13: "https://avayebaran.ir/product/%D8%AD%D9%84%D9%82%D9%87-%D9%87%D9%88%D8%B4-%D8%AE%D8%B1%D8%B3%DB%8C-%D8%A8%D8%B2%D8%B1%DA%AF/",
    16: "https://brix1.com/product/brix-7001/",
    17: "https://www.avayebaran.ir/product/%D8%A8%D9%88%D9%84%DB%8C%D9%86%DA%AF-%D9%88-%D8%AD%D9%84%D9%82%D9%87-%D9%BE%D8%B1%D8%AA%D8%A7%D8%A8-%DA%A9%DB%8C%D9%81%DB%8C-%D8%A8%D8%B2%D8%B1%DA%AF-%D9%84%D8%A8%D8%AE%D9%86%D8%AF/",
    20: "https://iepm.ir/%D9%84%D9%88%D8%A7%D8%B2%D9%85-%D8%AA%D9%81%D8%B1%DB%8C%D8%AD%DB%8C-%D9%88%D8%B1%D8%B2%D8%B4%DB%8C/%D8%B3%D8%AA-%D8%A7%D8%B3%D8%A8%D8%A7%D8%A8-%D8%A8%D8%A7%D8%B2%DB%8C-%D8%A2%D8%B4%D9%BE%D8%B2%D8%AE%D8%A7%D9%86%D9%87-%D9%85%D8%AF%D9%84-wd-p37?limit=75",
    21: "https://bebetoy.ir/shop/%D9%86%D9%82%D8%B4-%D8%A2%D9%81%D8%B1%DB%8C%D9%86%DB%8C/%D8%B9%D8%B1%D9%88%D8%B3%DA%A9/%D8%B9%D8%B1%D9%88%D8%B3%DA%A9-%D9%86%D9%88%D8%B2%D8%A7%D8%AF-%DB%B3%DB%B5-%D8%B3%D8%A7%D9%86%D8%AA%DB%8C-%D8%A8%D8%A7-%DA%86%D8%B4%D9%85-%D9%87%D8%A7%DB%8C-%D8%A8%D9%86%D9%81%D8%B4/",
    22: "https://centersara.ir/product/%D8%AF%D9%88%D9%85%DB%8C%D9%86%D9%88-200-%D9%82%D8%B7%D8%B9%D9%87-%D9%84%D8%A8%D8%AE%D9%86%D8%AF/",
    24: "https://avayebaran.ir/product/%D9%BE%D8%A7%D8%B2%D9%84-%D8%A8%D8%B2%D8%B1%DA%AF-%D8%AC%D9%86%DA%AF%D9%84-%D8%AD%DB%8C%D9%88%D8%A7%D9%86%D8%A7%D8%AA/",
    28: "https://robochip.ir/Product/RBC-18556/%D8%A8%D8%B3%D8%AA%D9%87-%D8%B3%D8%A7%D8%AE%D8%AA%D9%86%DB%8C-%D8%B3%D8%A7%D8%B2%D9%87-%D9%87%D8%A7%DB%8C-easymech-20-%D9%85%D8%AF%D9%84-111-%D9%82%D8%B7%D8%B9%D9%87/",
    29: "https://iepm.ir/%DA%A9%D9%81%D9%BE%D9%88%D8%B4-%D8%AF%DB%8C%D9%88%D8%A7%D8%B1%D9%BE%D9%88%D8%B4-%D8%AA%D8%A7%D8%AA%D8%A7%D9%85%DB%8C-%DA%AF%D8%B1%D8%A7%D9%86%D9%88%D9%84-%D9%81%D9%88%D9%85%DB%8C/%D9%BE%D8%A7%D8%B2%D9%84-",
    30: "https://centersara.ir/product/chartake-koochak-ofoghi/",
    31: "https://iepm.ir/%D8%B3%D8%AA-%D9%BE%D8%B2%D8%B4%DA%A9%DB%8C-%DA%86%D8%B1%D8%AE%D8%AF%D8%A7%D8%B1",
    34: "https://iepm.ir/%D8%AA%D9%88%D9%86%D9%84-%D9%87%D8%B2%D8%A7%D8%B1-%D9%BE%D8%A7-%D8%AF%D9%88-%D8%AA%DB%8C%DA%A9%D9%87",
    35: "https://iepm.ir/%D8%B7%D9%86%D8%A7%D8%A8-%D9%88%D8%B1%D8%B2%D8%B4%DB%8C-%D9%85%D8%AF%D9%84-JAK7",
    36: "https://sadattoys.com/product/%D9%BE%DB%8C%D9%86%DA%AF%D9%88-%D8%A8%D8%A7%D9%84%D8%A7%D9%86%D8%B3/",
    37: "https://tameshk.ariatheme.ir/product/%D8%A8%D8%A7%D8%B2%DB%8C-%D9%81%DA%A9%D8%B1%DB%8C-%D9%87%D9%88%DA%AF%D8%B1-%D9%85%D8%AF%D9%84-%D8%A8%D8%B2%D8%B1%DA%AF%D8%B1%D8%A7%D9%87-4-%D9%86%D9%81%D8%B1%D9%87/",
    38: "https://www.vinatahrir.com/product/arya-5-colors-bucket-play-dough-with-tools/",
    39: "https://www.avayebaran.ir/product/%DA%A9%D8%A7%D8%B1%D8%AA-%D9%BE%D8%A7%D8%B2%D9%84-%D8%A2%D9%85%D9%88%D8%B2%D8%B4%DB%8C-%D8%B7%D8%A8%D9%82%D9%87-%D8%A8%D9%86%D8%AF%DB%8C/",
    40: "https://sayantoys.com/product/%D9%BE%D8%A7%D8%B2%D9%84-%D8%A2%D9%85%D9%88%D8%B2%D8%B4%DB%8C-%D8%A8%D8%AF%D9%86/",
    41: "https://fluteshop.org/product/nino-percussion-ninoset012-wb/",
}

headers = {"User-Agent": "Mozilla/5.0"}

for toy_id, page_url in pages.items():
    try:
        r = requests.get(page_url, headers=headers, timeout=20)
        r.raise_for_status()
        text = r.text

        candidates = []

        for pattern in [
            r'<meta[^>]+property=["\']og:image["\'][^>]+content=["\']([^"\']+)',
            r'<meta[^>]+content=["\']([^"\']+)["\'][^>]+property=["\']og:image["\']',
            r'<img[^>]+src=["\']([^"\']+)["\']'
        ]:
            candidates += re.findall(pattern, text, re.I)

        candidates = [html.unescape(urljoin(page_url, x)) for x in candidates]

        image_url = None
        for u in candidates:
            if re.search(r'\.(jpg|jpeg|png|webp)(\?|$)', u, re.I):
                image_url = u
                break

        if not image_url:
            print(f"FAIL {toy_id}: image not found")
            continue

        img = requests.get(image_url, headers=headers, timeout=20)
        img.raise_for_status()

        ext = ".jpg"
        ct = img.headers.get("content-type", "")
        if "png" in ct:
            ext = ".png"
        elif "webp" in ct:
            ext = ".webp"

        filename = f"toy-{toy_id}{ext}"
        path = os.path.join(OUT, filename)

        with open(path, "wb") as f:
            f.write(img.content)

        toy = Toy.objects.get(id=toy_id)
        toy.image = f"toys/{filename}"
        toy.save(update_fields=["image"])

        print(f"OK {toy_id}: {filename}")

    except Exception as e:
        print(f"FAIL {toy_id}: {e}")

