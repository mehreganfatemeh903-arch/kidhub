from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from django.urls import path, re_path, include
from django.conf import settings
from django.views.static import serve
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from catalog.sitemaps import StaticSitemap, ToyAgeSitemap, BookAgeSitemap, ToySitemap, BookSitemap, ArticleSitemap
from catalog.robots import robots_txt

sitemaps = {
    "static": StaticSitemap,
    "toy_age": ToyAgeSitemap,
    "book_age": BookAgeSitemap,
    "toys": ToySitemap,
    "books": BookSitemap,
    "articles": ArticleSitemap,
}

urlpatterns = [
    path("sitemap.xml", sitemap, {"sitemaps": sitemaps}, name="sitemap"),
    path("robots.txt", robots_txt, name="robots"),
    path("admin/", admin.site.urls),
    path("api/", include("catalog.api_urls")),
    path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    re_path(r"^media/(?P<path>.*)$", serve, {"document_root": settings.MEDIA_ROOT}),
    path("", include("catalog.urls")),
]