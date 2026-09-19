import urllib.request
from django.core.files.base import ContentFile
from catalog.models import Toy, Book

def attach_image(instance, field_name, seed):
    url = f"https://picsum.photos/seed/{seed}/600/400"
    try:
        with urllib.request.urlopen(url, timeout=15) as response:
            data = response.read()
        getattr(instance, field_name).save(f"{seed}.jpg", ContentFile(data), save=True)
        print("عکس اضافه شد:", instance.title)
    except Exception as e:
        print("خطا برای:", instance.title, str(e))

for toy in Toy.objects.all():
    if not toy.image:
        attach_image(toy, "image", toy.slug)

for book in Book.objects.all():
    if not book.cover_image:
        attach_image(book, "cover_image", book.slug)

print("پایان.")