import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "kidhub.settings")
django.setup()

from catalog.models import Book

data = {
    72: "داستان دو موجود پشمالو را روایت می‌کند که درباره اینکه کدام‌یک کوچک و کدام‌یک بزرگ است با هم بحث می‌کنند. با پیدا شدن موجودات پشمالوی دیگری در اندازه‌های متفاوت، آن‌ها متوجه می‌شوند که بزرگ یا کوچک بودن به این بستگی دارد که خودت را با چه کسی مقایسه کنی. کتاب با زبانی ساده و تصاویر جذاب، مفهوم مقایسه، اندازه و نگاه به خود را برای کودکان مطرح می‌کند.",

    82: "کتابی آموزشی برای کودکان که با هدف آشنایی آن‌ها با مهارت‌های زندگی و رفتارهای سازگارانه طراحی شده است. کتاب به کودکان کمک می‌کند توانایی‌هایی را که برای ارتباط سالم، رفتار مناسب و سازگاری بهتر با محیط و دیگران نیاز دارند بشناسند و تمرین کنند. این اثر نوشته مژگان کلهر و با تصویرگری فرهاد جمشیدی منتشر شده است."
}

for book_id, description in data.items():
    book = Book.objects.get(id=book_id)
    book.description = description
    book.save(update_fields=["description"])
    print(f"UPDATED {book_id} - {book.title}")

print(f"\nTOTAL UPDATED: {len(data)}")
