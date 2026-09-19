import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "kidhub.settings")

import django
django.setup()

from catalog.models import Toy
from pathlib import Path
from urllib.request import Request, urlopen
from urllib.parse import urlsplit, urlunsplit, quote
from io import BytesIO
from PIL import Image
import re, html

direct_images = {
    13: "https://avayebaran.ir/media/product_images/110912_2_nz4LGDw.jpg",
    39: "https://www.avayebaran.ir/media/product_images/01_jdh33SR.webp",
    37: "https://dkstatics-public.digikala.com/digikala-products/bc5b8d5c275520575701ed660f10f79354a3e434_1656500897.jpg?x-oss-process=image%2Fresize%2Cm_lfit%2Ch_800%2Cw_800%2Fquality%2Cq_90",
    29: "https://iepm.ir/image/cache/catalog/kafposh/pazel2-1000x1000.jpg",
    8: "https://iepm.ir/image/cache/catalog/kafposh/pazel2-1000x1000.jpg",
    2: "https://www.newclassictoys.de/_clientfiles/products/Woet/md/10430%20%281%29.jpg",
}

pages = {
    27: "https://centersara.ir/product/بازی-حافظه/",
    5: "https://raminashop.com/product/آویز-تخت-نوزاد-موزیکال-کوکی-چیکو-chicco/",
}

root = Path("media/toys")
root.mkdir(parents=True, exist_ok=True)

def encode_url(url):
    parts = urlsplit(url)
    return urlunsplit((
        parts.scheme,
        parts.netloc,
        quote(parts.path, safe="/%:@"),
        quote(parts.query, safe="=&%/:?"),
        parts.fragment
    ))

def download_image(url, toy_id):
    url = encode_url(url)
    req = Request(url, headers={"User-Agent": "Mozilla/5.0"})
    data = urlopen(req, timeout=30).read()

    out = root / f"toy-{toy_id}-real.jpg"
    img = Image.open(BytesIO(data)).convert("RGB")
    img.save(out, "JPEG", quality=92)

    Toy.objects.filter(id=toy_id).update(
        image=f"toys/{out.name}"
    )

    print(f"{toy_id} | OK | {out.name}")

for toy_id, image_url in direct_images.items():
    try:
        download_image(image_url, toy_id)
    except Exception as e:
        print(f"{toy_id} | ERROR | {e}")

for toy_id, page_url in pages.items():
    try:
        page_url = encode_url(page_url)
        req = Request(page_url, headers={"User-Agent": "Mozilla/5.0"})
        page = urlopen(req, timeout=30).read().decode("utf-8", "ignore")

        m = re.search(
            r'<meta[^>]+property=["\']og:image["\'][^>]+content=["\']([^"\']+)',
            page,
            re.I
        )

        if not m:
            m = re.search(
                r'<meta[^>]+content=["\']([^"\']+)["\'][^>]+property=["\']og:image',
                page,
                re.I
            )

        if not m:
            print(f"{toy_id} | IMAGE URL NOT FOUND")
            continue

        image_url = html.unescape(m.group(1))

        if image_url.startswith("//"):
            image_url = "https:" + image_url

        download_image(image_url, toy_id)

    except Exception as e:
        print(f"{toy_id} | ERROR | {e}")
