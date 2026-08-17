const TOKEN_KEY = 'mathlearnlab:token'
const APIKEY_KEY = 'mathlearnlab:apikey'

export function getAuthToken() {
  return localStorage.getItem(TOKEN_KEY) || ''
}

export function isLoggedIn() {
  return !!getAuthToken()
}

// Called when any authed request returns 401. Views can hook this (e.g. open login dialog).
export function setUnauthorizedHandler(fn) {
  unauthorizedHandler = fn
}
let unauthorizedHandler = null

export function apiFetch(url, opts = {}) {
  const headers = { ...(opts.headers || {}) }
  const token = getAuthToken()
  // Don't clobber an explicitly provided Authorization (e.g. admin secret).
  if (token && !headers['Authorization']) headers['Authorization'] = `Bearer ${token}`
  const key = localStorage.getItem(APIKEY_KEY)
  if (key) headers['X-API-Key'] = key
  return fetch(url, { ...opts, headers }).then(r => {
    if (r.status === 401 && unauthorizedHandler) unauthorizedHandler()
    return r
  })
}

// Convenience: parse JSON from a response, throwing on !ok with detail message.
export async function parseJSON(r, fallbackMsg = 'Request failed') {
  let data = {}
  try { data = await r.json() } catch {}
  if (!r.ok) throw new Error(data.detail || fallbackMsg)
  return data
}
