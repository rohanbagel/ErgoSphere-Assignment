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


class BookInsight(models.Model):
	book = models.OneToOneField(Book, on_delete=models.CASCADE, related_name="insight")
	summary_text = models.TextField(blank=True)
	genre_label = models.CharField(max_length=120, blank=True)
	recommendation_text = models.TextField(blank=True)
	generated_by_model = models.CharField(max_length=120, blank=True)
	updated_at = models.DateTimeField(auto_now=True)

	class Meta:
		ordering = ["-updated_at"]


class BookChunk(models.Model):
	book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name="chunks")
	chunk_id = models.CharField(max_length=120, unique=True)
	chunk_index = models.PositiveIntegerField()
	chunk_text = models.TextField()
	token_count = models.PositiveIntegerField(default=0)
	created_at = models.DateTimeField(auto_now_add=True)

	class Meta:
		ordering = ["book_id", "chunk_index"]
		unique_together = ("book", "chunk_index")


class QAHistory(models.Model):
	question = models.TextField()
	book = models.ForeignKey(Book, null=True, blank=True, on_delete=models.SET_NULL, related_name="qa_history")
	answer = models.TextField(blank=True)
	citations_count = models.PositiveIntegerField(default=0)
	created_at = models.DateTimeField(auto_now_add=True)

	class Meta:
		ordering = ["-created_at"]
