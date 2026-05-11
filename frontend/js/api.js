const API_BASE = "/api";
const STORAGE_KEY = "expenseflow.session";

function readStorage() {
  try {
    const raw = window.localStorage.getItem(STORAGE_KEY);
    return raw ? JSON.parse(raw) : null;
  } catch {
    return null;
  }
}

function writeStorage(session) {
  window.localStorage.setItem(STORAGE_KEY, JSON.stringify(session));
}

export function getSession() {
  return readStorage();
}

export function setSession(session) {
  writeStorage(session);
}

export function clearSession() {
  window.localStorage.removeItem(STORAGE_KEY);
}

export function getAccessToken() {
  return getSession()?.tokens?.access ?? null;
}

export function formatCurrency(value) {
  return new Intl.NumberFormat("en-IN", { style: "currency", currency: "INR" }).format(Number(value ?? 0));
}

export function formatDate(value) {
  if (!value) {
    return "N/A";
  }
  return new Intl.DateTimeFormat("en-US", { month: "short", day: "numeric", year: "numeric" }).format(new Date(value));
}

async function refreshAccessToken() {
  const session = getSession();
  if (!session?.tokens?.refresh) {
    clearSession();
    return null;
  }

  const response = await fetch(`${API_BASE}/auth/refresh/`, {
    method: "POST",
    headers: { "Content-Type": "application/json", Accept: "application/json" },
    body: JSON.stringify({ refresh: session.tokens.refresh }),
  });

  if (!response.ok) {
    clearSession();
    return null;
  }

  const data = await response.json();
  const nextSession = { ...session, tokens: { ...session.tokens, access: data.access } };
  setSession(nextSession);
  return data.access;
}

export async function apiRequest(path, { method = "GET", body, auth = true, headers = {} } = {}) {
  const requestHeaders = { Accept: "application/json", ...headers };
  const options = { method, headers: requestHeaders };

  if (body !== undefined) {
    requestHeaders["Content-Type"] = "application/json";
    options.body = JSON.stringify(body);
  }

  if (auth) {
    const accessToken = getAccessToken();
    if (accessToken) {
      requestHeaders.Authorization = `Bearer ${accessToken}`;
    }
  }

  let response = await fetch(`${API_BASE}${path}`, options);

  if (response.status === 401 && auth) {
    const refreshedAccess = await refreshAccessToken();
    if (refreshedAccess) {
      requestHeaders.Authorization = `Bearer ${refreshedAccess}`;
      response = await fetch(`${API_BASE}${path}`, options);
    }
  }

  const contentType = response.headers.get("content-type") || "";
  const data = contentType.includes("application/json") ? await response.json() : null;

  if (!response.ok) {
    const message = Array.isArray(data)
      ? data.join(" ")
      : data?.detail || data?.message || data?.error || "Request failed.";
    const error = new Error(message);
    error.status = response.status;
    throw error;
  }

  return data;
}
