import { useAuth } from '@/stores/auth'

const TOKEN_KEY = 'mathlearnlab:token'
const APIKEY_KEY = 'mathlearnlab:apikey'

export function getAuthToken() {
  return localStorage.getItem(TOKEN_KEY) || ''
}

export function isLoggedIn() {
  return !!getAuthToken()
}

// Called when any authed request returns 401 after a failed refresh. Views can
// hook this (e.g. open login dialog).
export function setUnauthorizedHandler(fn) {
  unauthorizedHandler = fn
}
let unauthorizedHandler = null

// Deduplicated sliding-refresh: concurrent 401s share one refresh call.
let refreshPromise = null

function refreshToken() {
  if (refreshPromise) return refreshPromise
  refreshPromise = fetch('/api/auth/refresh', {
    method: 'POST',
    headers: { 'Authorization': `Bearer ${getAuthToken()}` },
  })
    .then(r => {
      if (!r.ok) throw new Error('refresh failed')
      return r.json()
    })
    .then(d => {
      localStorage.setItem(TOKEN_KEY, d.token)
      if (d.user) localStorage.setItem('mathlearnlab:user', JSON.stringify(d.user))
      // Keep the in-memory store in sync.
      try { useAuth().setToken(d.token, d.user) } catch {}
      return d
    })
    .finally(() => { refreshPromise = null })
  return refreshPromise
}

function buildHeaders(opts) {
  const headers = { ...(opts.headers || {}) }
  // explicitAuth means the caller set Authorization themselves (e.g. admin
  // secret) — don't attach the JWT and don't auto-refresh on its 401.
  const explicitAuth = !!headers['Authorization']
  const token = getAuthToken()
  if (token && !explicitAuth) headers['Authorization'] = `Bearer ${token}`
  const key = localStorage.getItem(APIKEY_KEY)
  if (key) headers['X-API-Key'] = key
  return { headers, explicitAuth }
}

export function apiFetch(url, opts = {}) {
  const { headers, explicitAuth } = buildHeaders(opts)
  const doFetch = () => fetch(url, { ...opts, headers })

  return doFetch().then(async r => {
    if (r.status === 401 && !explicitAuth && getAuthToken()) {
      // Token expired — try one sliding refresh, then retry the request once.
      try {
        await refreshToken()
        const rebuilt = buildHeaders(opts)
        return fetch(url, { ...opts, headers: rebuilt.headers })
      } catch {
        localStorage.removeItem(TOKEN_KEY)
        try { useAuth().logout() } catch {}
        if (unauthorizedHandler) unauthorizedHandler()
        return r
      }
    }
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
