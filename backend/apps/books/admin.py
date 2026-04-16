from django.contrib import admin

from .models import Book


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
