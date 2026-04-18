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
    <section className="space-y-6">
      <form onSubmit={onSubmit} className="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm">
        <h2 className="text-xl font-semibold text-slate-900">Ask Book Q&A (RAG)</h2>
        <p className="mt-1 text-sm text-slate-600">Ask across all books or narrow down with an optional book id.</p>

        <label className="mt-4 block text-sm font-medium text-slate-700">Question</label>
        <textarea
          value={question}
          onChange={(e) => setQuestion(e.target.value)}
          className="mt-2 min-h-28 w-full rounded-lg border border-slate-300 p-3 text-sm outline-none focus:border-sky-500"
          placeholder="What are common themes in these books?"
        />

        <label className="mt-4 block text-sm font-medium text-slate-700">Book id (optional)</label>
        <input
          value={bookId}
          onChange={(e) => setBookId(e.target.value)}
          className="mt-2 w-full rounded-lg border border-slate-300 p-3 text-sm outline-none focus:border-sky-500"
          placeholder="e.g. 1"
        />

        <button
          type="submit"
          disabled={loading}
          className="mt-4 rounded-lg bg-slate-900 px-4 py-2 text-sm font-semibold text-white disabled:opacity-60"
        >
          {loading ? 'Generating...' : 'Ask'}
        </button>

        {error ? <p className="mt-3 text-sm text-rose-700">{error}</p> : null}
      </form>

      {result ? (
        <article className="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm">
          <h3 className="text-lg font-semibold text-slate-900">Answer</h3>
          <p className="mt-3 whitespace-pre-wrap text-sm leading-7 text-slate-700">{result.answer}</p>

          <div className="mt-4 rounded-lg bg-slate-50 p-3 text-xs text-slate-700">
            Retrieval hits: {result.retrieval?.hits ?? 0} / top_k {result.retrieval?.top_k ?? 0}
          </div>

          <h4 className="mt-6 text-sm font-semibold uppercase tracking-wide text-slate-700">Citations</h4>
          <div className="mt-3 space-y-3">
            {(result.citations || []).map((citation) => (
              <div key={citation.chunk_id} className="rounded-lg border border-slate-200 p-3">
                <p className="text-sm font-semibold text-slate-900">{citation.book_title}</p>
                <p className="mt-1 text-xs text-slate-500">{citation.chunk_id}</p>
                <p className="mt-2 text-sm text-slate-700">{citation.excerpt}</p>
                <a href={citation.book_url} target="_blank" rel="noreferrer" className="mt-2 inline-flex text-xs font-medium text-sky-700">
                  Open source
                </a>
              </div>
            ))}
          </div>
        </article>
      ) : null}
    </section>
  )
}
