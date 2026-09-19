from catalog.models import AgeGroup, Book, Article

ages = list(AgeGroup.objects.all().order_by("min_age_months", "id"))

if not ages:
    raise RuntimeError("AgeGroup وجود ندارد.")

# حذف محتوای قبلی و غیرواقعی
Book.objects.all().delete()
Article.objects.all().delete()

BOOKS = [
    ("قصه پیتر خرگوشه", "the-tale-of-peter-rabbit",
     "The Tale of Peter Rabbit", "Beatrix Potter",
     "کتابی کلاسیک درباره ماجراجویی پیتر خرگوشه در باغ آقای مکگرگور.",
     "https://www.gutenberg.org/files/14838/14838-h/14838-h.htm"),

    ("قصه بنیامین خرگوشه", "the-tale-of-benjamin-bunny",
     "The Tale of Benjamin Bunny", "Beatrix Potter",
     "داستان بنیامین خرگوشه و ماجراهای او در باغ و خانه.",
     "https://www.gutenberg.org/files/14407/14407-h/14407-h.htm"),

    ("قصه سنجاب ناتکین", "the-tale-of-squirrel-nutkin",
     "The Tale of Squirrel Nutkin", "Beatrix Potter",
     "داستان سنجاب بازیگوشی که برای جمعآوری آجیل با ماجراهای مختلف روبهرو میشود.",
     "https://www.gutenberg.org/files/14872/14872-h/14872-h.htm"),

    ("قصه تام بچهگربه", "the-tale-of-tom-kitten",
     "The Tale of Tom Kitten", "Beatrix Potter",
     "داستان تام و خواهر و برادرهایش و اتفاقاتی که هنگام آماده شدن برای مهمانی رخ میدهد.",
     "https://www.gutenberg.org/files/14837/14837-h/14837-h.htm"),

    ("قصه جمیما اردک", "the-tale-of-jemima-puddle-duck",
     "The Tale of Jemima Puddle-Duck", "Beatrix Potter",
     "داستان جمیما اردکی که برای پیدا کردن محل مناسب تخمگذاری وارد ماجرا میشود.",
     "https://www.gutenberg.org/files/14814/14814-h/14814-h.htm"),

    ("قصه خرگوشهای فلوپسی", "the-tale-of-the-flopsy-bunnies",
     "The Tale of the Flopsy Bunnies", "Beatrix Potter",
     "داستان خانواده خرگوشها و ماجرایی که برای پیدا کردن غذا و بازگشت به خانه رخ میدهد.",
     "https://www.gutenberg.org/files/14220/14220-h/14220-h.htm"),
]

for title, slug, original_title, author, description, url in BOOKS:
    book = Book.objects.create(
        title=title,
        slug=slug,
        description=description,
        book_type="text",
        author=author,
        source_name="Project Gutenberg",
        source_url=url,
    )
    book.age_groups.set(ages[-3:] if len(ages) >= 3 else ages)


