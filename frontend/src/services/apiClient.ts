import axios from "axios";
import type { ApiErrorResponse } from "../types/api";

// Vite exposes env vars prefixed with VITE_ via import.meta.env.
// See frontend/.env.example.
const baseURL = import.meta.env.VITE_API_BASE_URL ?? "http://localhost:8080/api";

export const apiClient = axios.create({
  baseURL,
  headers: {
    "Content-Type": "application/json",
  },
});

const TOKEN_KEY = "recruitment_platform_token";

export function getToken(): string | null {
  return localStorage.getItem(TOKEN_KEY);
}

export function setToken(token: string): void {
  localStorage.setItem(TOKEN_KEY, token);
}

export function clearToken(): void {
  localStorage.removeItem(TOKEN_KEY);
}

// Request interceptor: attach the JWT (if we have one) to every outgoing
// request. This is the "Axios request interceptor" step in the
// registration -> login -> protected request flow described in the README.
apiClient.interceptors.request.use((config) => {
  const token = getToken();
  if (token && config.headers) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

/**
 * Normalizes any Axios error into a plain, user-facing message string.
 * Components call this instead of inspecting error.response.data everywhere.
 */
export function extractErrorMessage(error: unknown): string {
  if (axios.isAxiosError<ApiErrorResponse>(error)) {
    if (!error.response) {
      return "Network error: could not reach the server. Please check your connection and try again.";
    }
    const data = error.response.data;
    if (data?.details && data.details.length > 0) {
      return data.details.join(" ");
    }
    if (data?.message) {
      return data.message;
    }
    switch (error.response.status) {
      case 401:
        return "Your session has expired. Please log in again.";
      case 403:
        return "You do not have permission to perform this action.";
      case 404:
        return "The requested resource could not be found.";
      case 409:
        return "This conflicts with existing data (e.g. an account with this email already exists).";
      default:
        return "Something went wrong. Please try again.";
    }
  }
  return "An unexpected error occurred.";
}

<<<<<<< HEAD
// The Spring backend serializes several multi-word response fields as
// snake_case (e.g. token_type, user_id, total_users) while the UI types use
// camelCase. Normalize successful JSON responses in one place.
function snakeToCamel(key: string): string {
  return key.replace(/_([a-z0-9])/g, (_, c: string) => c.toUpperCase());
}

function camelizeKeys(value: unknown): unknown {
  if (Array.isArray(value)) return value.map(camelizeKeys);
  if (value !== null && typeof value === "object" && Object.getPrototypeOf(value) === Object.prototype) {
    return Object.fromEntries(
      Object.entries(value as Record<string, unknown>).map(([k, v]) => [snakeToCamel(k), camelizeKeys(v)])
    );
  }
  return value;
}

apiClient.interceptors.response.use((response) => {
  response.data = camelizeKeys(response.data);
  return response;
});

=======
>>>>>>> 019e83b0908bbf90a27da40578fca8faea6942c8
// Response interceptor: on a 401 anywhere in the app (expired/invalid JWT),
// clear the stored token so the UI falls back to a logged-out state instead
// of silently retrying with a dead token forever.
apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    if (axios.isAxiosError(error) && error.response?.status === 401) {
      clearToken();
    }
    return Promise.reject(error);
  }
);
