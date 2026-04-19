import { Link, Navigate, Route, Routes, useLocation } from 'react-router-dom'

import { AnimatedThemeToggler } from './components/ui/animated-theme-toggler'
import { AskPage } from './pages/AskPage'
import { BookDetailPage } from './pages/BookDetailPage'
import { BooksPage } from './pages/BooksPage'

function NavLink({ to, children }) {
  const location = useLocation()
  const isActive = location.pathname === to || location.pathname.startsWith(to + '/')

  return (
    <Link
      to={to}
      className={`relative px-3 py-1.5 text-sm font-medium transition-colors ${
        isActive
          ? 'text-primary'
          : 'text-muted-foreground hover:text-foreground'
      }`}
    >
      {children}
      {isActive && (
        <span className="absolute bottom-0 left-1/2 h-0.5 w-6 -translate-x-1/2 rounded-full bg-primary" />
      )}
    </Link>
  )
}

function App() {
  return (
    <div className="mx-auto min-h-screen w-full max-w-5xl px-4 py-6 md:px-8 md:py-10">
      {/* Header */}
      <header
        id="app-header"
        className="mb-8 rounded-xl border border-border bg-card p-5 shadow-md transition-colors md:mb-10 md:p-6"
      >
        <div className="flex items-start justify-between">
          <div>
            <p className="text-[11px] font-semibold uppercase tracking-[0.2em] text-muted-foreground">
              ErgoSphere Assignment
            </p>
            <h1 className="mt-2 text-2xl font-semibold tracking-tight text-card-foreground md:text-3xl">
              Book Intelligence Platform
            </h1>
            <p className="mt-2 max-w-2xl text-sm text-muted-foreground">
              Browse books, run ingestion, and ask grounded RAG questions with
              citations.
            </p>
          </div>
          <AnimatedThemeToggler className="border border-border bg-card text-foreground transition-colors hover:bg-accent hover:text-accent-foreground focus-visible:ring-2 focus-visible:ring-ring" />
        </div>

        <nav className="mt-5 flex gap-1 border-t border-border pt-4">
          <NavLink to="/books">Books</NavLink>
          <NavLink to="/ask">Q&A</NavLink>
        </nav>
      </header>

      {/* Routes */}
      <main>
        <Routes>
          <Route path="/" element={<Navigate to="/books" replace />} />
          <Route path="/books" element={<BooksPage />} />
          <Route path="/books/:bookId" element={<BookDetailPage />} />
          <Route path="/ask" element={<AskPage />} />
        </Routes>
      </main>
    </div>
  )
}

export default App
