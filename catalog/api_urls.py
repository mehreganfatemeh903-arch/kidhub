from rest_framework.routers import DefaultRouter
from .views import (
    AgeGroupViewSet, DevelopmentAreaViewSet,
    ToyViewSet, BookViewSet, ArticleViewSet,
)

router = DefaultRouter()
router.register(r"age-groups", AgeGroupViewSet, basename="age-group")
router.register(r"development-areas", DevelopmentAreaViewSet, basename="development-area")
router.register(r"toys", ToyViewSet, basename="toy")
router.register(r"books", BookViewSet, basename="book")
router.register(r"articles", ArticleViewSet, basename="article")

urlpatterns = router.urls