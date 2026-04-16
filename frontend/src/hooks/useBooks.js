import { useCallback, useEffect, useState } from 'react'

import { fetchBooks } from '@/services/api'

export function useBooks() {
  const [books, setBooks] = useState([])
  const [count, setCount] = useState(0)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')

  const loadBooks = useCallback(async () => {
    setLoading(true)
    setError('')

    try {
      const payload = await fetchBooks()
      setBooks(payload.results)
      setCount(payload.count)
    } catch (err) {
      setError(err?.message || 'Failed to load books')
      setBooks([])
      setCount(0)
    } finally {
      setLoading(false)
    }
  }, [])

  useEffect(() => {
    loadBooks()
  }, [loadBooks])

  return { books, count, loading, error, refresh: loadBooks }
}
