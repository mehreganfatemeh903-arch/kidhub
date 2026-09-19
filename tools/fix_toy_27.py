import os
from pathlib import Path
from urllib.request import Request, urlopen
from io import BytesIO

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "kidhub.settings")

import django
django.setup()

from PIL import Image
from catalog.models import Toy

url = "https://centersara.ir/wp-content/uploads/2026/02/%D8%A8%D8%A7%D8%B2%DB%8C-%D8%AD%D8%A7%D9%81%D8%B8%D9%872.jpg"

req = Request(url, headers={"User-Agent": "Mozilla/5.0"})
data = urlopen(req, timeout=60).read()

out = Path("media/toys/toy-27-real.jpg")
Image.open(BytesIO(data)).convert("RGB").save(out, "JPEG", quality=92)

Toy.objects.filter(id=27).update(image="toys/toy-27-real.jpg")

print("27 | OK |", out.name)
