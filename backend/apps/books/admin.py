from django.contrib import admin

from .models import Book, BookChunk, BookInsight, QAHistory


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
	list_display = (
		"id",
		"title",
		"author",
		"category",
		"rating",
		"insights_ready",
		"updated_at",
	)
	search_fields = ("title", "author", "category")
	list_filter = ("category", "insights_ready")


@admin.register(BookInsight)
class BookInsightAdmin(admin.ModelAdmin):
	list_display = ("id", "book", "genre_label", "generated_by_model", "updated_at")
	search_fields = ("book__title", "genre_label")


@admin.register(BookChunk)
class BookChunkAdmin(admin.ModelAdmin):
	list_display = ("id", "book", "chunk_id", "chunk_index", "token_count", "created_at")
	search_fields = ("book__title", "chunk_id")


@admin.register(QAHistory)
class QAHistoryAdmin(admin.ModelAdmin):
	list_display = ("id", "book", "citations_count", "created_at")
	search_fields = ("question", "answer", "book__title")
