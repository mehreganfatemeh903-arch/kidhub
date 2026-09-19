import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "kidhub.settings")
django.setup()

from catalog.models import Book

book = Book.objects.get(id=55)
book.description = "کتابی از مجموعه دالی‌بازی که با پرسش و پاسخ و صفحه‌های تاشو، کودک را به کشف محیط خانه دعوت می‌کند. کودک در جریان بازی با وسایلی مانند یخچال، تلویزیون، میز و صندلی آشنا می‌شود و همراهی والد در بازی دالی، کنجکاوی و مشارکت او را بیشتر می‌کند."
book.save(update_fields=["description"])

print(f"UPDATED {book.id} - {book.title}")
