import { useState } from "react";
import type { FormEvent } from "react";
import { Link, useNavigate } from "react-router-dom";
import { authService } from "../../services/authService";
import { extractErrorMessage } from "../../services/apiClient";
import { Alert } from "../../components/Alert";

type RegisterRole = "CANDIDATE" | "RECRUITER";

export function RegisterPage() {
  const navigate = useNavigate();
  const [role, setRole] = useState<RegisterRole>("CANDIDATE");

  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [designation, setDesignation] = useState("");
  const [companyName, setCompanyName] = useState("");

  const [error, setError] = useState<string | null>(null);
  const [success, setSuccess] = useState<string | null>(null);
  const [isSubmitting, setIsSubmitting] = useState(false);

  async function handleSubmit(e: FormEvent) {
    e.preventDefault();
    setError(null);
    setSuccess(null);
    setIsSubmitting(true);
    try {
      if (role === "CANDIDATE") {
        await authService.registerCandidate({ name, email, password });
      } else {
        await authService.registerRecruiter({
          name,
          email,
          password,
          designation: designation || undefined,
          companyName: companyName || undefined,
        });
      }
      setSuccess("Account created! Redirecting to login...");
      setTimeout(() => navigate("/login"), 1200);
    } catch (err) {
      setError(extractErrorMessage(err));
    } finally {
      setIsSubmitting(false);
    }
  }

  return (
    <div className="auth-page">
      <div className="auth-card">
        <h1>Create your account</h1>
        <p className="subtitle">Join as a candidate or a recruiter.</p>

        <div className="role-toggle">
          <button
            type="button"
            className={role === "CANDIDATE" ? "active" : ""}
            onClick={() => setRole("CANDIDATE")}
          >
            Candidate
          </button>
          <button
            type="button"
            className={role === "RECRUITER" ? "active" : ""}
            onClick={() => setRole("RECRUITER")}
          >
            Recruiter
          </button>
        </div>

        {error && <Alert type="error" message={error} />}
        {success && <Alert type="success" message={success} />}

        <form onSubmit={handleSubmit}>
          <div className="form-group">
            <label htmlFor="name">Full name</label>
            <input id="name" value={name} onChange={(e) => setName(e.target.value)} required />
          </div>
          <div className="form-group">
            <label htmlFor="email">Email</label>
            <input
              id="email"
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
              autoComplete="email"
            />
          </div>
          <div className="form-group">
            <label htmlFor="password">Password</label>
            <input
              id="password"
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
              autoComplete="new-password"
            />
            <p className="form-hint">At least 8 characters, with an uppercase letter, lowercase letter and a digit.</p>
          </div>

          {role === "RECRUITER" && (
            <>
              <div className="form-group">
                <label htmlFor="designation">Designation (optional)</label>
                <input id="designation" value={designation} onChange={(e) => setDesignation(e.target.value)} />
              </div>
              <div className="form-group">
                <label htmlFor="companyName">Company name (optional)</label>
                <input id="companyName" value={companyName} onChange={(e) => setCompanyName(e.target.value)} />
                <p className="form-hint">Must already exist in the system. You can add this later from your profile.</p>
              </div>
            </>
          )}

          <button className="btn btn-primary" type="submit" disabled={isSubmitting}>
            {isSubmitting ? "Creating account..." : "Register"}
          </button>
        </form>

        <p className="form-footer-text">
          Already have an account? <Link to="/login">Log in</Link>
        </p>
      </div>
    </div>
  );
}
