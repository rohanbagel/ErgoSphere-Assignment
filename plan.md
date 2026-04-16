# AI-Powered Book Intelligence Platform - Execution Plan

## 1) Goal and Delivery Strategy
Build a full-stack web application that:
- Scrapes and processes book data.
- Stores metadata in MySQL.
- Generates AI insights.
- Supports RAG-based question answering with source citations.
- Exposes required REST APIs.
- Provides required React + Tailwind frontend pages.

Delivery strategy:
- MVP-first for early submission advantage.
- Complete all mandatory requirements first.
- Add bonus features in strict priority order after core stability.

Deadline target:
- Hard deadline: 18 April 2026, 11:55 PM.
- Internal target for stable MVP: 18 April 2026, 5:00 PM.

## 2) Locked Tech Stack
- Backend: Django, Django REST Framework.
- Database: MySQL (metadata), ChromaDB (vectors).
- AI Provider: LM Studio (OpenAI-compatible local endpoint).
- Automation: Selenium.
- Frontend: React (JSX only) with Vite + Tailwind CSS.
- Deployment target for submission: local run instructions + screenshots + API docs in README.

## 3) Scope Mapping to Assignment Requirements
Mandatory requirements mapped:
1. Collect book data using automation.
2. Store and manage data in backend.
3. AI insight generation (minimum 2 insight types).
4. RAG question-answering over books with citations.
5. Required GET and POST APIs.
6. Frontend pages:
   - Dashboard/Book Listing
   - Book Detail
   - Q&A Interface
7. Submission quality:
   - README with setup, API docs, sample Q&A
   - 3-4 screenshots
   - requirements.txt
   - sample test data

## 4) High-Level Architecture
Data flow:
1. Selenium scraper collects raw book data from BooksToScrape.
2. Django ingestion pipeline normalizes and stores metadata in MySQL.
3. Book text is chunked with overlap and embedded.
4. Embeddings and chunk metadata are stored in ChromaDB.
5. Insight generator creates summary and genre (plus recommendation if time permits).
6. Q&A endpoint runs RAG:
   - Embed question
   - Retrieve top-k chunks
   - Build context
   - Generate answer using LM Studio
   - Return citations with chunk references
7. React frontend consumes APIs and displays data, insights, answers, and citations.

## 5) Recommended Project Structure

### Root
- backend/
- frontend/
- docs/
- samples/
- README.md
- plan.md

### Backend (Django)
- backend/manage.py
- backend/config/settings.py
- backend/config/urls.py
- backend/apps/books/models.py
- backend/apps/books/serializers.py
- backend/apps/books/views.py
- backend/apps/books/urls.py
- backend/apps/ingestion/scraper.py
- backend/apps/ingestion/service.py
- backend/apps/ai/chunking.py
- backend/apps/ai/embeddings.py
- backend/apps/ai/vector_store.py
- backend/apps/ai/insights.py
- backend/apps/ai/rag.py
- backend/requirements.txt

### Frontend (React + Vite, JSX only)
- frontend/public/
- frontend/src/main.jsx
- frontend/src/App.jsx
- frontend/src/pages/BooksPage.jsx
- frontend/src/pages/BookDetailPage.jsx
- frontend/src/pages/AskPage.jsx
- frontend/src/components/BookCard.jsx
- frontend/src/components/CitationList.jsx
- frontend/src/components/LoadingState.jsx
- frontend/src/components/ErrorState.jsx
- frontend/src/services/api.js
- frontend/src/hooks/useBooks.js
- frontend/src/hooks/useAskQuestion.js
- frontend/src/styles/index.css
- frontend/vite.config.js
- frontend/package.json

## 6) API Contract (Finalize Before Coding)

### GET /api/books/
Purpose: List uploaded books.

Response 200:
{
  "count": 120,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": 1,
      "title": "Book Name",
      "author": "Author Name",
      "rating": 4.2,
      "review_count": 321,
      "description": "...",
      "book_url": "https://...",
      "insights_ready": true
    }
  ]
}

