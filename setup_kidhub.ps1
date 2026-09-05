Write-Host "Setting up KidHub project files..." -ForegroundColor Cyan

New-Item -ItemType Directory -Force -Path "templates\catalog" | Out-Null

@'
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = "django-insecure-CHANGE-THIS-IN-PRODUCTION"
DEBUG = True
ALLOWED_HOSTS = ["*"]

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "catalog",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "kidhub.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "kidhub.wsgi.application"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

LANGUAGE_CODE = "fa"
TIME_ZONE = "Asia/Tehran"
USE_I18N = True
USE_TZ = True

STATIC_URL = "static/"
STATICFILES_DIRS = [BASE_DIR / "static"]

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
'@ | Set-Content -Path "kidhub\settings.py" -Encoding UTF8
Write-Host "  kidhub/settings.py created" -ForegroundColor Green

@'
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("catalog.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
'@ | Set-Content -Path "kidhub\urls.py" -Encoding UTF8
Write-Host "  kidhub/urls.py created" -ForegroundColor Green

@'
from django.db import models
from django.urls import reverse


class AgeGroup(models.Model):
    title = models.CharField(max_length=50)
    min_age_months = models.PositiveIntegerField()
    max_age_months = models.PositiveIntegerField()
    order = models.PositiveIntegerField(default=0)
    description = models.TextField(blank=True)

    class Meta:
        ordering = ["order"]

    def __str__(self):
        return self.title


class AffiliateSource(models.Model):
    name = models.CharField(max_length=100)
    base_url = models.URLField(blank=True)
    commission_note = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.name


class DevelopmentArea(models.Model):
    name = models.CharField(max_length=50)
    icon = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return self.name


class Toy(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    age_groups = models.ManyToManyField(AgeGroup, related_name="toys")
    development_areas = models.ManyToManyField(DevelopmentArea, related_name="toys", blank=True)
    short_description = models.CharField(max_length=300)
    why_it_helps = models.TextField()
    image = models.ImageField(upload_to="toys/", blank=True, null=True)
    affiliate_source = models.ForeignKey(AffiliateSource, on_delete=models.SET_NULL, null=True, blank=True)
    affiliate_url = models.URLField(blank=True)
    price_range = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("toy_detail", kwargs={"slug": self.slug})


class Book(models.Model):
    class BookType(models.TextChoices):
        AUDIO = "audio", "صوتی"
        VIDEO = "video", "تصویری/انیمیشن"
        TEXT = "text", "متنی"

    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    age_groups = models.ManyToManyField(AgeGroup, related_name="books")
    book_type = models.CharField(max_length=10, choices=BookType.choices)
    description = models.TextField()
    cover_image = models.ImageField(upload_to="books/", blank=True, null=True)
    source_name = models.CharField(max_length=100, blank=True)
    source_url = models.URLField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.title


class Article(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    age_groups = models.ManyToManyField(AgeGroup, related_name="articles", blank=True)
    summary = models.CharField(max_length=300)
    body = models.TextField()
    published_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-published_at"]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("article_detail", kwargs={"slug": self.slug})
'@ | Set-Content -Path "catalog\models.py" -Encoding UTF8
Write-Host "  catalog/models.py created" -ForegroundColor Green

@'
from django.contrib import admin
from .models import AgeGroup, AffiliateSource, DevelopmentArea, Toy, Book, Article


@admin.register(AgeGroup)
class AgeGroupAdmin(admin.ModelAdmin):
    list_display = ("title", "min_age_months", "max_age_months", "order")
    ordering = ("order",)


@admin.register(AffiliateSource)
class AffiliateSourceAdmin(admin.ModelAdmin):
    list_display = ("name", "base_url", "commission_note")


@admin.register(DevelopmentArea)
class DevelopmentAreaAdmin(admin.ModelAdmin):
    list_display = ("name",)


@admin.register(Toy)
class ToyAdmin(admin.ModelAdmin):
    list_display = ("title", "affiliate_source", "price_range", "created_at")
    list_filter = ("age_groups", "development_areas", "affiliate_source")
    search_fields = ("title", "short_description")
    prepopulated_fields = {"slug": ("title",)}
    filter_horizontal = ("age_groups", "development_areas")


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ("title", "book_type", "source_name", "created_at")
    list_filter = ("age_groups", "book_type")
    search_fields = ("title",)
    prepopulated_fields = {"slug": ("title",)}
    filter_horizontal = ("age_groups",)


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ("title", "published_at")
    search_fields = ("title", "body")
    prepopulated_fields = {"slug": ("title",)}
    filter_horizontal = ("age_groups",)
'@ | Set-Content -Path "catalog\admin.py" -Encoding UTF8
Write-Host "  catalog/admin.py created" -ForegroundColor Green

@'
from django.shortcuts import render, get_object_or_404
from .models import AgeGroup, Toy, Book, Article


def home(request):
    age_groups = AgeGroup.objects.all()
    latest_articles = Article.objects.all()[:4]
    return render(request, "catalog/home.html", {
        "age_groups": age_groups,
        "latest_articles": latest_articles,
    })


def toy_list(request, age_group_id=None):
    toys = Toy.objects.all()
    age_group = None
    if age_group_id:
        age_group = get_object_or_404(AgeGroup, pk=age_group_id)
        toys = toys.filter(age_groups=age_group)
    return render(request, "catalog/toy_list.html", {
        "toys": toys,
        "age_groups": AgeGroup.objects.all(),
        "selected_age_group": age_group,
    })


def toy_detail(request, slug):
    toy = get_object_or_404(Toy, slug=slug)
    related = Toy.objects.filter(age_groups__in=toy.age_groups.all()).exclude(id=toy.id).distinct()[:4]
    return render(request, "catalog/toy_detail.html", {"toy": toy, "related": related})


def book_list(request, age_group_id=None):
    books = Book.objects.all()
    age_group = None
    if age_group_id:
        age_group = get_object_or_404(AgeGroup, pk=age_group_id)
        books = books.filter(age_groups=age_group)
    return render(request, "catalog/book_list.html", {
        "books": books,
        "age_groups": AgeGroup.objects.all(),
        "selected_age_group": age_group,
    })


def article_detail(request, slug):
    article = get_object_or_404(Article, slug=slug)
    return render(request, "catalog/article_detail.html", {"article": article})
'@ | Set-Content -Path "catalog\views.py" -Encoding UTF8
Write-Host "  catalog/views.py created" -ForegroundColor Green

@'
from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("toys/", views.toy_list, name="toy_list"),
    path("toys/age/<int:age_group_id>/", views.toy_list, name="toy_list_by_age"),
    path("toys/<slug:slug>/", views.toy_detail, name="toy_detail"),
    path("books/", views.book_list, name="book_list"),
    path("books/age/<int:age_group_id>/", views.book_list, name="book_list_by_age"),
    path("articles/<slug:slug>/", views.article_detail, name="article_detail"),
]
'@ | Set-Content -Path "catalog\urls.py" -Encoding UTF8
Write-Host "  catalog/urls.py created" -ForegroundColor Green

@'
<!DOCTYPE html>
<html lang="fa" dir="rtl">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{% block title %}راهنمای رشد کودک{% endblock %}</title>
  <style>
    body { font-family: Tahoma, sans-serif; margin: 0; background: #fdf9f3; color: #333; }
    header { background: #ff9f68; padding: 16px 24px; }
    header a { color: white; text-decoration: none; font-weight: bold; margin-left: 16px; }
    .container { max-width: 1000px; margin: 0 auto; padding: 24px; }
    .card { background: white; border-radius: 10px; padding: 16px; margin-bottom: 16px; box-shadow: 0 1px 4px rgba(0,0,0,0.08); }
    .age-badges a { display: inline-block; background: #ffe3cc; padding: 6px 14px; border-radius: 20px; margin: 4px; text-decoration: none; color: #b85c00; font-size: 14px; }
    .btn-buy { display: inline-block; background: #2e8b57; color: white; padding: 8px 16px; border-radius: 6px; text-decoration: none; margin-top: 8px; }
    footer { text-align: center; padding: 24px; color: #999; font-size: 13px; }
  </style>
</head>
<body>
  <header>
    <a href="{% url 'home' %}">خانه</a>
    <a href="{% url 'toy_list' %}">اسباب‌بازی‌ها</a>
    <a href="{% url 'book_list' %}">کتابخانه</a>
  </header>
  <div class="container">
    {% block content %}{% endblock %}
  </div>
  <footer>راهنمای رشد کودک — محتوا صرفاً جنبه‌ی اطلاع‌رسانی دارد.</footer>
</body>
</html>
'@ | Set-Content -Path "templates\base.html" -Encoding UTF8
Write-Host "  templates/base.html created" -ForegroundColor Green

@'
{% extends "base.html" %}
{% block content %}
  <h1>کودک شما چند سالشه؟</h1>
  <p>بازه‌ی سنی رو انتخاب کن تا اسباب‌بازی و کتاب مناسب رشدش رو ببینی.</p>
  <div class="age-badges">
    {% for age in age_groups %}
      <a href="{% url 'toy_list_by_age' age.id %}">{{ age.title }}</a>
    {% endfor %}
  </div>

  {% if latest_articles %}
    <h2 style="margin-top:32px;">آخرین مطالب</h2>
    {% for article in latest_articles %}
      <div class="card">
        <a href="{{ article.get_absolute_url }}"><strong>{{ article.title }}</strong></a>
        <p>{{ article.summary }}</p>
      </div>
    {% endfor %}
  {% endif %}
{% endblock %}
'@ | Set-Content -Path "templates\catalog\home.html" -Encoding UTF8
Write-Host "  templates/catalog/home.html created" -ForegroundColor Green

@'
{% extends "base.html" %}
{% block content %}
  <h1>{% if selected_age_group %}اسباب‌بازی مناسب {{ selected_age_group.title }}{% else %}همه‌ی اسباب‌بازی‌ها{% endif %}</h1>

  <div class="age-badges">
    <a href="{% url 'toy_list' %}">همه</a>
    {% for age in age_groups %}
      <a href="{% url 'toy_list_by_age' age.id %}">{{ age.title }}</a>
    {% endfor %}
  </div>

  {% for toy in toys %}
    <div class="card">
      <h3><a href="{{ toy.get_absolute_url }}">{{ toy.title }}</a></h3>
      <p>{{ toy.short_description }}</p>
    </div>
  {% empty %}
    <p>هنوز اسباب‌بازی‌ای برای این سن ثبت نشده.</p>
  {% endfor %}
{% endblock %}
'@ | Set-Content -Path "templates\catalog\toy_list.html" -Encoding UTF8
Write-Host "  templates/catalog/toy_list.html created" -ForegroundColor Green

@'
{% extends "base.html" %}
{% block content %}
  <div class="card">
    {% if toy.image %}<img src="{{ toy.image.url }}" style="max-width:100%;border-radius:8px;">{% endif %}
    <h1>{{ toy.title }}</h1>
    <p>{{ toy.short_description }}</p>

    <h3>چرا برای رشد کودک مفیده؟</h3>
    <p>{{ toy.why_it_helps }}</p>

    <p><strong>مناسب برای:</strong>
      {% for age in toy.age_groups.all %}{{ age.title }}{% if not forloop.last %}، {% endif %}{% endfor %}
    </p>

    {% if toy.price_range %}<p><strong>بازه‌ی قیمت:</strong> {{ toy.price_range }}</p>{% endif %}

    {% if toy.affiliate_url %}
      <a class="btn-buy" href="{{ toy.affiliate_url }}" target="_blank" rel="nofollow noopener">
        مشاهده و خرید {% if toy.affiliate_source %}از {{ toy.affiliate_source.name }}{% endif %}
      </a>
    {% endif %}
  </div>
{% endblock %}
'@ | Set-Content -Path "templates\catalog\toy_detail.html" -Encoding UTF8
Write-Host "  templates/catalog/toy_detail.html created" -ForegroundColor Green

@'
{% extends "base.html" %}
{% block content %}
  <h1>{% if selected_age_group %}کتاب مناسب {{ selected_age_group.title }}{% else %}کتابخانه{% endif %}</h1>
  <div class="age-badges">
    <a href="{% url 'book_list' %}">همه</a>
    {% for age in age_groups %}
      <a href="{% url 'book_list_by_age' age.id %}">{{ age.title }}</a>
    {% endfor %}
  </div>
  {% for book in books %}
    <div class="card">
      <h3>{{ book.title }} <small>({{ book.get_book_type_display }})</small></h3>
      <p>{{ book.description }}</p>
      {% if book.source_url %}<a href="{{ book.source_url }}" target="_blank">مشاهده در {{ book.source_name }}</a>{% endif %}
    </div>
  {% empty %}
    <p>هنوز کتابی برای این سن ثبت نشده.</p>
  {% endfor %}
{% endblock %}
'@ | Set-Content -Path "templates\catalog\book_list.html" -Encoding UTF8
Write-Host "  templates/catalog/book_list.html created" -ForegroundColor Green

@'
{% extends "base.html" %}
{% block content %}
  <div class="card">
    <h1>{{ article.title }}</h1>
    <p>{{ article.body|linebreaks }}</p>
  </div>
{% endblock %}
'@ | Set-Content -Path "templates\catalog\article_detail.html" -Encoding UTF8
Write-Host "  templates/catalog/article_detail.html created" -ForegroundColor Green

Write-Host ""
Write-Host "All files created successfully!" -ForegroundColor Cyan
Write-Host "Next steps:" -ForegroundColor Yellow
Write-Host "  python manage.py makemigrations catalog"
Write-Host "  python manage.py migrate"
Write-Host "  python manage.py createsuperuser"
Write-Host "  python manage.py runserver"
