import { useEffect, useState } from 'react'
import { Link, useParams } from 'react-router-dom'

import { fetchBook, fetchRecommendations } from '@/services/api'

export function BookDetailPage() {
  const { bookId } = useParams()
  const [book, setBook] = useState(null)
  const [recommendations, setRecommendations] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')

  useEffect(() => {
    let cancelled = false

    async function loadBook() {
      setLoading(true)
      setError('')

      try {
        const payload = await fetchBook(bookId)
        const recPayload = await fetchRecommendations(bookId)
        if (!cancelled) {
          setBook(payload)
          setRecommendations(recPayload?.recommendations || [])
        }
      } catch (err) {
        if (!cancelled) {
          setError(err?.message || 'Failed to load book details')
          setBook(null)
          setRecommendations([])
        }
      } finally {
        if (!cancelled) {
          setLoading(false)
        }
      }
    }

    loadBook()

    return () => {
      cancelled = true
    }
  }, [bookId])

  if (loading) {
    return (
      <section id="book-detail-loading" className="rounded-xl border border-border bg-card p-8 text-muted-foreground">
        <div className="flex items-center gap-3">
          <svg className="h-5 w-5 animate-spin text-primary" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
            <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" />
            <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z" />
          </svg>
          Loading details...
        </div>
      </section>
    )
  }

  if (error || !book) {
    return (
      <section id="book-detail-error" className="rounded-xl border border-destructive/30 bg-destructive/10 p-8 text-destructive">
        <p className="font-semibold">Could not load this book</p>
        <p className="mt-1 text-sm opacity-80">{error || 'Book not found.'}</p>
        <Link
          to="/books"
          className="mt-4 inline-flex rounded-lg bg-destructive px-4 py-2 text-sm font-medium text-destructive-foreground transition-colors hover:opacity-90"
        >
          Back to books
        </Link>
      </section>
    )
  }

  return (
    <article id="book-detail" className="space-y-6">
      {/* Back link */}
      <Link
        to="/books"
        className="inline-flex items-center gap-1.5 text-sm font-medium text-muted-foreground transition-colors hover:text-foreground"
      >
        <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
          <path d="m12 19-7-7 7-7" />
          <path d="M19 12H5" />
        </svg>
        Back to books
      </Link>

      {/* Main card */}
      <div className="rounded-xl border border-border bg-card p-6 shadow-sm md:p-8">
        <h2 className="text-2xl font-semibold tracking-tight text-card-foreground md:text-3xl">
          {book.title}
        </h2>
        <p className="mt-2 text-muted-foreground">By {book.author || 'Unknown Author'}</p>

        {/* Meta grid */}
        <div className="mt-6 grid gap-3 rounded-lg bg-muted p-4 text-sm text-muted-foreground md:grid-cols-3">
          <div className="flex items-center gap-2">
            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className="text-chart-2">
              <path d="M3 7V5a2 2 0 0 1 2-2h2" /><path d="M17 3h2a2 2 0 0 1 2 2v2" /><path d="M21 17v2a2 2 0 0 1-2 2h-2" /><path d="M7 21H5a2 2 0 0 1-2-2v-2" />
            </svg>
            Category: <span className="font-medium text-foreground">{book.category || 'N/A'}</span>
          </div>
          <div className="flex items-center gap-2">
            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="currentColor" className="text-chart-1">
              <polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2" />
            </svg>
            Rating: <span className="font-medium text-foreground">{book.rating ?? 'N/A'}</span>
          </div>
          <div className="flex items-center gap-2">
            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className="text-chart-3">
              <path d="M7.9 20A9 9 0 1 0 4 16.1L2 22Z" />
            </svg>
            Reviews: <span className="font-medium text-foreground">{book.review_count ?? 0}</span>
          </div>
        </div>

        {/* Description */}
        <p className="mt-6 whitespace-pre-wrap leading-7 text-muted-foreground">
          {book.description || 'No description available yet.'}
        </p>
      </div>

      {/* AI Insights */}
      {book.insights ? (
        <section id="book-insights" className="rounded-xl border border-border bg-card p-6 shadow-sm">
          <h3 className="flex items-center gap-2 text-sm font-semibold uppercase tracking-wide text-foreground">
            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className="text-chart-2">
              <path d="M12 2v4" /><path d="m6.8 14-3.5 2" /><path d="m20.7 16-3.5-2" />
              <path d="M6.5 5.5 9 8" /><path d="m17.5 5.5-2.5 2.5" />
              <circle cx="12" cy="13" r="5" />
            </svg>
            AI Insights
          </h3>
          <div className="mt-4 space-y-3 text-sm">
            <div className="rounded-lg bg-muted p-3">
              <span className="font-medium text-foreground">Summary:</span>
              <span className="ml-1 text-muted-foreground">{book.insights.summary || 'N/A'}</span>
            </div>
            <div className="rounded-lg bg-muted p-3">
              <span className="font-medium text-foreground">Genre:</span>
              <span className="ml-1 text-muted-foreground">{book.insights.genre || 'N/A'}</span>
            </div>
            <div className="rounded-lg bg-muted p-3">
              <span className="font-medium text-foreground">Recommendation:</span>
              <span className="ml-1 text-muted-foreground">{book.insights.recommendation || 'N/A'}</span>
            </div>
          </div>
        </section>
      ) : null}

      {/* Status & link */}
      <div className="flex flex-wrap items-center gap-4 rounded-xl border border-border bg-card px-6 py-4 text-sm shadow-sm">
        <span className="text-muted-foreground">
          Insights ready:{' '}
          <span className={`font-semibold ${book.insights_ready ? 'text-chart-2' : 'text-destructive'}`}>
            {book.insights_ready ? 'Yes' : 'No'}
          </span>
        </span>
        <a
          href={book.book_url}
          target="_blank"
          rel="noreferrer"
          className="inline-flex items-center gap-1.5 font-medium text-primary transition-colors hover:text-chart-2"
        >
          <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
            <path d="M15 3h6v6" /><path d="M10 14 21 3" /><path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6" />
          </svg>
          Open source page
        </a>
      </div>

      {/* Related Books */}
      <section id="related-books" className="rounded-xl border border-border bg-card p-6 shadow-sm">
        <h3 className="text-lg font-semibold text-card-foreground">Related Books</h3>
        {recommendations.length === 0 ? (
          <p className="mt-3 text-sm text-muted-foreground">No recommendations yet.</p>
        ) : (
          <ul className="mt-4 space-y-3">
            {recommendations.map((item) => (
              <li key={item.id} className="rounded-lg border border-border bg-muted p-4 transition-colors hover:bg-accent">
                <p className="font-semibold text-card-foreground">{item.title}</p>
                <p className="text-sm text-muted-foreground">{item.author}</p>
                <p className="mt-1.5 text-sm text-muted-foreground">{item.reason}</p>
              </li>
            ))}
          </ul>
        )}
      </section>
    </article>
  )
}