### GET /api/books/{id}/
Purpose: Retrieve full details for one book.

Response 200:
{
  "id": 1,
  "title": "Book Name",
  "author": "Author Name",
  "rating": 4.2,
  "review_count": 321,
  "description": "...",
  "book_url": "https://...",
  "insights": {
    "summary": "...",
    "genre": "Science Fiction",
    "recommendation": "If you like X, try Y"
  },
  "updated_at": "2026-04-16T10:00:00Z"
}

### GET /api/books/{id}/recommendations/
Purpose: Related books for selected book.

Response 200:
{
  "book_id": 1,
  "recommendations": [
    {
      "id": 22,
      "title": "Related Book",
      "author": "Author 2",
      "score": 0.89,
      "reason": "Similar genre and themes"
    }
  ]
}

### POST /api/books/upload/
Purpose: Trigger scrape/upload and processing.

Request:
{
  "source": "books_to_scrape",
  "start_url": "https://books.toscrape.com/",
  "max_pages": 5,
  "force_reprocess": false
}

Response 202:
{
  "job_id": "job_123",
  "status": "queued",
  "message": "Book ingestion started"
}

### POST /api/qa/ask/
Purpose: Ask RAG question across books.

Request:
{
  "question": "What are common themes in dystopian books?",
  "book_id": null,
  "top_k": 5
}

Response 200:
{
  "answer": "...",
  "citations": [
    {
      "book_id": 1,
      "book_title": "Book Name",
      "book_url": "https://...",
      "chunk_id": "1_3",
      "excerpt": "..."
    }
  ],
  "retrieval": {
    "top_k": 5,
    "hits": 5
  }
}

Error response format (all endpoints):
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Invalid input",
    "details": {
      "field": "question"
    }
  }
}

## 7) Database and Data Model Plan

### books
- id (PK)
- title
- author
- rating
- review_count
- description
- book_url (unique)
- source
- content_hash
- insights_ready
- created_at
- updated_at

### book_chunks
- id (PK)
- book_id (FK)
- chunk_index
- chunk_text
- token_count
- metadata_json
- created_at

### book_insights
- id (PK)
- book_id (FK)
- summary_text
- genre_label
- recommendation_text (nullable)
- generated_by_model
- cache_key
- created_at

### qa_history
- id (PK)
- question
- answer
- top_k
- latency_ms
- cache_hit
- created_at

### qa_citations
- id (PK)
- qa_id (FK)
- book_id (FK)
- chunk_ref
- excerpt
- score

## 8) RAG Pipeline Design
1. Input question arrives at /api/qa/ask.
2. Normalize question and compute cache key.
3. If cached answer exists and cache valid, return cached result.
4. Generate question embedding.
5. Query ChromaDB for top_k similar chunks (optionally filter by book_id).
6. Build context window from retrieved chunks.
7. Prompt LM Studio model with context + citation instructions.
8. Parse generated answer.
9. Attach citations from retrieved chunks.
10. Store qa_history and qa_citations.
11. Return response.

Chunking strategy (advanced baseline):
- Target chunk size: 350-500 tokens.
- Overlap: 60-100 tokens.
- Split by semantic boundaries when possible (paragraph-first, fallback fixed windows).

## 9) AI Insight Plan (Minimum Two Required)
Required to implement:
1. Summary generation.
2. Genre classification.

Optional third for extra strength:
3. Recommendation logic:
   - "If you like X, you will like Y" based on embedding similarity + metadata.

## 10) Frontend Implementation Plan (React JSX + Tailwind)

### Page 1: Dashboard / Book Listing
- Search and simple filters.
- Book cards/table with required fields.
- CTA to open detail page.

### Page 2: Book Detail
- Full metadata panel.
- AI insights section.
- Link to ask question about this specific book.

### Page 3: Q&A Interface
- Question input.
- Answer output section.
- Citation list with source snippets and book links.
- Optional history panel (bonus).

UX quality requirements:
- Loading states for all async screens.
- Error states with retry button.
- Empty states for no-data scenarios.
- Mobile-first responsive layout.

