from django.db import models


class Book(models.Model):
	title = models.CharField(max_length=255)
	author = models.CharField(max_length=255, blank=True, default="Unknown")
	category = models.CharField(max_length=120, blank=True)
	rating = models.DecimalField(max_digits=3, decimal_places=1, null=True, blank=True)
	review_count = models.PositiveIntegerField(default=0)
	price = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
	description = models.TextField(blank=True)
	image_url = models.URLField(blank=True)
	book_url = models.URLField(unique=True)
	source = models.CharField(max_length=100, default="books_to_scrape")
	insights_ready = models.BooleanField(default=False)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	class Meta:
		ordering = ["-updated_at"]

	def __str__(self) -> str:
		return self.title
