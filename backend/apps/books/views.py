from rest_framework import generics

from .models import Book
from .serializers import BookDetailSerializer, BookListSerializer


class BookListView(generics.ListAPIView):
	queryset = Book.objects.all()
	serializer_class = BookListSerializer
	search_fields = ("title", "author", "category")
	ordering_fields = ("updated_at", "rating", "review_count")


class BookDetailView(generics.RetrieveAPIView):
	queryset = Book.objects.all()
	serializer_class = BookDetailSerializer
