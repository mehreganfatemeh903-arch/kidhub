from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import (
    AgeGroupViewSet,
    DevelopmentAreaViewSet,
    ToyViewSet,
    BookViewSet,
    ArticleViewSet,
    ChildProfileViewSet,
    RegisterView,
    ContactMessageCreateView,
    LullabyViewSet,
    ParentLullabyRecordingViewSet,
)

router = DefaultRouter()
router.register(r"age-groups", AgeGroupViewSet, basename="age-group")
router.register(r"development-areas", DevelopmentAreaViewSet, basename="development-area")
router.register(r"toys", ToyViewSet, basename="toy")
router.register(r"books", BookViewSet, basename="book")
router.register(r"articles", ArticleViewSet, basename="article")
router.register(r"child-profiles", ChildProfileViewSet, basename="child-profile")
router.register(r"lullabies", LullabyViewSet, basename="lullaby")
router.register(r"lullaby-recordings", ParentLullabyRecordingViewSet, basename="lullaby-recording")

urlpatterns = router.urls + [
    path("register/", RegisterView.as_view(), name="register"),
    path("contact/", ContactMessageCreateView.as_view(), name="contact"),
]
