from rest_framework import serializers

from .models import Book, BookInsight


class BookListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = (
            "id",
            "title",
            "author",
            "rating",
            "review_count",
            "description",
            "book_url",
            "insights_ready",
        )


class BookDetailSerializer(serializers.ModelSerializer):
    insights = serializers.SerializerMethodField()

    class Meta:
        model = Book
        fields = (
            "id",
            "title",
            "author",
            "category",
            "rating",
            "review_count",
            "price",
            "description",
            "image_url",
            "book_url",
            "insights_ready",
            "insights",
            "updated_at",
        )

    def get_insights(self, obj: Book):
        if not obj.insights_ready:
            return None

        try:
            insight = obj.insight
        except BookInsight.DoesNotExist:
            return {
                "summary": "",
                "genre": obj.category or "",
                "recommendation": "",
            }

        return {
            "summary": insight.summary_text,
            "genre": insight.genre_label or obj.category or "",
            "recommendation": insight.recommendation_text,
        }


class UploadBooksRequestSerializer(serializers.Serializer):
    source = serializers.CharField(required=False, default="books_to_scrape")
    start_url = serializers.URLField(required=False, default="https://books.toscrape.com/")
    max_pages = serializers.IntegerField(required=False, default=3, min_value=1, max_value=20)
    max_books = serializers.IntegerField(required=False, default=5, min_value=1, max_value=50)
    force_reprocess = serializers.BooleanField(required=False, default=False)
