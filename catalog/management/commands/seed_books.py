from django.core.management.base import BaseCommand
from catalog.models import Book, AgeGroup


AAP_URL = "https://www.healthychildren.org/English/ages-stages/baby/Pages/how-to-share-books-with-your-baby.aspx"
ROSHD_URL = "https://samanketab.roshdmag.ir/"
MICHKA_URL = "https://michkapub.com/"


BOOKS = [
    # =========================================================
    # 0 تا 6 ماه — AgeGroup 4
    # =========================================================
    {
        "title": "نی‌نی چقدر ملوسه",
        "slug": "nini-cheghadr-molouse",
        "age": 4,
        "topic": "شناخت چهره و ارتباط عاطفی",
        "benefit": "کتابی تصویری و تعاملی برای گفت‌وگوی والد و نوزاد و توجه به چهره‌ها و صداها.",
    },
    {
        "title": "مامان اونو می‌بوسه",
        "slug": "maman-ono-mibose",
        "age": 4,
        "topic": "دلبستگی و امنیت عاطفی",
        "benefit": "مناسب برای همراهی با تماس چشمی، صدای والد و تعامل عاطفی با نوزاد.",
    },
    {
        "title": "این سر و دست و پاشه",
        "slug": "in-sar-o-dast-o-pashe",
        "age": 4,
        "topic": "شناخت بدن",
        "benefit": "کمک به نام‌گذاری اعضای بدن و ایجاد تعامل کلامی ساده بین والد و کودک.",
    },
    {
        "title": "ناف نی‌نی کجاشه؟",
        "slug": "nafe-nini-kojash",
        "age": 4,
        "topic": "شناخت بدن و کنجکاوی",
        "benefit": "برای گفت‌وگوی ساده درباره بدن و تقویت توجه مشترک والد و کودک.",
    },
    {
        "title": "نی‌نی قام‌قام",
        "slug": "nini-gham-gham",
        "age": 4,
        "topic": "صداها و زبان اولیه",
        "benefit": "مناسب برای تقلید صدا، تکرار و بازی‌های کلامی ساده.",
    },
    {
        "title": "مامان جون نی‌نی بیا",
        "slug": "maman-joon-nini-bia",
        "age": 4,
        "topic": "تعامل والد و کودک",
        "benefit": "برای ایجاد روتین خواندن و تقویت ارتباط عاطفی و توجه مشترک.",
    },
    {
        "title": "بچه‌ی من چه شکلیه؟",
        "slug": "bache-man-che-shekliye",
        "age": 4,
        "topic": "شناخت خود و خانواده",
        "benefit": "کمک به گفت‌وگو درباره ویژگی‌های ظاهری و ارتباط با اعضای خانواده.",
    },
    {
        "title": "دالی چی؟ دالی کی؟",
        "slug": "dali-chi-dali-key",
        "age": 4,
        "topic": "پایداری شیء و تعامل",
        "benefit": "بازی دالی به تقویت توجه، انتظار و مشارکت کودک در تعامل کمک می‌کند.",
    },
    {
        "title": "دالی! یه باغ‌وحش ناز!",
        "slug": "dali-ye-bagh-vohsh-naz",
        "age": 4,
        "topic": "شناخت حیوانات و زبان",
        "benefit": "مناسب برای نام‌گذاری حیوانات، تقلید صدا و تعامل تصویری.",
    },
    {
        "title": "تق‌تق، بیا بیرون",
        "slug": "tagh-tagh-bia-biroon",
        "age": 4,
        "topic": "کنجکاوی و کشف",
        "benefit": "کتابی تعاملی برای ایجاد انتظار، پرسش و مشارکت کودک در روند داستان.",
    },

    # =========================================================
    # 6 تا 12 ماه — AgeGroup 5
    # =========================================================
    {
        "title": "نی‌نی عاشق بهاره",
        "slug": "nini-ashegh-bahare",
        "age": 5,
        "topic": "شناخت طبیعت و فصل‌ها",
        "benefit": "کمک به مشاهده تصاویر، نام‌گذاری عناصر محیط و ایجاد گفت‌وگوی مشترک.",
    },
    {
        "title": "نی‌نی عاشق تابستونه",
        "slug": "nini-ashegh-tabestoone",
        "age": 5,
        "topic": "شناخت محیط",
        "benefit": "تقویت توجه به تصاویر و واژگان مربوط به محیط و فصل تابستان.",
    },
    {
        "title": "نی‌نی عاشق پاییزه",
        "slug": "nini-ashegh-paeeze",
        "age": 5,
        "topic": "طبیعت و مشاهده",
        "benefit": "مناسب برای گفت‌وگوی والد و کودک درباره تغییرات محیط و رنگ‌ها.",
    },
    {
        "title": "نی‌نی عاشق زمستونه",
        "slug": "nini-ashegh-zemestoone",
        "age": 5,
        "topic": "طبیعت و واژگان",
        "benefit": "تقویت مشاهده، اشاره و نام‌گذاری تصاویر مربوط به فصل زمستان.",
    },
    {
        "title": "نی‌نی قام‌قام و حیوانات",
        "slug": "nini-gham-gham-animals",
        "age": 5,
        "topic": "زبان و شناخت حیوانات",
        "benefit": "برای تقلید صدا، اشاره به تصاویر و افزایش واژگان اولیه.",
    },
    {
        "title": "کیک نی‌نی کجایی؟",
        "slug": "cake-nini-kojayi",
        "age": 5,
        "topic": "جست‌وجو و حل مسئله ساده",
        "benefit": "ساختار پرسش و پاسخ و جست‌وجوی تصویری، توجه و کنجکاوی کودک را فعال می‌کند.",
    },
    {
        "title": "بزرگ بشم چی می‌شم؟",
        "slug": "bozorg-besham-chi-misham",
        "age": 5,
        "topic": "شناخت نقش‌ها و مشاغل",
        "benefit": "کمک به نام‌گذاری نقش‌ها و آشنایی اولیه با دنیای پیرامون.",
    },
    {
        "title": "مامان و نی‌نی",
        "slug": "maman-o-nini",
        "age": 5,
        "topic": "رابطه والد و کودک",
        "benefit": "برای تقویت تعامل، توجه مشترک و روتین خواندن با والد.",
    },
    {
        "title": "دالی یه باغ وحش ناز!",
        "slug": "dali-bagh-vohsh-naz",
        "age": 5,
        "topic": "حیوانات و زبان",
        "benefit": "مناسب برای اشاره، نام‌گذاری و تقلید صداهای حیوانات.",
    },
    {
        "title": "دالی‌بازی: نی‌نی و حیوانات",
        "slug": "dali-bazi-nini-o-heyvanat",
        "age": 5,
        "topic": "تعامل تصویری",
        "benefit": "فعالیت‌های دالی و تصاویر ساده برای توجه، مشارکت و زبان اولیه.",
    },

    # =========================================================
    # 1 تا 2 سال — AgeGroup 6
    # =========================================================
    {
        "title": "نی‌نی می‌خواد بره کجا؟ تختخواب",
        "slug": "nini-mikhad-bere-koja-takhtkhab",
        "age": 6,
        "topic": "روتین خواب",
        "benefit": "برای ایجاد روتین آرام قبل از خواب و گفت‌وگو درباره مراحل خواب.",
    },
    {
        "title": "نی‌نی عاشق حیواناته",
        "slug": "nini-ashegh-heyvanate",
        "age": 6,
        "topic": "شناخت حیوانات",
        "benefit": "افزایش واژگان و تشخیص تصاویر حیوانات از طریق تکرار و تعامل.",
    },
    {
        "title": "جورچین حیوانات",
        "slug": "jorchin-heyvanat-book",
        "age": 6,
        "topic": "حل مسئله و هماهنگی چشم و دست",
        "benefit": "برای تطبیق شکل و تصویر و تقویت هماهنگی دیداری-حرکتی.",
    },
    {
        "title": "جورچین آشنایی با حیوانات جنگل",
        "slug": "jorchin-ashnayi-heyvanat-jangal",
        "age": 6,
        "topic": "شناخت حیوانات و حل مسئله",
        "benefit": "کمک به تشخیص شکل‌ها، ارتباط تصویر و افزایش توجه.",
    },
    {
        "title": "کیک نی‌نی کجایی؟",
        "slug": "cake-nini-kojayi-1",
        "age": 6,
        "topic": "جست‌وجو و کنجکاوی",
        "benefit": "فعالیت جست‌وجوی تصویری برای توجه و مشارکت کودک.",
    },
    {
        "title": "دالی چی؟ دالی کی؟",
        "slug": "dali-chi-dali-key-1",
        "age": 6,
        "topic": "زبان و تعامل",
        "benefit": "تکرار و تعامل والد و کودک برای تقویت توجه و زبان.",
    },
    {
        "title": "این سر و دست و پاشه",
        "slug": "in-sar-dast-pashe-1",
        "age": 6,
        "topic": "شناخت بدن",
        "benefit": "کمک به نام‌گذاری اعضای بدن و گسترش واژگان.",
    },
    {
        "title": "خبر داری قورباغه می‌پره، پر نداره؟",
        "slug": "khabar-dari-ghorbاغه-mipare",
        "age": 6,
        "topic": "دانش علمی و جانوران",
        "benefit": "ایجاد پرسش و پاسخ و آشنایی کودک با ویژگی‌های حیوانات.",
    },
    {
        "title": "خبر داری ماهی با چشم باز می‌خوابه؟",
        "slug": "khabar-dari-mahi-ba-cheshm-baz",
        "age": 6,
        "topic": "دانش علمی",
        "benefit": "تقویت کنجکاوی علمی و گفت‌وگو درباره رفتار جانوران.",
    },
    {
        "title": "خبر داری پاندا روی درخت می‌خوابه؟",
        "slug": "khabar-dari-panda-rooye-derakht",
        "age": 6,
        "topic": "دانش علمی و حیوانات",
        "benefit": "آشنایی با رفتار جانوران و تقویت پرسشگری.",
    },

    # =========================================================
    # 2 تا 3 سال — AgeGroup 7
    # =========================================================
    {
        "title": "جورج چه چیزی را فراموش کرده؟",
        "slug": "george-che-chizi-ra-faramoosh-karde",
        "age": 7,
        "author": "Julia Donaldson",
        "topic": "روتین و حل مسئله",
        "benefit": "کمک به دنبال‌کردن توالی اتفاقات، حل مسئله و گفت‌وگو درباره کارهای روزمره.",
    },
    {
        "title": "من هم بغل می‌خواهم",
        "slug": "man-ham-baghal-mikhaham",
        "age": 7,
        "author": "John A. Rowe",
        "topic": "ارتباط و نیاز عاطفی",
        "benefit": "مناسب برای گفت‌وگو درباره نیاز به محبت، ارتباط و احساس امنیت.",
    },
    {
        "title": "نانسی می‌داند",
        "slug": "nancy-midand",
        "age": 7,
        "author": "Sybil Young",
        "translator": "مینا پورشعبانی",
        "topic": "اعتمادبه‌نفس و شناخت خود",
        "benefit": "کمک به گفت‌وگو درباره احساسات، شناخت خود و تجربه‌های روزمره کودک.",
    },
    {
        "title": "من نبودم!",
        "slug": "man-naboodam",
        "age": 7,
        "author": "فرزانه رحمانی",
        "topic": "مسئولیت‌پذیری و رفتار",
        "benefit": "فرصتی برای گفت‌وگو درباره مسئولیت رفتار و پیامدهای انتخاب‌ها.",
    },
    {
        "title": "بنی و برادرش",
        "slug": "beni-o-baradash",
        "age": 7,
        "author": "Barbro Lindgren",
        "translator": "مینا پورشعبانی",
        "topic": "خواهر و برادر و احساسات",
        "benefit": "کمک به صحبت درباره حسادت، اختلاف و رابطه با خواهر یا برادر.",
    },
    {
        "title": "نگران نباش داگلی بغلی",
        "slug": "negaran-nabash-dogli-baghali",
        "age": 7,
        "topic": "نگرانی و امنیت عاطفی",
        "benefit": "کمک به نام‌گذاری نگرانی و گفت‌وگو درباره راه‌های آرام‌شدن.",
    },
    {
        "title": "داگلی بغلی به مدرسه کوچولوها می‌رود",
        "slug": "dogli-baghali-miravad-madrese",
        "age": 7,
        "topic": "آمادگی برای جدایی و مدرسه",
        "benefit": "کمک به گفت‌وگو درباره محیط جدید، جدایی کوتاه‌مدت و سازگاری.",
    },
    {
        "title": "مراقبم باش!",
        "slug": "moraghebam-bash",
        "age": 7,
        "topic": "ایمنی و مراقبت",
        "benefit": "فرصتی برای آموزش رفتارهای مراقبتی و گفت‌وگو درباره موقعیت‌های روزمره.",
    },
    {
        "title": "تو کوچولو هستی، نیستی",
        "slug": "to-koocholoo-hasti-nisti",
        "age": 7,
        "topic": "شناخت خود و استقلال",
        "benefit": "کمک به گفت‌وگو درباره توانایی‌ها، استقلال و شناخت خود.",
    },
    {
        "title": "این مال کیه؟ من، تو",
        "slug": "in-mal-kie-man-to",
        "age": 7,
        "topic": "مالکیت و مرزبندی",
        "benefit": "کمک به فهم مالکیت، اشتراک‌گذاری و احترام به وسایل دیگران.",
    },

    # =========================================================
    # 3 تا 4 سال — AgeGroup 8
    # =========================================================
    {
        "title": "عاشقتم کانگوروی آبی!",
        "slug": "asheghetam-kangorooye-abi",
        "age": 8,
        "author": "اما چیچستر کلارک",
        "translator": "پارسا مهین‌پور / نسرین وکیلی",
        "publisher": "مبتکران / میچکا",
        "topic": "پیوند عاطفی و دوستی",
        "benefit": "کمک به گفت‌وگو درباره دلبستگی، دوستی، احساس تعلق و کیفیت رابطه.",
        "source": "مبتکران / میچکا",
        "source_url": "https://michkapub.com/product/i-love-you-blue-kangaroo/",
        "awards": "نامزد مدال کیت گرین‌اوی؛ تأییدشده در ساماندهی منابع آموزشی و تربیتی",
    },
    {
        "title": "اتاق دوست‌داشتنی من - لطفاً در بزنید!",
        "slug": "otagh-doost-dashtani-man",
        "age": 8,
        "topic": "مرزهای شخصی و خلوت کودک",
        "benefit": "کمک به درک نیاز کودک به خلوت، مرز شخصی و احترام متقابل.",
        "source": "انتشارات میچکا",
        "source_url": MICHKA_URL,
        "awards": "برگزیده و دریافت‌کننده افتخارات داخلی و بین‌المللی",
    },
    {
        "title": "ایزی و راسو",
        "slug": "izi-o-rasoo",
        "age": 8,
        "topic": "ترس و شجاعت",
        "benefit": "کمک به گفت‌وگو درباره ترس و راه‌های مواجهه تدریجی با موقعیت‌های ناآشنا.",
        "source": "انتشارات میچکا",
        "source_url": MICHKA_URL,
    },
    {
        "title": "مامان خیلی بزرگ من",
        "slug": "maman-kheyli-bozorg-man",
        "age": 8,
        "topic": "پذیرش خود و دیگران",
        "benefit": "کمک به گفت‌وگو درباره تفاوت‌ها، پذیرش خود و احترام به دیگران.",
        "source": "انتشارات میچکا",
        "source_url": MICHKA_URL,
    },
    {
        "title": "آبی",
        "slug": "abi-sarah-christo",
        "age": 8,
        "author": "Sarah Christo",
        "topic": "تنظیم هیجان",
        "benefit": "فرصتی برای نام‌گذاری احساسات و گفت‌وگو درباره کنترل و بیان هیجان.",
        "source": "انتشارات میچکا",
        "source_url": MICHKA_URL,
    },
    {
        "title": "من می‌توانم",
        "slug": "man-mitavanam",
        "age": 8,
        "author": "Sato Ten",
        "translator": "رضوان خرمّیان",
        "topic": "توانمندی و اعتمادبه‌نفس",
        "benefit": "کمک به شناخت توانایی‌ها و تقویت نگرش رشد و تلاش.",
        "source": "انتشارات میچکا",
        "source_url": MICHKA_URL,
    },
    {
        "title": "سیرک ادب و نزاکت",
        "slug": "circ-adab-o-nezakat",
        "age": 8,
        "author": "Pierre Winters",
        "topic": "آداب اجتماعی",
        "benefit": "کمک به آموزش رفتار اجتماعی، احترام و تعامل مناسب با دیگران.",
        "source": "سامانه رشد",
        "source_url": ROSHD_URL,
        "awards": "معرفی‌شده در کتابنامه رشد دوره پیش‌دبستانی",
    },
    {
        "title": "مامان دیوید همیشه می‌گوید: نه، دیوید!",
        "slug": "na-david",
        "author": "David Shannon",
        "translator": "فرشته عبدی",
        "age": 8,
        "topic": "قواعد و رفتار",
        "benefit": "فرصتی برای گفت‌وگو درباره قانون، رفتار و پیامدهای آن بدون تحقیر کودک.",
        "source": "سامانه رشد",
        "source_url": "https://samanketab.roshdmag.ir/",
    },
    {
        "title": "مهارت‌های زندگی برای کودکان",
        "slug": "mahارت-haye-zendegi-baraye-koodakan",
        "age": 8,
        "topic": "مهارت‌های اجتماعی و ارتباطی",
        "benefit": "پرداختن به تعامل، ارتباط، خلاقیت و مهارت‌های روزمره کودک.",
        "source": "سامانه رشد",
        "source_url": "https://samanketab.roshdmag.ir/",
    },
    {
        "title": "کتاب کار مهارت‌های زندگی - پیش‌دبستانی",
        "slug": "ketab-kar-maharat-haye-zendegi-pishdabestani",
        "age": 8,
        "author": "ثنا حسین‌پور",
        "publisher": "خیلی سبز",
        "topic": "مهارت‌های اجتماعی و رفتاری",
        "benefit": "فعالیت‌هایی درباره همکاری، نظم اجتماعی، نه گفتن، احساسات و خشم.",
        "source": "سامانه رشد",
        "source_url": "https://samanketab.roshdmag.ir/",
    },

    # =========================================================
    # 4 تا 5 سال — AgeGroup 9
    # =========================================================
    {
        "title": "این گوزن مال من است",
        "slug": "in-gozhn-mal-man-ast",
        "age": 9,
        "topic": "انتخاب، قانون و مسئولیت",
        "benefit": "کمک به گفت‌وگو درباره مالکیت، قانون، انتخاب و پیامدهای رفتار.",
        "source": "انتشارات میچکا",
        "source_url": MICHKA_URL,
        "awards": "Irish Book Awards؛ New York Times Bestseller؛ تأییدشده در رشد",
    },
    {
        "title": "لوبی‌ها: من نبودم!",
        "slug": "loobia-man-naboodam",
        "age": 9,
        "topic": "حل مسئله و مسئولیت",
        "benefit": "کمک به بررسی مسئله، مسئولیت‌پذیری و گفت‌وگو درباره رفتار.",
        "source": "انتشارات میچکا",
        "source_url": MICHKA_URL,
    },
    {
        "title": "دست‌ورزی و کاردستی - مجموعه مرجع پیش‌دبستانی",
        "slug": "dastvarzi-kardasti-pishdabestani",
        "age": 9,
        "topic": "دست‌ورزی و آمادگی نوشتن",
        "benefit": "تقویت مهارت‌های دستی، هماهنگی چشم و دست و آمادگی برای فعالیت‌های نوشتاری.",
        "source": "انتشارات میچکا",
        "source_url": MICHKA_URL,
    },
    {
        "title": "نقاشی، مهارت و خلاقیت - مجموعه مرجع پیش‌دبستانی",
        "slug": "naghashi-maharat-khalaghiat",
        "age": 9,
        "topic": "خلاقیت و بیان تصویری",
        "benefit": "تقویت خلاقیت، بیان تصویری و هماهنگی حرکتی ظریف.",
        "source": "انتشارات میچکا",
        "source_url": MICHKA_URL,
    },
    {
        "title": "مهارت‌های زندگی - مجموعه مرجع پیش‌دبستانی",
        "slug": "maharat-zendegi-mojmoe-marej-pishdabestani",
        "age": 9,
        "topic": "خودآگاهی و مهارت اجتماعی",
        "benefit": "پرداختن به خودآگاهی، احساسات، ارتباط و آداب اجتماعی.",
        "source": "انتشارات میچکا",
        "source_url": MICHKA_URL,
    },
    {
        "title": "ریاضی - مجموعه مرجع پیش‌دبستانی",
        "slug": "riazi-mojmoe-marej-pishdabestani",
        "age": 9,
        "topic": "مفاهیم پایه ریاضی",
        "benefit": "تقویت مفاهیم پایه عددی و تفکر منطقی در قالب فعالیت‌های پیش‌دبستانی.",
        "source": "انتشارات میچکا",
        "source_url": MICHKA_URL,
    },
    {
        "title": "هوش - مجموعه مرجع پیش‌دبستانی",
        "slug": "hoosh-mojmoe-marej-pishdabestani",
        "age": 9,
        "topic": "تفکر و حل مسئله",
        "benefit": "تمرین‌های شناختی برای توجه، تشخیص الگو و حل مسئله.",
        "source": "انتشارات میچکا",
        "source_url": MICHKA_URL,
    },
    {
        "title": "زبان فارسی - مجموعه مرجع پیش‌دبستانی",
        "slug": "zaban-farsi-mojmoe-marej-pishdabestani",
        "age": 9,
        "topic": "زبان و آمادگی خواندن",
        "benefit": "تقویت واژگان، آگاهی زبانی و آمادگی اولیه برای خواندن.",
        "source": "انتشارات میچکا",
        "source_url": MICHKA_URL,
    },
    {
        "title": "دانش، بهداشت و جهان پیرامون - مجموعه مرجع پیش‌دبستانی",
        "slug": "danesh-behdasht-jahan-piramoon",
        "age": 9,
        "topic": "دانش عمومی و بهداشت",
        "benefit": "آشنایی کودک با بدن، بهداشت، حیوانات، گیاهان و محیط پیرامون.",
        "source": "انتشارات میچکا",
        "source_url": MICHKA_URL,
    },
    {
        "title": "کتاب زبان‌آموزی ۴ تا ۵ سال",
        "slug": "ketab-zaban-amoozi-4-5",
        "age": 9,
        "topic": "زبان و آمادگی خواندن",
        "benefit": "فعالیت‌های زبانی مناسب پیش‌دبستانی برای تقویت واژگان و آمادگی سوادآموزی.",
        "source": "سامانه رشد",
        "source_url": "https://samanketab.roshdmag.ir/",
    },
]


