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
