import { Navigate, Outlet } from "react-router-dom";
import { useAuth } from "../context/AuthContext";
import type { Role } from "../types/auth";

interface RoleRouteProps {
  allowedRoles: Role[];
}

/**
 * Layered on top of ProtectedRoute: also requires the user's role to be in
 * allowedRoles. E.g. <RoleRoute allowedRoles={["ADMIN"]} /> wraps
 * /admin/* routes so a logged-in CANDIDATE gets redirected instead of
 * seeing an admin page shell that all its API calls will 403 on.
 */
export function RoleRoute({ allowedRoles }: RoleRouteProps) {
  const { user } = useAuth();

  if (!user || !allowedRoles.includes(user.role)) {
    return <Navigate to="/unauthorized" replace />;
  }

  return <Outlet />;
}
