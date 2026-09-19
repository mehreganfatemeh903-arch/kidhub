import os
import urllib.request
from pathlib import Path

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "kidhub.settings")

import django
django.setup()

from django.conf import settings
from django.core.files.base import ContentFile
from catalog.models import Toy

MEDIA_TOYS = Path(settings.MEDIA_ROOT) / "toys"
MEDIA_TOYS.mkdir(parents=True, exist_ok=True)

items = {
    14: ("toy-14.jpg", "https://image.torob.com/base/images/ll/N5/llN528bBEEvgYdr2.jpg_/280x280.jpg"),
    20: ("toy-20.jpg", "https://iepm.ir/image/cache/catalog/AX%20SITE2/C107-1000x1000.jpg"),
    26: ("toy-26.jpg", "https://avayebaran.ir/media/product_images/IMG_8698.jpg"),
}

def download(url):
    req = urllib.request.Request(
        url,
        headers={"User-Agent": "Mozilla/5.0"}
    )
    with urllib.request.urlopen(req, timeout=30) as r:
        return r.read()

for toy_id, (filename, url) in items.items():
    toy = Toy.objects.get(id=toy_id)
    try:
        data = download(url)
        toy.image.save(filename, ContentFile(data), save=True)
        print(f"OK | {toy_id} | {toy.title} | {toy.image.name}")
    except Exception as e:
        print(f"ERROR | {toy_id} | {toy.title} | {e}")

print("DONE")
