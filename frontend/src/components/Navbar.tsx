import { NavLink } from "react-router-dom";
import { Code } from "lucide-react";
import { useAuth } from "../context/AuthContext";

const NAV_LINKS: Record<string, { to: string; label: string; icon?: React.ReactNode }[]> = {
  CANDIDATE: [
    { to: "/candidate/dashboard", label: "Dashboard" },
    { to: "/candidate/profile", label: "Profile" },
    { to: "/github", label: "GitHub", icon: <Code size={16} /> },
  ],
  RECRUITER: [
    { to: "/recruiter/dashboard", label: "Dashboard" },
    { to: "/recruiter/profile", label: "Profile" },
    { to: "/github", label: "GitHub", icon: <Code size={16} /> },
  ],
  ADMIN: [
    { to: "/admin/dashboard", label: "Dashboard" },
    { to: "/admin/users", label: "Users" },
  ],
};

export function Navbar() {
  const { user, logout } = useAuth();

  return (
    <header className="navbar">
      <div className="navbar-brand">AI Coding Assessment Platform</div>
      {user && (
        <nav className="navbar-links">
          {NAV_LINKS[user.role].map((link) => (
            <NavLink key={link.to} to={link.to} className={({ isActive }) => (isActive ? "active" : "")}>
              {link.icon && <span style={{ marginRight: "0.25rem" }}>{link.icon}</span>}
              {link.label}
              {link.to === "/github" && user.githubConnected && (
                <span className="badge" style={{ marginLeft: "0.25rem", fontSize: "0.6rem" }}>
                  ✓
                </span>
              )}
            </NavLink>
          ))}
          <div className="navbar-user">
            <span className="badge">{user.role}</span>
            <span>{user.name}</span>
            <button className="btn btn-secondary" onClick={logout}>
              Logout
            </button>
          </div>
        </nav>
      )}
    </header>
  );
}
