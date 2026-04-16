import { useEffect, useState } from 'react'
import { Link, useParams } from 'react-router-dom'

import { fetchBook } from '@/services/api'

export function BookDetailPage() {
  const { bookId } = useParams()
  const [book, setBook] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')

  useEffect(() => {
    let cancelled = false

    async function loadBook() {
      setLoading(true)
      setError('')

      try {
        const payload = await fetchBook(bookId)
        if (!cancelled) {
          setBook(payload)
        }
      } catch (err) {
        if (!cancelled) {
          setError(err?.message || 'Failed to load book details')
          setBook(null)
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
      <section className="rounded-2xl border border-slate-200/80 bg-white p-8 text-slate-700">
        Loading details...
      </section>
    )
  }

  if (error || !book) {
    return (
      <section className="rounded-2xl border border-rose-200 bg-rose-50 p-8 text-rose-900">
        <p className="font-semibold">Could not load this book</p>
        <p className="mt-1 text-sm">{error || 'Book not found.'}</p>
        <Link
          to="/books"
          className="mt-4 inline-flex rounded-lg bg-rose-900 px-3 py-2 text-sm font-medium text-white"
        >
          Back to books
        </Link>
      </section>
    )
  }

  return (
    <article className="rounded-2xl border border-slate-200/80 bg-white p-6 shadow-sm md:p-8">
      <Link to="/books" className="text-sm font-medium text-sky-700">
        &lt;- Back to books
      </Link>

      <h2 className="mt-4 text-3xl font-semibold tracking-tight text-slate-900">
        {book.title}
      </h2>
      <p className="mt-2 text-slate-600">By {book.author || 'Unknown Author'}</p>

      <div className="mt-6 grid gap-3 rounded-xl bg-slate-50 p-4 text-sm text-slate-700 md:grid-cols-3">
        <p>Category: {book.category || 'N/A'}</p>
        <p>Rating: {book.rating ?? 'N/A'}</p>
        <p>Reviews: {book.review_count ?? 0}</p>
      </div>

      <p className="mt-6 whitespace-pre-wrap leading-7 text-slate-700">
        {book.description || 'No description available yet.'}
      </p>

      <div className="mt-8 space-y-2 text-sm text-slate-700">
        <p>
          Insights ready:{' '}
          <span className="font-semibold">
            {book.insights_ready ? 'Yes' : 'No'}
          </span>
        </p>
        <a
          href={book.book_url}
          target="_blank"
          rel="noreferrer"
          className="inline-flex font-medium text-sky-700"
        >
          Open source page
        </a>
      </div>
    </article>
  )
}
