from rest_framework import serializers
from .models import AgeGroup, AffiliateSource, DevelopmentArea, Toy, Book, Article


class AgeGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = AgeGroup
        fields = ["id", "title", "min_age_months", "max_age_months", "order", "description"]


class DevelopmentAreaSerializer(serializers.ModelSerializer):
    class Meta:
        model = DevelopmentArea
        fields = ["id", "name", "icon"]


class AffiliateSourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = AffiliateSource
        fields = ["id", "name", "base_url", "commission_note"]


class ToySerializer(serializers.ModelSerializer):
    age_groups = AgeGroupSerializer(many=True, read_only=True)
    development_areas = DevelopmentAreaSerializer(many=True, read_only=True)
    affiliate_source = AffiliateSourceSerializer(read_only=True)

    class Meta:
        model = Toy
        fields = [
            "id", "title", "slug", "age_groups", "development_areas",
            "short_description", "why_it_helps", "image",
            "affiliate_source", "affiliate_url", "price_range", "created_at",
        ]


class BookSerializer(serializers.ModelSerializer):
    age_groups = AgeGroupSerializer(many=True, read_only=True)

    class Meta:
        model = Book
        fields = [
            "id", "title", "slug", "age_groups", "book_type",
            "description", "cover_image", "source_name", "source_url", "created_at",
        ]


class ArticleSerializer(serializers.ModelSerializer):
    age_groups = AgeGroupSerializer(many=True, read_only=True)

    class Meta:
        model = Article
        fields = [
            "id", "title", "slug", "age_groups", "summary", "body", "published_at",
        ]