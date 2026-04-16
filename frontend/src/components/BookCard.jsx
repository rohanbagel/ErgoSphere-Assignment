import { Link } from 'react-router-dom'

export function BookCard({ book }) {
  return (
    <article className="group rounded-2xl border border-slate-200/80 bg-white p-5 shadow-sm transition hover:-translate-y-0.5 hover:shadow-md">
      <p className="text-xs font-semibold uppercase tracking-[0.16em] text-emerald-700">
        {book.author || 'Unknown Author'}
      </p>
      <h2 className="mt-2 line-clamp-2 text-lg font-semibold text-slate-900">
        {book.title}
      </h2>
      <p className="mt-3 line-clamp-3 text-sm text-slate-600">
        {book.description || 'No description available yet.'}
      </p>

      <div className="mt-4 flex items-center justify-between text-sm text-slate-700">
        <span>Rating: {book.rating ?? 'N/A'}</span>
        <span>Reviews: {book.review_count ?? 0}</span>
      </div>

      <Link
        to={`/books/${book.id}`}
        className="mt-5 inline-flex items-center gap-2 text-sm font-semibold text-sky-700 transition group-hover:text-sky-600"
      >
        Open Details
        <span aria-hidden="true">-&gt;</span>
      </Link>
    </article>
  )
}
