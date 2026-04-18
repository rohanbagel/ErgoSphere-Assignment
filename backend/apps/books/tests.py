from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from unittest.mock import patch

from .models import Book


class BookApiTests(APITestCase):
	def setUp(self):
		self.book = Book.objects.create(
			title="The Silent Planet",
			author="A. Writer",
			category="Sci-Fi",
			rating=4.5,
			review_count=42,
			description="A sample record for endpoint smoke tests.",
			book_url="https://example.com/books/silent-planet",
			insights_ready=False,
		)

	def test_list_books(self):
		response = self.client.get(reverse("books:list"))

		self.assertEqual(response.status_code, status.HTTP_200_OK)
		self.assertEqual(response.data["count"], 1)
		self.assertEqual(response.data["results"][0]["title"], self.book.title)

	def test_get_book_detail(self):
		response = self.client.get(reverse("books:detail", args=[self.book.id]))

		self.assertEqual(response.status_code, status.HTTP_200_OK)
		self.assertEqual(response.data["id"], self.book.id)
		self.assertEqual(response.data["title"], self.book.title)

	@patch("apps.books.views.get_recommendations")
	def test_get_recommendations(self, mocked_recommendations):
		mocked_recommendations.return_value = [
			{
				"id": 2,
				"title": "Other Book",
				"author": "Someone",
				"score": 0.0,
				"reason": "Similar themes found.",
			}
		]

		response = self.client.get(reverse("books:recommendations", args=[self.book.id]))

		self.assertEqual(response.status_code, status.HTTP_200_OK)
		self.assertEqual(response.data["book_id"], self.book.id)
		self.assertEqual(len(response.data["recommendations"]), 1)

	@patch("apps.books.views.ingest_books")
	def test_upload_books(self, mocked_ingest):
		mocked_ingest.return_value = {
			"processed_books": 3,
			"indexed_chunks": 12,
			"source": "https://books.toscrape.com/",
		}

		response = self.client.post(
			reverse("books:upload"),
			{"start_url": "https://books.toscrape.com/", "max_pages": 1},
			format="json",
		)

		self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)
		self.assertEqual(response.data["status"], "completed")

	@patch("apps.ai.views.ask_question")
	def test_ask_question(self, mocked_ask):
		mocked_ask.return_value = {
			"answer": "Answer text [S1]",
			"citations": [
				{
					"book_id": self.book.id,
					"book_title": self.book.title,
					"book_url": self.book.book_url,
					"chunk_id": "book_1_chunk_0",
					"excerpt": "Sample excerpt",
				}
			],
			"retrieval": {"top_k": 5, "hits": 1},
		}

		response = self.client.post(
			reverse("ai:ask"),
			{"question": "What is this book about?", "book_id": self.book.id, "top_k": 5},
			format="json",
		)

		self.assertEqual(response.status_code, status.HTTP_200_OK)
		self.assertIn("answer", response.data)
		self.assertEqual(response.data["retrieval"]["hits"], 1)