## 11) Phase-Wise Build Plan (2-Day Schedule)

### Phase A (2-3 hours): Setup and contract freeze
- Scaffold backend and frontend.
- Add env files and dependency install.
- Finalize API payloads and response schema.
Deliverable: runnable skeleton with health endpoint and basic React app shell.

### Phase B (4-5 hours): Models, migrations, scraper foundation
- Implement MySQL models and migrations.
- Build Selenium scraper and ingestion service.
- Persist initial scraped dataset.
Deliverable: POST upload endpoint stores books in DB.

### Phase C (4-5 hours): Chunking, embeddings, insights
- Implement chunking and vector indexing to ChromaDB.
- Generate summary + genre for ingested books.
- Add cache for repeated insight generation.
Deliverable: book detail endpoint returns insights.

### Phase D (4-5 hours): RAG endpoint with citations
- Implement /api/qa/ask with retrieval and LM Studio generation.
- Add citation mapping and response formatting.
- Add fallback handling for low-retrieval scenarios.
Deliverable: RAG endpoint answers with sources.

### Phase E (4-5 hours): Frontend pages and integration
- Build listing, detail, and Q&A pages.
- Integrate all required backend endpoints.
- Add loading/error/empty states and responsive polish.
Deliverable: complete required UI flow.

### Phase F (2-3 hours): QA, docs, screenshots, submission prep
- End-to-end testing with sample prompts.
- Write README and API docs.
- Capture 3-4 screenshots.
- Add requirements.txt and sample test files.
Deliverable: submission-ready repository.

## 12) Bonus Feature Priority Order
Implement in this order only after MVP is stable:
1. Caching AI responses.
2. Recommendation logic as third insight.
3. Bulk or multi-page scrape improvements.
4. Save chat history in frontend and backend.
5. Celery async background jobs.

## 13) Testing and Validation Checklist

### Functional
- All required GET/POST endpoints work.
- Scrape -> process -> index -> ask flow works end-to-end.
- At least two insight types generated for each processed book.

### RAG Quality
- At least 10 benchmark questions tested.
- Every answer includes source citations.
- Retrieval hits are relevant for sampled queries.

### Frontend
- Required pages render correctly.
- API failures are handled gracefully.
- Works on desktop and mobile.

### Submission
- README includes setup, API docs, sample Q&A.
- 3-4 screenshots included.
- requirements.txt present.
- sample testing inputs present.

## 14) README Structure Plan
1. Project overview.
2. Tech stack and architecture diagram (optional but recommended).
3. Setup instructions (backend + frontend + LM Studio).
4. API documentation with examples.
5. RAG pipeline explanation and citation format.
6. Sample questions and actual answers.
7. Screenshots (3-4).
8. Limitations and future improvements.

## 15) Key Risks and Mitigation
1. LM Studio latency or model instability.
   - Mitigation: reduce top_k, trim context, cache repeated queries.
2. Scraper instability from site changes.
   - Mitigation: robust selectors, retries, graceful error logging.
3. Time overrun before deadline.
   - Mitigation: strict MVP freeze; bonus only after checklist completion.
4. Citation mismatch.
   - Mitigation: fixed citation schema tied to retrieved chunk IDs.

## 16) Immediate Next Commands (Suggested)
Backend:
1. Create Django project and app.
2. Configure MySQL and DRF.
3. Add models and run migrations.

Frontend:
1. Scaffold Vite React app in frontend/.
2. Install Tailwind and configure Vite plugin.
3. Build page routes and API service layer.

AI/RAG:
1. Start LM Studio local server.
2. Add embedding and retrieval modules.
3. Validate /api/qa/ask with citations.

## 17) Definition of Done
Project is done when:
1. All assignment-mandated APIs are implemented and testable.
2. All required frontend pages are complete and integrated.
3. RAG answers include citations.
4. At least two AI insights are generated.
5. README, screenshots, sample Q&A, requirements.txt, and samples are complete.
6. Repository is submission-ready and form link can be submitted.
