from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.ai.rag import get_recommendations
from apps.ingestion.service import ingest_books
from .models import Book
from .serializers import BookDetailSerializer, BookListSerializer, UploadBooksRequestSerializer


class BookListView(generics.ListAPIView):
	queryset = Book.objects.all()
	serializer_class = BookListSerializer
	search_fields = ("title", "author", "category")
	ordering_fields = ("updated_at", "rating", "review_count")


class BookDetailView(generics.RetrieveAPIView):
	queryset = Book.objects.all()
	serializer_class = BookDetailSerializer


class BookRecommendationsView(APIView):
	def get(self, request, pk: int):
		book = generics.get_object_or_404(Book, pk=pk)
		recommendations = get_recommendations(book)
		return Response(
			{
				"book_id": book.id,
				"recommendations": recommendations,
			},
			status=status.HTTP_200_OK,
		)


class BookUploadView(APIView):
	def post(self, request):
		serializer = UploadBooksRequestSerializer(data=request.data)
		serializer.is_valid(raise_exception=True)
		payload = serializer.validated_data

		result = ingest_books(
			start_url=payload.get("start_url", "https://books.toscrape.com/"),
			max_pages=payload.get("max_pages", 3),
			max_books=payload.get("max_books", 5),
		)

		return Response(
			{
				"status": "completed",
				"message": "Book ingestion completed",
				"result": result,
			},
			status=status.HTTP_202_ACCEPTED,
		)
