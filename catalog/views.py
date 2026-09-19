from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import render, get_object_or_404
from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import AgeGroup, AffiliateSource, DevelopmentArea, Toy, Book, Article, ContactMessage, ChildProfile, Lullaby, ParentLullabyRecording
from .serializers import (
    AgeGroupSerializer, AffiliateSourceSerializer, DevelopmentAreaSerializer,
    ToySerializer, BookSerializer, ArticleSerializer, ContactMessageSerializer, ChildProfileSerializer, LullabySerializer, ParentLullabyRecordingSerializer,
)


# ============ Template Views ============

def home(request):
    age_groups = AgeGroup.objects.all().prefetch_related("toys", "books")
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


def article_list(request):
    articles = Article.objects.all()
    return render(request, "catalog/article_list.html", {"articles": articles})


def article_detail(request, slug):
    article = get_object_or_404(Article, slug=slug)
    return render(request, "catalog/article_detail.html", {"article": article})


# ============ API ViewSets ============

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
    filterset_fields = ["age_groups"]
    search_fields = ["title", "summary", "body"]


# ============ Registration View ============

from rest_framework import generics, permissions
from .serializers import RegisterSerializer


class RegisterView(generics.CreateAPIView):
    queryset = None
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        from django.contrib.auth.models import User
        return User.objects.all()


def book_detail(request, slug):
    book = get_object_or_404(Book, slug=slug)
    return render(request, "catalog/book_detail.html", {"book": book})


class ContactMessageCreateView(generics.CreateAPIView):
    queryset = ContactMessage.objects.all()
    serializer_class = ContactMessageSerializer
    permission_classes = [permissions.AllowAny]


class ChildProfileViewSet(viewsets.ModelViewSet):
    serializer_class = ChildProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return ChildProfile.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=True, methods=["get"])
    def recommendations(self, request, pk=None):
        child = self.get_object()
        data = recommend_for_child(child)
        return Response(data)


from .services.recommendations import recommend_for_child


class LullabyViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Lullaby.objects.all().prefetch_related("age_groups")
    serializer_class = LullabySerializer
    lookup_field = "slug"
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ["age_groups"]
    search_fields = ["title", "description"]


class ParentLullabyRecordingViewSet(viewsets.ModelViewSet):
    serializer_class = ParentLullabyRecordingSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_destroy(self, instance):
        if instance.audio_file:
            instance.audio_file.delete(save=False)
        instance.delete()

    def get_queryset(self):
        return ParentLullabyRecording.objects.filter(
            user=self.request.user
        ).select_related("child", "lullaby")

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

def search(request):
    from django.db.models import Q

    query = request.GET.get("q", "").strip()
    age_id = request.GET.get("age", "").strip()
    area_id = request.GET.get("area", "").strip()
    content_type = request.GET.get("type", "all").strip()
    sort = request.GET.get("sort", "newest").strip()

    age_groups = AgeGroup.objects.all().order_by("order")
    development_areas = DevelopmentArea.objects.all().order_by("id")

    toys = Toy.objects.all().prefetch_related(
        "age_groups",
        "development_areas",
    )

    books = Book.objects.all().prefetch_related("age_groups")

    if query:
        toys = toys.filter(
            Q(title__icontains=query)
            | Q(short_description__icontains=query)
            | Q(why_it_helps__icontains=query)
            | Q(development_areas__name__icontains=query)
        ).distinct()

        books = books.filter(
            Q(title__icontains=query)
            | Q(description__icontains=query)
            | Q(author__icontains=query)
            | Q(translator__icontains=query)
            | Q(topic__icontains=query)
            | Q(developmental_benefit__icontains=query)
        ).distinct()

    if age_id.isdigit():
        toys = toys.filter(age_groups__id=int(age_id)).distinct()
        books = books.filter(age_groups__id=int(age_id)).distinct()

    if area_id.isdigit():
        toys = toys.filter(development_areas__id=int(area_id)).distinct()
        books = Book.objects.none()

    if content_type == "toys":
        books = Book.objects.none()
    elif content_type == "books":
        toys = Toy.objects.none()

    if sort == "oldest":
        toys = toys.order_by("created_at")
        books = books.order_by("created_at")
    elif sort == "title":
        toys = toys.order_by("title")
        books = books.order_by("title")
    else:
        toys = toys.order_by("-created_at")
        books = books.order_by("-created_at")

    return render(request, "catalog/search.html", {
        "query": query,
        "toys": toys,
        "books": books,
        "age_groups": age_groups,
        "development_areas": development_areas,
        "selected_age": age_id,
        "selected_area": area_id,
        "selected_type": content_type,
        "selected_sort": sort,
    })
