from rest_framework import serializers

from .models import Book


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

        return {
            "summary": "",
            "genre": obj.category or "",
            "recommendation": "",
        }