PARENT_BOOKS = [
    {
        "title": "کودکی با مغز تمام‌عیار",
        "slug": "whole-brain-child",
        "author": "Daniel J. Siegel / Tina Payne Bryson",
        "translator": "بنفشه عربانی",
        "publisher": "بوی کاغذ",
        "topic": "روانشناسی رشد و فرزندپروری",
        "benefit": "ارائه راهبردهایی برای درک رشد مغز کودک، تنظیم هیجان و تعامل والد و کودک.",
    },
    {
        "title": "مشکلات رفتاری کودکان: راهنمای کاربردی برای والدین",
        "slug": "behavior-problems-children",
        "author": "مهرناز سعادت",
        "publisher": "بوی کاغذ",
        "topic": "رفتار کودک و فرزندپروری",
        "benefit": "راهنمای عملی برای شناخت و مدیریت مشکلات رفتاری کودکان.",
    },
    {
        "title": "وقتی نگرانی‌های من خیلی زیاد می‌شود!",
        "slug": "when-worries-get-too-big",
        "author": "Kari Dan Baron",
        "translator": "آیناز محمدی‌زاده",
        "publisher": "بوی کاغذ",
        "topic": "اضطراب و تنظیم هیجان",
        "benefit": "فعالیت‌هایی برای کمک به کودک در شناخت نگرانی و تمرین راهکارهای آرام‌سازی.",
    },
    {
        "title": "علیه تربیت فرزند",
        "slug": "against-parenting",
        "author": "Alison Gopnik",
        "translator": "مینا قاجارگر",
        "topic": "علم فرزندپروری",
        "benefit": "نگاهی علمی و انتقادی به نقش والدین و رشد طبیعی کودک.",
    },
    {
        "title": "انضباط بدون اشک",
        "slug": "discipline-without-tears",
        "topic": "انضباط و تربیت",
        "benefit": "راهنمای تربیتی برای ایجاد نظم، مسئولیت و همکاری بدون تنبیه و تحقیر.",
    },
    {
        "title": "چگونه با کودکان کوچک صحبت کنیم تا گوش دهند",
        "slug": "how-to-talk-little-kids-will-listen",
        "author": "Joanna Faber / Julie King",
        "topic": "ارتباط والد و کودک",
        "benefit": "راهبردهای ارتباطی برای کاهش تعارض و افزایش همکاری کودک.",
    },
    {
        "title": "پرورش هوش اخلاقی کودکان و نوجوانان",
        "slug": "moral-intelligence-children",
        "author": "ساناز مهدوی‌تبار / زهره اکبری سبزواری",
        "publisher": "پرورش ذهن فرزام",
        "topic": "رشد اخلاقی",
        "benefit": "منبع والد و مربی درباره رشد اخلاقی و تربیت ارزش‌های اجتماعی.",
        "source": "سامانه رشد",
        "source_url": ROSHD_URL,
    },
    {
        "title": "راهکارهای رشد اخلاقی کودکان",
        "slug": "moral-development-children",
        "author": "ساناز مهدوی‌تبار / مژگان خانی ابیانه",
        "publisher": "پرورش ذهن فرزام",
        "topic": "رشد اخلاقی و تربیتی",
        "benefit": "راهنمای والد و مربی برای حمایت از رشد اخلاقی کودک.",
        "source": "سامانه رشد",
        "source_url": ROSHD_URL,
    },
]


