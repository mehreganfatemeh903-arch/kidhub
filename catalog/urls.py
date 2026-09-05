from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("toys/", views.toy_list, name="toy_list"),
    path("toys/age/<int:age_group_id>/", views.toy_list, name="toy_list_by_age"),
    path("toys/<slug:slug>/", views.toy_detail, name="toy_detail"),
    path("books/", views.book_list, name="book_list"),
    path("books/age/<int:age_group_id>/", views.book_list, name="book_list_by_age"),
    path("articles/<slug:slug>/", views.article_detail, name="article_detail"),
]
