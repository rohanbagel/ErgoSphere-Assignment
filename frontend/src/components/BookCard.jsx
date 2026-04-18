import { Link } from 'react-router-dom'

export function BookCard({ book }) {
  return (
    <article
      id={`book-card-${book.id}`}
      className="group flex flex-col rounded-xl border border-border bg-card p-5 shadow-sm transition-all duration-200 hover:-translate-y-0.5 hover:shadow-md"
    >
      <p className="text-[11px] font-semibold uppercase tracking-[0.16em] text-chart-2">
        {book.author || 'Unknown Author'}
      </p>
      <h2 className="mt-2 line-clamp-2 text-base font-semibold text-card-foreground">
        {book.title}
      </h2>
      <p className="mt-2 line-clamp-3 flex-1 text-sm text-muted-foreground">
        {book.description || 'No description available yet.'}
      </p>

      <div className="mt-4 flex items-center justify-between border-t border-border pt-3 text-xs text-muted-foreground">
        <span className="flex items-center gap-1">
          <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="currentColor" className="text-chart-1">
            <polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2" />
          </svg>
          {book.rating ?? 'N/A'}
        </span>
        <span>{book.review_count ?? 0} reviews</span>
      </div>

      <Link
        to={`/books/${book.id}`}
        className="mt-4 inline-flex items-center gap-1.5 text-sm font-medium text-primary transition-colors group-hover:text-chart-2"
      >
        Open Details
        <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
          <path d="M5 12h14" />
          <path d="m12 5 7 7-7 7" />
        </svg>
      </Link>
    </article>
  )
}