class Command(BaseCommand):
    help = "Seed curated KidHub books and parent guides"

    def handle(self, *args, **options):
        age_groups = {
            age.id: age
            for age in AgeGroup.objects.filter(id__in=[4, 5, 6, 7, 8, 9])
        }

        created = 0
        updated = 0

        for item in BOOKS:
            age = age_groups[item["age"]]

            defaults = {
                "title": item["title"],
                "book_type": "text",
                "description": item.get(
                    "description",
                    f"کتابی منتخب برای گروه سنی {age.title} با تمرکز بر رشد و یادگیری کودک."
                ),
                "author": item.get("author", ""),
                "translator": item.get("translator", ""),
                "publisher": item.get("publisher", ""),
                "source_name": item.get("source", ""),
                "source_url": item.get("source_url", ""),
                "purchase_url": item.get("purchase_url", ""),
                "price": item.get("price"),
                "topic": item.get("topic", ""),
                "developmental_benefit": item.get("benefit", ""),
                "evidence_source_name": "AAP / HealthyChildren و منابع رشد",
                "evidence_source_url": item.get("evidence_url", AAP_URL),
                "awards": item.get("awards", ""),
                "is_parent_guide": False,
            }

            book, was_created = Book.objects.update_or_create(
                slug=item["slug"],
                defaults=defaults,
            )

            book.age_groups.set([age])

            if was_created:
                created += 1
            else:
                updated += 1

        for item in PARENT_BOOKS:
            defaults = {
                "title": item["title"],
                "book_type": "text",
                "description": "منبع تخصصی برای والدین و مربیان در زمینه رشد، رفتار و تربیت کودک.",
                "author": item.get("author", ""),
                "translator": item.get("translator", ""),
                "publisher": item.get("publisher", ""),
                "source_name": item.get("source", ""),
                "source_url": item.get("source_url", ""),
                "purchase_url": item.get("purchase_url", ""),
                "price": item.get("price"),
                "topic": item.get("topic", ""),
                "developmental_benefit": item.get("benefit", ""),
                "evidence_source_name": "منابع تخصصی رشد کودک و سامانه رشد",
                "evidence_source_url": item.get("evidence_url", ROSHD_URL),
                "awards": item.get("awards", ""),
                "is_parent_guide": True,
            }

            book, was_created = Book.objects.update_or_create(
                slug=item["slug"],
                defaults=defaults,
            )

            book.age_groups.clear()

            if was_created:
                created += 1
            else:
                updated += 1

        self.stdout.write("")
        self.stdout.write(self.style.SUCCESS(
            f"Book seed completed: created={created}, updated={updated}"
        ))
        self.stdout.write(
            f"Child books configured: {len(BOOKS)} | Parent guides configured: {len(PARENT_BOOKS)}"
        )
