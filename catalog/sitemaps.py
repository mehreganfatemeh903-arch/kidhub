from django.contrib.sitemaps import Sitemap
from django.urls import reverse

from .models import Toy, Book, Article


class StaticSitemap(Sitemap):
    changefreq = "weekly"
    priority = 1.0

    def items(self):
        return ["home", "toy_list", "book_list", "article_list"]

    def location(self, item):
        return reverse(item)


class ToyAgeSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.8

    def items(self):
        return [
            f"toy_age_{age.id}"
            for age in self._age_groups()
        ]

    def _age_groups(self):
        from .models import AgeGroup
        return AgeGroup.objects.all()

    def location(self, item):
        age_id = item.replace("toy_age_", "")
        return reverse("toy_list_by_age", kwargs={"age_group_id": age_id})


class BookAgeSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.8

    def items(self):
        return [
            f"book_age_{age.id}"
            for age in self._age_groups()
        ]

    def _age_groups(self):
        from .models import AgeGroup
        return AgeGroup.objects.all()

    def location(self, item):
        age_id = item.replace("book_age_", "")
        return reverse("book_list_by_age", kwargs={"age_group_id": age_id})


class ToySitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.8

    def items(self):
        return Toy.objects.all()

    def lastmod(self, obj):
        return obj.created_at


class BookSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.8

    def items(self):
        return Book.objects.all()

    def lastmod(self, obj):
        return obj.created_at


class ArticleSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.7

    def items(self):
        return Article.objects.all()

    def lastmod(self, obj):
        return obj.published_at
