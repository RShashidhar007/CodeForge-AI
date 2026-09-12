import { useAuth } from "../../context/AuthContext";

export function RecruiterDashboard() {
  const { user } = useAuth();

  return (
    <div>
      <h1>Welcome, {user?.name}</h1>
      <p className="subtitle">This is your recruiter dashboard.</p>

      <div className="card">
        <h2>Getting started</h2>
        <p>
          Job postings, candidate matching, and assessment creation will be added here in later
          stages of the platform. For now, set up your profile and company details.
        </p>
      </div>
    </div>
  );
}
