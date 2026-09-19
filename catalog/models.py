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
    affiliate_url = models.URLField(max_length=500, blank=True)
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
        AUDIO = "audio", "کتاب صوتی"
        VIDEO = "video", "ویدئو / انیمیشن"
        TEXT = "text", "کتاب متنی"

    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    age_groups = models.ManyToManyField(AgeGroup, related_name="books")
    book_type = models.CharField(max_length=10, choices=BookType.choices)
    description = models.TextField()
    cover_image = models.ImageField(upload_to="books/", blank=True, null=True)
    author = models.CharField(max_length=200, blank=True)
    translator = models.CharField(max_length=200, blank=True)
    publisher = models.CharField(max_length=200, blank=True)
    source_name = models.CharField(max_length=100, blank=True)
    source_url = models.URLField(max_length=500, blank=True)
    purchase_url = models.URLField(max_length=500, blank=True)
    price = models.PositiveIntegerField(null=True, blank=True)
    topic = models.CharField(max_length=200, blank=True)
    developmental_benefit = models.TextField(blank=True)
    evidence_source_name = models.CharField(max_length=200, blank=True)
    evidence_source_url = models.URLField(max_length=500, blank=True)
    awards = models.TextField(blank=True)
    is_parent_guide = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("book_detail", kwargs={"slug": self.slug})

class Article(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    age_groups = models.ManyToManyField(AgeGroup, related_name="articles", blank=True)
    summary = models.CharField(max_length=300)
    body = models.TextField()
    source_name = models.CharField(max_length=200, blank=True)
    source_url = models.URLField(max_length=500, blank=True)
    published_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-published_at"]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("article_detail", kwargs={"slug": self.slug})

class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.name} - {self.subject}"

from django.contrib.auth.models import User


class ChildProfile(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="child_profiles",
    )
    name = models.CharField(max_length=100)
    birth_date = models.DateField()
    interests = models.JSONField(default=list, blank=True)
    goals = models.JSONField(default=list, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.name} - {self.user.username}"






class Lullaby(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    age_groups = models.ManyToManyField(AgeGroup, related_name="lullabies", blank=True)
    description = models.TextField(blank=True)
    lyrics = models.TextField(blank=True)
    audio_file = models.FileField(upload_to="lullabies/", blank=True, null=True)
    source_name = models.CharField(max_length=200, blank=True)
    source_url = models.URLField(max_length=500, blank=True)
    is_public_domain = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["title"]

    def __str__(self):
        return self.title


class ParentLullabyRecording(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="lullaby_recordings",
    )
    child = models.ForeignKey(
        ChildProfile,
        on_delete=models.CASCADE,
        related_name="lullaby_recordings",
        null=True,
        blank=True,
    )
    lullaby = models.ForeignKey(
        Lullaby,
        on_delete=models.CASCADE,
        related_name="parent_recordings",
    )
    audio_file = models.FileField(upload_to="parent_lullabies/")
    title = models.CharField(max_length=200, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.title or f"{self.user.username} - {self.lullaby.title}"
