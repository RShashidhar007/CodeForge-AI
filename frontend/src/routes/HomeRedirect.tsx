import { Navigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext";
import type { Role } from "../types/auth";

const DASHBOARD_BY_ROLE: Record<Role, string> = {
  CANDIDATE: "/candidate/dashboard",
  RECRUITER: "/recruiter/dashboard",
  ADMIN: "/admin/dashboard",
};

export function HomeRedirect() {
  const { user, isLoading } = useAuth();

  if (isLoading) return null;

  return <Navigate to={user ? DASHBOARD_BY_ROLE[user.role] : "/login"} replace />;
}
