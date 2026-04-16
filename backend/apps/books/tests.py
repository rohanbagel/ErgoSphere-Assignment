from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

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
