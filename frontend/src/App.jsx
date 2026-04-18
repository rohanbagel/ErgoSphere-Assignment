import { Navigate, Route, Routes } from 'react-router-dom'

import { AskPage } from './pages/AskPage'
import { BookDetailPage } from './pages/BookDetailPage'
import { BooksPage } from './pages/BooksPage'

function App() {
  return (
    <div className="mx-auto min-h-screen w-full max-w-6xl px-4 py-8 md:px-8 md:py-10">
      <header className="mb-8 rounded-2xl border border-slate-200/80 bg-white/80 p-6 shadow-lg shadow-slate-900/5 backdrop-blur md:mb-10">
        <p className="text-xs font-semibold uppercase tracking-[0.2em] text-sky-700">
          ErgoSphere Assignment
        </p>
        <h1 className="mt-3 text-3xl font-semibold tracking-tight text-slate-900 md:text-4xl">
          Book Intelligence Platform
        </h1>
        <p className="mt-3 max-w-3xl text-sm text-slate-700 md:text-base">
          Browse books, run ingestion, and ask grounded RAG questions with citations.
        </p>

        <div className="mt-4 flex gap-3 text-sm font-medium">
          <a href="/books" className="text-sky-700">Books</a>
          <a href="/ask" className="text-sky-700">Q&A</a>
        </div>
      </header>

      <Routes>
        <Route path="/" element={<Navigate to="/books" replace />} />
        <Route path="/books" element={<BooksPage />} />
        <Route path="/books/:bookId" element={<BookDetailPage />} />
        <Route path="/ask" element={<AskPage />} />
      </Routes>
    </div>
  )
}

export default App
