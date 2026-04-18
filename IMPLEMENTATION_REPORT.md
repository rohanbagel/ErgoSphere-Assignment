# RAG + AI Ingestion Implementation Report

Date: 2026-04-18

## What Was Implemented

### Backend APIs
- Existing endpoints retained:
  - `GET /api/books/`
  - `GET /api/books/{id}/`
- New endpoints added:
  - `POST /api/books/upload/` (Selenium-based ingestion trigger)
  - `GET /api/books/{id}/recommendations/` (embedding similarity recommendations)
  - `POST /api/qa/ask/` (RAG Q&A with citations)

### Data Model
Added new models in `apps.books`:
- `BookInsight`
  - `summary_text`, `genre_label`, `recommendation_text`, `generated_by_model`
- `BookChunk`
  - `chunk_id`, `chunk_index`, `chunk_text`, `token_count`
- `QAHistory`
  - `question`, `answer`, `citations_count`, optional `book`

Migration created:
- `backend/apps/books/migrations/0002_bookinsight_bookchunk_qahistory.py`

### AI / RAG Pipeline
Added new modules under `backend/apps/ai/`:
- `chunking.py`
  - overlapping chunk strategy
- `embeddings.py`
  - sentence-transformers embedding generation
- `vector_store.py`
  - Chroma upsert + query helpers
- `llm.py`
  - Groq chat completion via OpenAI-compatible client
- `rag.py`
  - indexing book chunks
  - insight generation
  - question answering with retrieved context and citations
  - recommendation generation
- `serializers.py`
  - ask payload validation
- `views.py`
  - `AskQuestionView`
- `urls.py`
  - `/api/qa/ask/`

### Ingestion Engine
Added modules under `backend/apps/ingestion/`:
- `scraper.py`
  - Selenium scraping flow for `books.toscrape.com`
- `service.py`
  - upsert books into DB
  - generate insights
  - index chunks in Chroma

### Frontend
- Added Q&A page:
  - `frontend/src/pages/AskPage.jsx`
- Updated routes:
  - `frontend/src/App.jsx` now includes `/ask`
- Added API client calls:
  - `fetchRecommendations`
  - `uploadBooks`
  - `askQuestion`
  - in `frontend/src/services/api.js`
- Books page:
  - added ingestion trigger button (`Run Ingestion`)
- Book detail page:
  - added insights display
  - added related recommendations section

## Files Changed

### Backend
- `backend/apps/books/models.py`
- `backend/apps/books/migrations/0002_bookinsight_bookchunk_qahistory.py`
- `backend/apps/books/serializers.py`
- `backend/apps/books/views.py`
- `backend/apps/books/urls.py`
- `backend/apps/books/admin.py`
- `backend/apps/books/tests.py`
- `backend/apps/ai/chunking.py`
- `backend/apps/ai/embeddings.py`
- `backend/apps/ai/vector_store.py`
- `backend/apps/ai/llm.py`
- `backend/apps/ai/rag.py`
- `backend/apps/ai/serializers.py`
- `backend/apps/ai/views.py`
- `backend/apps/ai/urls.py`
- `backend/apps/ingestion/scraper.py`
- `backend/apps/ingestion/service.py`
- `backend/config/settings.py`
- `backend/config/urls.py`
- `backend/.env.example`

### Frontend
- `frontend/src/services/api.js`
- `frontend/src/App.jsx`
- `frontend/src/pages/BooksPage.jsx`
- `frontend/src/pages/BookDetailPage.jsx`
- `frontend/src/pages/AskPage.jsx`

## Validation Completed
- `python manage.py check` -> passed
- `python manage.py test apps.books` -> passed
- `npm run build` -> passed

## Required Env Setup (Backend)
Add these to `backend/.env`:

- `GROQ_API_KEY=...`
- `GROQ_MODEL=llama-3.1-8b-instant`
- `EMBEDDING_MODEL=sentence-transformers/all-MiniLM-L6-v2`
- `CHROMA_PERSIST_DIR=./chroma_data`
- `CHROMA_COLLECTION=book_chunks`
- `SCRAPER_BASE_URL=https://books.toscrape.com/`
- `SCRAPER_DEFAULT_MAX_PAGES=3`

## Run Steps

### Backend
1. `cd backend`
2. `./.venv/Scripts/python.exe manage.py migrate`
3. `./.venv/Scripts/python.exe manage.py runserver`

### Frontend
1. `cd frontend`
2. `npm install`
3. `npm run dev`

## Demo Flow
1. Open frontend `/books`
2. Click `Run Ingestion`
3. Open any book detail to see insights + recommendations
4. Open `/ask` and query Q&A with citations
