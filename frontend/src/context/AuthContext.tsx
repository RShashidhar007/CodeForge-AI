import { createContext, useContext, useEffect, useMemo, useState } from "react";
import type { ReactNode } from "react";
import type { LoginRequest, User } from "../types/auth";
import { authService } from "../services/authService";
import { clearToken, getToken, setToken } from "../services/apiClient";

interface AuthContextValue {
  user: User | null;
  isAuthenticated: boolean;
  isLoading: boolean;
  login: (payload: LoginRequest) => Promise<User>;
  logout: () => void;
}

const AuthContext = createContext<AuthContextValue | undefined>(undefined);

const USER_KEY = "recruitment_platform_user";

/**
 * Holds the logged-in user's info in React state (the "Authentication
 * state" step of the login flow) and persists it + the JWT to localStorage
 * so a page refresh doesn't log the user out. On first mount we just restore
 * whatever was persisted; we intentionally don't re-validate the token
 * against the backend here to keep Month 1 simple -- an expired token will
 * simply get a 401 on the next protected request, which the Axios response
 * interceptor turns into a clean logout.
 */
export function AuthProvider({ children }: { children: ReactNode }) {
  const [user, setUser] = useState<User | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    const token = getToken();
    const storedUser = localStorage.getItem(USER_KEY);
    if (token && storedUser) {
      try {
        setUser(JSON.parse(storedUser) as User);
      } catch {
        clearToken();
        localStorage.removeItem(USER_KEY);
      }
    }
    setIsLoading(false);
  }, []);

  const login = async (payload: LoginRequest): Promise<User> => {
    const response = await authService.login(payload);
    setToken(response.token);
    localStorage.setItem(USER_KEY, JSON.stringify(response.user));
    setUser(response.user);
    return response.user;
  };

  const logout = () => {
    clearToken();
    localStorage.removeItem(USER_KEY);
    setUser(null);
  };

  const value = useMemo<AuthContextValue>(
    () => ({ user, isAuthenticated: !!user, isLoading, login, logout }),
    [user, isLoading]
  );

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}

export function useAuth(): AuthContextValue {
  const ctx = useContext(AuthContext);
  if (!ctx) {
    throw new Error("useAuth must be used within an AuthProvider");
  }
  return ctx;
}
