import { Link } from "react-router-dom";

export function UnauthorizedPage() {
  return (
    <div className="page-container">
      <div className="card">
        <h1>403 - Access denied</h1>
        <p>You don&apos;t have permission to view this page with your current role.</p>
        <Link to="/">Go home</Link>
      </div>
    </div>
  );
}
