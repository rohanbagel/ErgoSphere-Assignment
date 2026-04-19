# AI-Powered Book Intelligence Platform

> **Important (Render Free Tier Cold Start):** The backend is hosted on Render free tier, which goes idle after inactivity. The first request can take **up to 60 seconds** to wake the service, so the site may not work immediately for about a minute.

Full-stack assignment project built with Django + DRF (backend) and React + Vite + Tailwind (frontend).

## Live Deployment

- Frontend (Vercel): https://ergosphere-three.vercel.app

## Hosting Architecture

- **Vercel** is used to host and serve the React frontend (`frontend/`) as a fast static deployment.
- **Render** is used to host the Django backend API (`backend/`) and handle server-side logic/routes.
- **ChromaDB** is used as the vector database for embeddings and RAG retrieval in the Q&A pipeline.
- The frontend on Vercel calls backend APIs on Render, and the backend queries ChromaDB for retrieval-augmented responses.

## Screenshots (UI)

### 1) Books Listing Dashboard

![Books Listing Dashboard](screenshots/01-books-page.png)

### 2) Book Detail + AI Insights + Recommendations

![Book Detail Page](screenshots/02-book-detail-page.png)

### 3) Q&A (RAG) Interface

![Q&A Form](screenshots/03-ask-page-form.png)

### 4) Q&A Submitted State

![Q&A Submitted](screenshots/04-ask-page-submitted.png)

## Tech Stack

- Backend: Django, Django REST Framework
- Frontend: React (Vite), Tailwind CSS
- Scraping: Selenium
- Embeddings/RAG: sentence-transformers + ChromaDB
- LLM Integration: Groq (OpenAI-compatible API client)

## Project Structure

- `backend/` Django application and API
- `frontend/` React client
- `screenshots/` UI screenshots for submission
- `samples/` API request/response samples for testing

## Setup Instructions

### 1) Clone repository

```bash
git clone <your-repo-url>
cd ErgoSphere-Assignment
```

### 2) Backend setup

```bash
cd backend
python -m venv .venv
# Windows PowerShell
.\.venv\Scripts\Activate.ps1
# (or CMD)
# .venv\Scripts\activate.bat

pip install -r requirements.txt
```

Create `.env` in `backend/` (do not commit secrets):

```env
DJANGO_SECRET_KEY=change-me
DJANGO_DEBUG=True
DJANGO_ALLOWED_HOSTS=127.0.0.1,localhost

DB_ENGINE=sqlite
CORS_ALLOW_ALL_ORIGINS=False
CORS_ALLOWED_ORIGINS=http://127.0.0.1:5173,http://localhost:5173

GROQ_API_KEY=your_key
GROQ_MODEL=llama-3.1-8b-instant
EMBEDDING_MODEL=sentence-transformers/all-MiniLM-L6-v2
EMBEDDING_BACKEND=sentence-transformers
EMBEDDING_HASH_DIM=384

CHROMA_MODE=local
CHROMA_PERSIST_DIR=./chroma_data
CHROMA_COLLECTION=book_chunks
```

### Render 512MB Memory-Safe Configuration

If your Render free instance restarts with memory-limit errors, use lightweight hash embeddings in production:

```env
EMBEDDING_BACKEND=hash
EMBEDDING_HASH_DIM=384
SCRAPER_DEFAULT_MAX_PAGES=2
```

Why this helps:

- `sentence-transformers` can load large models into RAM and exceed 512MB.
- `hash` embeddings avoid loading ML models in-process and keep memory usage stable.
- Lower default scraper pages reduces temporary spikes during ingestion jobs.

Run migrations and backend server:

```bash
python manage.py migrate
python manage.py runserver
```

Backend runs at: `http://127.0.0.1:8000`

### 3) Frontend setup

```bash
cd ../frontend
npm install
```

Create `.env` in `frontend/`:

```env
VITE_API_BASE_URL=http://127.0.0.1:8000/api
```

Run frontend:

```bash
npm run dev
```

Frontend runs at: `http://127.0.0.1:5173`

## API Documentation

Base URL: `http://127.0.0.1:8000/api`

### 1) GET `/books/`

Purpose: List books with pagination.

Sample response shape:

```json
{
  "count": 11,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": 1,
      "title": "Demo Book",
      "author": "...",
      "category": "...",
      "rating": 4,
      "review_count": 12,
      "insights_ready": true
    }
  ]
}
```

### 2) GET `/books/{id}/`

Purpose: Fetch full details for a single book.

Includes description, insights, and metadata.

### 3) GET `/books/{id}/recommendations/`

Purpose: Return related/recommended books for a selected book.

### 4) POST `/books/upload/`

Purpose: Trigger scraping/ingestion and indexing.

Sample request:

```json
{
  "start_url": "https://books.toscrape.com/",
  "max_pages": 2,
  "max_books": 10
}
```

Sample response:

```json
{
  "status": "completed",
  "message": "Book ingestion completed",
  "result": {
    "processed": 10,
    "indexed": 10
  }
}
```

### 5) POST `/qa/ask/`

Purpose: Ask a RAG question over ingested books with citations.

Sample request:

```json
{
  "question": "List two recurring themes across the ingested books.",
  "top_k": 5
}
```

Sample response shape:

```json
{
  "answer": "...",
  "citations": [
    {
      "book_id": 3,
      "book_title": "...",
      "book_url": "...",
      "chunk_id": "S3",
      "excerpt": "..."
    }
  ],
  "retrieval": {
    "top_k": 5,
    "hits": 5
  }
}
```

## Sample Questions and Answers

### Q1

**Question:** `List two recurring themes across the ingested books.`

**Answer (from running system):**

- Challenging societal norms and hypocrisy
- Exploring connection and relationships

**Citations returned:** `5`

### Q2

**Question:** `What are the key themes of this book? (book_id=1)`

**Answer (from running system):**

- The system asked for more context when insufficient chunk context was retrieved for that specific query.

**Citations returned:** `0`

## Requirements File

Backend Python dependencies are provided in:

- `backend/requirements.txt`

## Samples for Testing

Testing samples are included in:

- `samples/api/books-upload.request.json`
- `samples/api/qa-ask.request.json`
- `samples/api/qa-ask.response.sample.json`

You can directly use these payloads in Postman or curl.

## Run Tests

```bash
cd backend
python manage.py test
```

## Submission Checklist

- [X] Code pushed to GitHub repository
- [X] README includes 3-4 UI screenshots
- [X] README includes setup instructions
- [X] README includes API documentation
- [X] README includes sample Q&A
- [X] `requirements.txt` included (`backend/requirements.txt`)
- [X] Testing samples included (`samples/`)
- [X] Fill repository link form: https://forms.gle/Fby8pMSmBJqjuVf56

## Notes

- Do not commit `.env` files or secret keys.
- Keep API keys configured through environment variables.
