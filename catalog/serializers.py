from pathlib import Path

from rest_framework import serializers
from .models import AgeGroup, AffiliateSource, DevelopmentArea, Toy, Book, Article, ContactMessage, ChildProfile, Lullaby, ParentLullabyRecording


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
            "description", "cover_image", "author", "translator", "publisher",
            "source_name", "source_url", "purchase_url", "price", "topic",
            "developmental_benefit", "evidence_source_name", "evidence_source_url",
            "awards", "is_parent_guide", "created_at",
        ]


class ArticleSerializer(serializers.ModelSerializer):
    age_groups = AgeGroupSerializer(many=True, read_only=True)

    class Meta:
        model = Article
        fields = [
            "id", "title", "slug", "age_groups", "summary", "body", "source_name", "source_url", "published_at",
        ]

# ============ Registration ============
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers as drf_serializers


class RegisterSerializer(drf_serializers.ModelSerializer):
    password = drf_serializers.CharField(write_only=True, validators=[validate_password])

    class Meta:
        model = User
        fields = ["id", "username", "email", "password"]

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data["username"],
            email=validated_data.get("email", ""),
            password=validated_data["password"],
        )
        return user


class ContactMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactMessage
        fields = ["id", "name", "email", "subject", "message", "created_at", "is_read"]
        read_only_fields = ["id", "created_at", "is_read"]

class ChildProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChildProfile
        fields = [
            "id",
            "name",
            "birth_date",
            "interests",
            "goals",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]


class LullabySerializer(serializers.ModelSerializer):
    age_groups = AgeGroupSerializer(many=True, read_only=True)

    class Meta:
        model = Lullaby
        fields = [
            "id", "title", "slug", "age_groups", "description", "lyrics",
            "audio_file", "source_name", "source_url",
            "is_public_domain", "created_at",
        ]


class ParentLullabyRecordingSerializer(serializers.ModelSerializer):
    MAX_AUDIO_SIZE = 10 * 1024 * 1024
    ALLOWED_AUDIO_EXTENSIONS = {".webm", ".ogg", ".mp3", ".wav", ".mp4", ".m4a"}
    ALLOWED_AUDIO_TYPES = {
        "audio/webm",
        "audio/ogg",
        "audio/mpeg",
        "audio/wav",
        "audio/x-wav",
        "audio/mp4",
        "audio/x-m4a",
        "audio/m4a",
    }

    def validate_audio_file(self, value):
        if value.size > self.MAX_AUDIO_SIZE:
            raise serializers.ValidationError(
                "حجم فایل صوتی نباید بیشتر از 10 مگابایت باشد."
            )

        extension = Path(value.name).suffix.lower()
        content_type = getattr(value, "content_type", "")

        if extension not in self.ALLOWED_AUDIO_EXTENSIONS:
            raise serializers.ValidationError(
                "فرمت فایل صوتی مجاز نیست."
            )

        if content_type and content_type not in self.ALLOWED_AUDIO_TYPES:
            raise serializers.ValidationError(
                "نوع فایل صوتی مجاز نیست."
            )

        return value

    def validate_child(self, value):
        request = self.context.get("request")
        if request and value and value.user_id != request.user.id:
            raise serializers.ValidationError(
                "این کودک متعلق به حساب کاربری شما نیست."
            )
        return value

    class Meta:
        model = ParentLullabyRecording
        fields = [
            "id", "child", "lullaby", "audio_file",
            "title", "created_at",
        ]
        read_only_fields = ["id", "created_at"]
