# -*- coding: utf-8 -*-
from catalog.models import AgeGroup, Toy, Book

age0_6 = AgeGroup.objects.get(id=1)
age1_2 = AgeGroup.objects.get(id=2)
age3_5 = AgeGroup.objects.get(id=3)

# 1) اصلاح عنوان اشتباه رکوردهای فعلی
for toy in Toy.objects.all():
    desc = toy.short_description or ""
    if "پازل" in desc and "حیوانات" in desc and toy.title != "پازل چوبی حیوانات مزرعه":
        toy.title = "پازل چوبی حیوانات مزرعه"
        toy.save()
        print("اصلاح شد:", toy.id, toy.title)

# 2) اسباب‌بازی برای ۰ تا ۶ ماه
toy, created = Toy.objects.get_or_create(
    slug="aroosak-narm-mosighaei",
    defaults=dict(
        title="عروسک نرم موزیکال",
        short_description="عروسکی نرم با آهنگ ملایم برای آرام کردن و سرگرمی نوزاد.",
        why_it_helps="با پخش صدا و موسیقی ملایم، حس شنوایی و آرامش نوزاد را تقویت می‌کند.",
        price_range="۱۵۰ تا ۲۵۰ هزار تومان",
    ),
)
toy.age_groups.set([age0_6])
if created:
    print("اضافه شد:", toy.title)

toy, created = Toy.objects.get_or_create(
    slug="avizeh-takht-rangi",
    defaults=dict(
        title="آویز رنگی بالای تخت",
        short_description="آویزی با اشکال رنگی متحرک که بالای تخت نوزاد نصب می‌شود.",
        why_it_helps="دنبال کردن اشیای رنگی متحرک، تمرکز بینایی نوزاد را تقویت می‌کند.",
        price_range="۲۰۰ تا ۳۵۰ هزار تومان",
    ),
)
toy.age_groups.set([age0_6])
if created:
    print("اضافه شد:", toy.title)

# 3) اسباب‌بازی برای ۱ تا ۲ سال
toy, created = Toy.objects.get_or_create(
    slug="mashin-choobi-koochak",
    defaults=dict(
        title="ماشین چوبی کوچک",
        short_description="ماشین اسباب‌بازی چوبی با چرخ‌های قابل حرکت، مناسب کودکان نوپا.",
        why_it_helps="هل دادن و دنبال کردن ماشین، مهارت راه رفتن و هماهنگی حرکتی را تقویت می‌کند.",
        price_range="۱۰۰ تا ۲۰۰ هزار تومان",
    ),
)
toy.age_groups.set([age1_2])
if created:
    print("اضافه شد:", toy.title)

# 4) اسباب‌بازی برای ۳ تا ۵ سال
toy, created = Toy.objects.get_or_create(
    slug="khamir-bazi-rangin-kaman",
    defaults=dict(
        title="ست خمیربازی رنگین‌کمان",
        short_description="مجموعه خمیربازی در ۶ رنگ به همراه قالب‌های مختلف.",
        why_it_helps="له کردن و شکل دادن خمیر، عضلات ظریف دست و خلاقیت را تقویت می‌کند.",
        price_range="۱۲۰ تا ۲۲۰ هزار تومان",
    ),
)
toy.age_groups.set([age3_5])
if created:
    print("اضافه شد:", toy.title)

toy, created = Toy.objects.get_or_create(
    slug="pazl-alefba",
    defaults=dict(
        title="پازل درشت حروف الفبا",
        short_description="پازل چوبی با قطعات درشت حروف الفبای فارسی.",
        why_it_helps="آشنایی زودهنگام با حروف و تقویت مهارت حل مسئله.",
        price_range="۹۰ تا ۱۵۰ هزار تومان",
    ),
)
toy.age_groups.set([age3_5])
if created:
    print("اضافه شد:", toy.title)

# 5) کتاب برای هر بازه‌ی سنی
book, created = Book.objects.get_or_create(
    slug="ketab-sedaha-hayvanat",
    defaults=dict(
        title="کتاب صوتی صداهای حیوانات",
        book_type="audio",
        description="کتابی با دکمه‌های صوتی که صدای حیوانات مختلف را پخش می‌کند.",
        source_name="نشر پیدایش",
    ),
)
book.age_groups.set([age0_6])
if created:
    print("اضافه شد:", book.title)

book, created = Book.objects.get_or_create(
    slug="ketab-moghavaei-hayvanat",
    defaults=dict(
        title="کتاب مقوایی حیوانات مزرعه",
        book_type="text",
        description="کتاب مقوایی با تصاویر بزرگ و رنگی از حیوانات مزرعه، مناسب ورق زدن توسط کودک.",
        source_name="نشر افق",
    ),
)
book.age_groups.set([age1_2])
if created:
    print("اضافه شد:", book.title)

book, created = Book.objects.get_or_create(
    slug="anime-koochak-dooste-man",
    defaults=dict(
        title="انیمیشن کوتاه دوست من",
        book_type="video",
        description="انیمیشنی کوتاه درباره‌ی دوستی و همکاری، مناسب تماشای گروهی با کودک.",
        source_name="آپارات کودک",
    ),
)
book.age_groups.set([age3_5])
if created:
    print("اضافه شد:", book.title)

print("پایان: همه‌ی داده‌های نمونه با موفقیت وارد شدند.")
