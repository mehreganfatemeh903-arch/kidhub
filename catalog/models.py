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
