import os
import requests
import urllib3

urllib3.disable_warnings()

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "kidhub.settings")

import django
django.setup()

from django.core.files.base import ContentFile
from catalog.models import Toy

items = {
    10: (
        "toy-10.jpg",
        "https://m.media-amazon.com/images/I/71FlKW4o0xL._AC_SL500_.jpg",
    ),
    14: (
        "toy-14.jpg",
        "https://image.torob.com/base/images/ll/N5/llN528bBEEvgYdr2.jpg_/280x280.jpg",
    ),
    15: (
        "toy-15.jpg",
        "https://image.made-in-china.com/202f0j00SqliNCWFMKuf/Building-a-Figure-Eight-Train-Track-Features-Wooden-Train-Set.jpg",
    ),
    18: (
        "toy-18.jpg",
        "https://files.emalls.ir/files/Products/automatic/6142964/gxqrr5us.jpg",
    ),
    19: (
        "toy-19.jpg",
        "https://bebetoy.ir/wp-content/uploads/2023/12/%D8%AA%D8%AE%D8%AA%D9%87-%D8%AC%D8%A7%D8%AF%D9%88%DB%8C%DB%8C-%D9%BE%D8%A7%DB%8C%D9%87-%D8%AF%D8%A7%D8%B1.jpg",
    ),
    23: (
        "toy-23.jpg",
        "https://avayebaran.ir/media/product_images/02_zeMmsF6.webp",
    ),
    25: (
        "toy-25.png",
        "https://www.technolife.com/image/gallery-3-137730_de58f6b8-8295-11f0-bea5-17f082fe705a.png",
    ),
    40: (
        "toy-40.jpg",
        "https://sayantoys.com/wp-content/uploads/2021/02/post-6-700x700.jpg",
    ),
}

for toy_id, (filename, url) in items.items():
    toy = Toy.objects.get(id=toy_id)

    try:
        response = requests.get(
            url,
            headers={"User-Agent": "Mozilla/5.0"},
            verify=False,
            timeout=40,
        )
        response.raise_for_status()

        toy.image.save(
            filename,
            ContentFile(response.content),
            save=True,
        )

        print(f"OK | {toy_id} | {toy.title} | {toy.image.name} | {len(response.content)} bytes")

    except Exception as e:
        print(f"ERROR | {toy_id} | {toy.title} | {e}")

print()
print("ALL DONE")
