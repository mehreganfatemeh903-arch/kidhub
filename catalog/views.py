from django.shortcuts import render, get_object_or_404
from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import AgeGroup, AffiliateSource, DevelopmentArea, Toy, Book, Article
from .serializers import (
    AgeGroupSerializer, AffiliateSourceSerializer, DevelopmentAreaSerializer,
    ToySerializer, BookSerializer, ArticleSerializer,
)


# ============ Template Views (صفحات وب سایت) ============

def home(request):
    age_groups = AgeGroup.objects.all()
    latest_articles = Article.objects.all()[:5]
    return render(request, "catalog/home.html", {
        "age_groups": age_groups,
        "latest_articles": latest_articles,
    })


def toy_list(request, age_group_id=None):
    age_groups = AgeGroup.objects.all()
    selected_age_group = None
    toys = Toy.objects.all()
    if age_group_id:
        selected_age_group = get_object_or_404(AgeGroup, id=age_group_id)
        toys = toys.filter(age_groups=selected_age_group)
    return render(request, "catalog/toy_list.html", {
        "age_groups": age_groups,
        "selected_age_group": selected_age_group,
        "toys": toys,
    })


def toy_detail(request, slug):
    toy = get_object_or_404(Toy, slug=slug)
    return render(request, "catalog/toy_detail.html", {"toy": toy})


def book_list(request, age_group_id=None):
    age_groups = AgeGroup.objects.all()
    selected_age_group = None
    books = Book.objects.all()
    if age_group_id:
        selected_age_group = get_object_or_404(AgeGroup, id=age_group_id)
        books = books.filter(age_groups=selected_age_group)
    return render(request, "catalog/book_list.html", {
        "age_groups": age_groups,
        "selected_age_group": selected_age_group,
        "books": books,
    })


def article_detail(request, slug):
    article = get_object_or_404(Article, slug=slug)
    return render(request, "catalog/article_detail.html", {"article": article})


# ============ API ViewSets (برای Next.js / اپلیکیشن موبایل) ============

class AgeGroupViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = AgeGroup.objects.all()
    serializer_class = AgeGroupSerializer


class DevelopmentAreaViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = DevelopmentArea.objects.all()
    serializer_class = DevelopmentAreaSerializer


class ToyViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Toy.objects.all()
    serializer_class = ToySerializer
    lookup_field = "slug"
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ["age_groups", "development_areas"]
    search_fields = ["title", "short_description"]


class BookViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    lookup_field = "slug"
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ["age_groups", "book_type"]
    search_fields = ["title", "description"]


class ArticleViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    lookup_field = "slug"
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    search_fields = ["title", "summary", "body"]