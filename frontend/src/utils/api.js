const TOKEN_KEY = 'mathlearnlab:token'
const APIKEY_KEY = 'mathlearnlab:apikey'

export function getAuthToken() {
  return localStorage.getItem(TOKEN_KEY) || ''
}

export function isLoggedIn() {
  return !!getAuthToken()
}

export function apiFetch(url, opts = {}) {
  const headers = { ...(opts.headers || {}) }
  const token = getAuthToken()
  if (token) headers['Authorization'] = `Bearer ${token}`
  const key = localStorage.getItem(APIKEY_KEY)
  if (key) headers['X-API-Key'] = key
  return fetch(url, { ...opts, headers })
}
