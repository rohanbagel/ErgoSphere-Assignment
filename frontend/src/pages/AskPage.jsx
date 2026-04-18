import { useState } from 'react'

import { askQuestion } from '@/services/api'

export function AskPage() {
  const [question, setQuestion] = useState('')
  const [bookId, setBookId] = useState('')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')
  const [result, setResult] = useState(null)

  async function onSubmit(event) {
    event.preventDefault()
    if (!question.trim()) {
      setError('Please enter a question.')
      return
    }

    setLoading(true)
    setError('')
    setResult(null)

    try {
      const payload = {
        question: question.trim(),
        top_k: 5,
      }
      if (bookId.trim()) {
        payload.book_id = Number(bookId)
      }

      const response = await askQuestion(payload)
      setResult(response)
    } catch (err) {
      setError(err?.response?.data?.detail || err?.message || 'Failed to get answer')
    } finally {
      setLoading(false)
    }
  }

  return (
    <section id="ask-page" className="space-y-6">
      {/* Question form */}
      <form
        id="ask-form"
        onSubmit={onSubmit}
        className="rounded-xl border border-border bg-card p-6 shadow-sm"
      >
        <div className="flex items-center gap-2">
          <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className="text-chart-2">
            <circle cx="12" cy="12" r="10" />
            <path d="M9.09 9a3 3 0 0 1 5.83 1c0 2-3 3-3 3" />
            <path d="M12 17h.01" />
          </svg>
          <h2 className="text-lg font-semibold text-card-foreground">Ask Book Q&A (RAG)</h2>
        </div>
        <p className="mt-1.5 text-sm text-muted-foreground">
          Ask across all books or narrow down with an optional book ID.
        </p>

        <div className="mt-5 space-y-4">
          <div>
            <label htmlFor="question-input" className="block text-sm font-medium text-foreground">
              Question
            </label>
            <textarea
              id="question-input"
              value={question}
              onChange={(e) => setQuestion(e.target.value)}
              className="mt-1.5 min-h-28 w-full rounded-lg border border-input bg-background p-3 text-sm text-foreground placeholder:text-muted-foreground outline-none transition-colors focus:border-ring focus:ring-1 focus:ring-ring"
              placeholder="What are common themes in these books?"
            />
          </div>

          <div>
            <label htmlFor="book-id-input" className="block text-sm font-medium text-foreground">
              Book ID <span className="text-muted-foreground">(optional)</span>
            </label>
            <input
              id="book-id-input"
              value={bookId}
              onChange={(e) => setBookId(e.target.value)}
              className="mt-1.5 w-full rounded-lg border border-input bg-background p-3 text-sm text-foreground placeholder:text-muted-foreground outline-none transition-colors focus:border-ring focus:ring-1 focus:ring-ring"
              placeholder="e.g. 1"
            />
          </div>
        </div>

        <button
          id="ask-submit-btn"
          type="submit"
          disabled={loading}
          className="mt-5 rounded-lg bg-primary px-5 py-2.5 text-sm font-semibold text-primary-foreground transition-colors hover:opacity-90 disabled:opacity-50"
        >
          {loading ? (
            <span className="flex items-center gap-2">
              <svg className="h-4 w-4 animate-spin" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" />
                <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z" />
              </svg>
              Generating...
            </span>
          ) : (
            'Ask'
          )}
        </button>

        {error ? (
          <p className="mt-3 text-sm text-destructive">{error}</p>
        ) : null}
      </form>

      {/* Answer result */}
      {result ? (
        <article id="ask-result" className="space-y-6">
          {/* Answer card */}
          <div className="rounded-xl border border-border bg-card p-6 shadow-sm">
            <h3 className="flex items-center gap-2 text-lg font-semibold text-card-foreground">
              <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className="text-chart-2">
                <path d="M12 2v4" /><path d="m6.8 14-3.5 2" /><path d="m20.7 16-3.5-2" />
                <path d="M6.5 5.5 9 8" /><path d="m17.5 5.5-2.5 2.5" />
                <circle cx="12" cy="13" r="5" />
              </svg>
              Answer
            </h3>
            <p className="mt-3 whitespace-pre-wrap text-sm leading-7 text-muted-foreground">
              {result.answer}
            </p>

            <div className="mt-4 rounded-lg bg-muted px-3 py-2 text-xs text-muted-foreground">
              Retrieval hits: <span className="font-medium text-foreground">{result.retrieval?.hits ?? 0}</span> / top_k <span className="font-medium text-foreground">{result.retrieval?.top_k ?? 0}</span>
            </div>
          </div>

          {/* Citations */}
          <div className="rounded-xl border border-border bg-card p-6 shadow-sm">
            <h4 className="flex items-center gap-2 text-sm font-semibold uppercase tracking-wide text-foreground">
              <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className="text-chart-1">
                <path d="M4 19.5v-15A2.5 2.5 0 0 1 6.5 2H19a1 1 0 0 1 1 1v18a1 1 0 0 1-1 1H6.5a1 1 0 0 1 0-5H20" />
              </svg>
              Citations
            </h4>
            <div className="mt-4 space-y-3">
              {(result.citations || []).map((citation) => (
                <div
                  key={citation.chunk_id}
                  className="rounded-lg border border-border bg-muted p-4 transition-colors hover:bg-accent"
                >
                  <div className="flex items-start justify-between gap-3">
                    <div>
                      <p className="text-sm font-semibold text-card-foreground">{citation.book_title}</p>
                      <p className="mt-0.5 font-mono text-xs text-muted-foreground">{citation.chunk_id}</p>
                    </div>
                    <a
                      href={citation.book_url}
                      target="_blank"
                      rel="noreferrer"
                      className="shrink-0 text-xs font-medium text-primary transition-colors hover:text-chart-2"
                    >
                      Open source →
                    </a>
                  </div>
                  <p className="mt-2 text-sm leading-6 text-muted-foreground">{citation.excerpt}</p>
                </div>
              ))}
            </div>
          </div>
        </article>
      ) : null}
    </section>
  )
}