ARTICLES = [
    (
        "نقاط عطف رشد کودک",
        "cdc-developmental-milestones",
        "منبع رسمی CDC برای آشنایی با نقاط عطف رشد کودکان در سنین مختلف.",
        "این منبع رسمی مراکز کنترل و پیشگیری بیماریهای آمریکا نقاط عطف رشدی کودک را در زمینههایی مانند ارتباط یادگیری حرکت و مهارتهای اجتماعی توضیح میدهد. والدین میتوانند از این اطلاعات برای مشاهده رشد کودک و گفتوگو با متخصص استفاده کنند.",
        "CDC",
        "https://www.cdc.gov/act-early/milestones/index.html",
    ),
    (
        "چکلیست نقاط عطف رشد بر اساس سن",
        "cdc-milestone-checklists-by-age",
        "چکلیست رسمی CDC برای بررسی نقاط عطف رشد کودک بر اساس سن.",
        "CDC چکلیستهای نقاط عطف رشد را برای سنین مختلف ارائه میکند. این چکلیستها برای مشاهده و ثبت مهارتهایی که کودک در مسیر رشد به دست میآورد طراحی شدهاند و جایگزین ارزیابی پزشکی نیستند.",
        "CDC",
        "https://www.cdc.gov/act-early/resources/milestones-checklist-by-age.html",
    ),
    (
        "نقاط عطف رشد در ۲ ماهگی",
        "cdc-milestones-2-months",
        "نمونههایی از مهارتهای رشدی مورد انتظار در حدود دو ماهگی.",
        "صفحه رسمی CDC برخی مهارتهای ارتباطی اجتماعی شناختی و حرکتی را که بسیاری از نوزادان در حدود دو ماهگی نشان میدهند توضیح میدهد.",
        "CDC",
        "https://www.cdc.gov/act-early/milestones/2-months.html",
    ),
    (
        "نقاط عطف رشد در ۲ سالگی",
        "cdc-milestones-2-years",
        "نمونههایی از مهارتهای رشدی مورد انتظار در حدود دو سالگی.",
        "صفحه رسمی CDC درباره مهارتهای زبانی اجتماعی شناختی و حرکتی کودکان حدود دو سال توضیح میدهد و به والدین کمک میکند رشد کودک را بهتر مشاهده کنند.",
        "CDC",
        "https://www.cdc.gov/act-early/milestones/2-years.html",
    ),
    (
        "چطور با نوزاد کتاب بخوانیم",
        "healthychildren-sharing-books-with-baby",
        "راهنمای آکادمی اطفال آمریکا برای کتابخوانی با نوزاد.",
        "آکادمی اطفال آمریکا توضیح میدهد که کتابخوانی مشترک با نوزاد میتواند فرصتی برای ارتباط گفتوگو و تعامل والد و کودک ایجاد کند. لازم نیست نوزاد تمام داستان را بفهمد نگاه کردن به تصاویر صحبت کردن و پاسخ دادن به واکنشهای کودک نیز بخشی از تجربه کتابخوانی است.",
        "American Academy of Pediatrics / HealthyChildren.org",
        "https://www.healthychildren.org/English/ages-stages/baby/Pages/how-to-share-books-with-your-baby.aspx",
    ),
    (
        "کتابخوانی با کودک ۱۲ تا ۱۴ ماهه",
        "healthychildren-books-12-14-months",
        "راهنمای HealthyChildren برای کتابخوانی با کودک نوپا.",
        "این راهنمای آکادمی اطفال آمریکا پیشنهادهایی برای تعامل با کودک هنگام کتابخوانی در حدود ۱۲ تا ۱۴ ماهگی ارائه میکند و بر گفتوگو اشاره به تصاویر و مشارکت فعال کودک تأکید دارد.",
        "American Academy of Pediatrics / HealthyChildren.org",
        "https://www.healthychildren.org/English/ages-stages/toddler/Pages/How-to-Share-Books-with-Your-12-to-14-Month-Old.aspx",
    ),
    (
        "کتابخوانی با کودک ۱۵ تا ۱۷ ماهه",
        "healthychildren-books-15-17-months",
        "راهنمای HealthyChildren برای کتابخوانی با کودک ۱۵ تا ۱۷ ماهه.",
        "راهنمای آکادمی اطفال آمریکا روشهایی برای مشارکت دادن کودک نوپا در کتابخوانی صحبت درباره تصاویر و ایجاد تعامل هنگام خواندن کتاب پیشنهاد میکند.",
        "American Academy of Pediatrics / HealthyChildren.org",
        "https://www.healthychildren.org/English/ages-stages/toddler/Pages/How-to-Share-Books-with-Your-15-to-17-Month-Old.aspx",
    ),
    (
        "کتابخوانی برای کودکان با نیازهای رشدی یا سلامت ویه",
        "healthychildren-sharing-books-special-needs",
        "پیشنهادهای HealthyChildren برای کتابخوانی با کودکان دارای نیازهای رشدی یا سلامت ویه.",
        "این منبع آکادمی اطفال آمریکا نکاتی برای سازگار کردن تجربه کتابخوانی با نیازها و تواناییهای متفاوت کودکان ارائه میکند.",
        "American Academy of Pediatrics / HealthyChildren.org",
        "https://www.healthychildren.org/English/health-issues/conditions/developmental-disabilities/Pages/sharing-books-tips-for-parents-of-children-with-special-health-and-development-needs.aspx",
    ),
]

for title, slug, summary, body, source_name, source_url in ARTICLES:
    article = Article.objects.create(
        title=title,
        slug=slug,
        summary=summary,
        body=body,
        source_name=source_name,
        source_url=source_url,
    )
    article.age_groups.set(ages)

print("REAL BOOKS:", Book.objects.count())
print("REAL ARTICLES:", Article.objects.count())
