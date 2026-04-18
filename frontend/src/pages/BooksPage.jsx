import { BookCard } from '@/components/BookCard'
import { useBooks } from '@/hooks/useBooks'
import { uploadBooks } from '@/services/api'

import { useState } from 'react'

export function BooksPage() {
  const { books, count, loading, error, refresh } = useBooks()
  const [ingesting, setIngesting] = useState(false)
  const [ingestError, setIngestError] = useState('')

  async function runIngestion() {
    setIngesting(true)
    setIngestError('')
    try {
      await uploadBooks({ max_pages: 2, max_books: 10 })
      await refresh()
    } catch (err) {
      setIngestError(err?.message || 'Failed to run ingestion')
    } finally {
      setIngesting(false)
    }
  }

  if (loading) {
    return (
      <section id="books-loading" className="rounded-xl border border-border bg-card p-8 text-muted-foreground">
        <div className="flex items-center gap-3">
          <svg className="h-5 w-5 animate-spin text-primary" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
            <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" />
            <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z" />
          </svg>
          Loading books...
        </div>
      </section>
    )
  }

  if (error) {
    return (
      <section id="books-error" className="rounded-xl border border-destructive/30 bg-destructive/10 p-8 text-destructive">
        <p className="font-semibold">Could not load books</p>
        <p className="mt-1 text-sm opacity-80">{error}</p>
        <button
          onClick={refresh}
          className="mt-4 rounded-lg bg-destructive px-4 py-2 text-sm font-medium text-destructive-foreground transition-colors hover:opacity-90"
        >
          Retry
        </button>
      </section>
    )
  }

  return (
    <section id="books-page">
      <div className="mb-6 flex items-end justify-between gap-4">
        <div>
          <p className="text-[11px] font-semibold uppercase tracking-[0.18em] text-muted-foreground">
            Book Catalog
          </p>
          <h2 className="mt-1.5 text-xl font-semibold tracking-tight text-foreground md:text-2xl">
            {count} book{count === 1 ? '' : 's'} available
          </h2>
        </div>
        <button
          id="run-ingestion-btn"
          onClick={runIngestion}
          disabled={ingesting}
          className="rounded-lg bg-primary px-4 py-2 text-xs font-semibold text-primary-foreground transition-colors hover:opacity-90 disabled:opacity-50"
        >
          {ingesting ? (
            <span className="flex items-center gap-2">
              <svg className="h-3.5 w-3.5 animate-spin" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" />
                <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z" />
              </svg>
              Ingesting...
            </span>
          ) : (
            'Run Ingestion'
          )}
        </button>
      </div>

      {ingestError ? (
        <div className="mb-4 rounded-lg border border-destructive/30 bg-destructive/10 p-3 text-sm text-destructive">
          {ingestError}
        </div>
      ) : null}

      {books.length === 0 ? (
        <div id="books-empty" className="rounded-xl border border-chart-1/30 bg-chart-1/10 p-8 text-center text-foreground">
          <svg xmlns="http://www.w3.org/2000/svg" width="40" height="40" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" className="mx-auto text-chart-1">
            <path d="M4 19.5v-15A2.5 2.5 0 0 1 6.5 2H19a1 1 0 0 1 1 1v18a1 1 0 0 1-1 1H6.5a1 1 0 0 1 0-5H20" />
          </svg>
          <p className="mt-3 font-medium">No books found yet</p>
          <p className="mt-1 text-sm text-muted-foreground">Run ingestion to populate the catalog.</p>
        </div>
      ) : (
        <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
          {books.map((book) => (
            <BookCard key={book.id} book={book} />
          ))}
        </div>
      )}
    </section>
  )
}
