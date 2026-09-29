import { Navigate, Outlet, useLocation } from "react-router-dom";
import { useAuth } from "../context/AuthContext";

/**
 * Gate for any route that requires "logged in, any role". Redirects to
 * /login (remembering where the user was headed) if there's no user.
 *
 * IMPORTANT (also called out in the README): this only controls what the
 * React app *renders*. It is a UX convenience, not a security boundary --
 * the real enforcement happens server-side via Spring Security's
 * @PreAuthorize rules and the JWT filter. A user could disable JavaScript
 * and this check entirely; they still could not call a protected API
 * without a valid token for the right role.
 */
export function ProtectedRoute() {
  const { isAuthenticated, isLoading } = useAuth();
  const location = useLocation();

  if (isLoading) {
    return <div className="page-loading">Loading...</div>;
  }

  if (!isAuthenticated) {
    return <Navigate to="/login" state={{ from: location }} replace />;
  }

  return <Outlet />;
}
