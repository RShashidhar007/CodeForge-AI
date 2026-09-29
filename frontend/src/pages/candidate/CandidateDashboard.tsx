import { useAuth } from "../../context/AuthContext";

export function CandidateDashboard() {
  const { user } = useAuth();

  return (
    <div>
      <h1>Welcome, {user?.name}</h1>
      <p className="subtitle">This is your candidate dashboard.</p>

      <div className="card">
        <h2>Getting started</h2>
        <p>
          Your profile is the foundation for everything coming next on this platform -- coding
          assessments, AI interviews, and job matching will all read from the profile you fill in.
        </p>
        <p>Head over to your Profile page to add your skills, bio, and links.</p>
      </div>
    </div>
  );
}
