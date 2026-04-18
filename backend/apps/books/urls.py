from django.urls import path

from .views import BookDetailView, BookListView, BookRecommendationsView, BookUploadView

app_name = "books"

urlpatterns = [
    path("", BookListView.as_view(), name="list"),
    path("<int:pk>/", BookDetailView.as_view(), name="detail"),
    path("<int:pk>/recommendations/", BookRecommendationsView.as_view(), name="recommendations"),
    path("upload/", BookUploadView.as_view(), name="upload"),
]
