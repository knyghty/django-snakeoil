from django.urls import path

from . import views


urlpatterns = [
    path(
        "articles/<slug:slug>/",
        views.ArticleDetailView.as_view(),
        name="article_detail",
    ),
    path("test-page/", views.TestView.as_view()),
    path("jinja2/", views.Jinja2TestView.as_view()),
    path("", views.TestView.as_view()),
]
