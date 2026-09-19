import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "kidhub.settings")
django.setup()

from catalog.models import Book

data = {
    61: "کتابی کوتاه و تصویری برای خردسالان که با موضوع پرش قورباغه، کودک را با یکی از ویژگی‌های جالب این جانور آشنا می‌کند. کتاب با زبانی ساده و مناسب کودکان، یک دانستنی درباره قورباغه را به شکل سرگرم‌کننده مطرح می‌کند.",

    62: "کتابی کوتاه و تصویری برای خردسالان که به یکی از ویژگی‌های جالب ماهی‌ها، یعنی خوابیدن با چشم‌های باز، می‌پردازد. کتاب با زبانی ساده، یک دانستنی علمی درباره زندگی ماهی‌ها را برای کودکان قابل فهم و جذاب می‌کند.",

    63: "کتابی کوتاه و تصویری برای خردسالان که درباره خوابیدن پاندا روی درخت است. کتاب با زبانی ساده و کودکانه، یکی از رفتارهای جالب این حیوان را معرفی می‌کند و فرصتی برای آشنایی کودک با ویژگی‌های جانوران فراهم می‌آورد.",
}

for book_id, description in data.items():
    book = Book.objects.get(id=book_id)
    book.description = description
    book.save(update_fields=["description"])
    print(f"UPDATED {book_id} - {book.title}")

print(f"\nTOTAL UPDATED: {len(data)}")
