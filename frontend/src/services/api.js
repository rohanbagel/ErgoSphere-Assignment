import axios from 'axios'

const baseURL = import.meta.env.VITE_API_BASE_URL || 'http://127.0.0.1:8000/api'

const api = axios.create({
  baseURL,
  timeout: 10000,
})

export async function fetchBooks() {
  const response = await api.get('/books/')
  const payload = response.data

  if (Array.isArray(payload)) {
    return { count: payload.length, results: payload }
  }

  return {
    count: payload.count ?? 0,
    results: payload.results ?? [],
  }
}

export async function fetchBook(bookId) {
  const response = await api.get(`/books/${bookId}/`)
  return response.data
}
