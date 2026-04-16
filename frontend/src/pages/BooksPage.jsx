import { BookCard } from '@/components/BookCard'
import { useBooks } from '@/hooks/useBooks'

export function BooksPage() {
  const { books, count, loading, error, refresh } = useBooks()

  if (loading) {
    return (
      <section className="rounded-2xl border border-slate-200/80 bg-white p-8 text-slate-700">
        Loading books...
      </section>
    )
  }

  if (error) {
    return (
      <section className="rounded-2xl border border-rose-200 bg-rose-50 p-8 text-rose-900">
        <p className="font-semibold">Could not load books</p>
        <p className="mt-1 text-sm">{error}</p>
        <button
          onClick={refresh}
          className="mt-4 rounded-lg bg-rose-900 px-3 py-2 text-sm font-medium text-white"
        >
          Retry
        </button>
      </section>
    )
  }

  return (
    <section>
      <div className="mb-6 flex items-end justify-between">
        <div>
          <p className="text-xs font-semibold uppercase tracking-[0.18em] text-slate-500">
            Book Catalog
          </p>
          <h2 className="mt-2 text-2xl font-semibold tracking-tight text-slate-900">
            {count} book{count === 1 ? '' : 's'} available
          </h2>
        </div>
      </div>

      {books.length === 0 ? (
        <div className="rounded-2xl border border-amber-200 bg-amber-50 p-8 text-amber-900">
          No books found yet. Run ingestion next.
        </div>
      ) : (
        <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
          {books.map((book) => (
            <BookCard key={book.id} book={book} />
          ))}
        </div>
      )}
    </section>
  )
}
