import { useEffect, useState } from "react";
import { adminService } from "../../services/adminService";
import { extractErrorMessage } from "../../services/apiClient";
import { Alert } from "../../components/Alert";
import { LoadingState } from "../../components/LoadingState";
import type { PlatformStats } from "../../types/admin";

export function AdminDashboard() {
  const [stats, setStats] = useState<PlatformStats | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    adminService
      .getStats()
      .then(setStats)
      .catch((err) => setError(extractErrorMessage(err)))
      .finally(() => setIsLoading(false));
  }, []);

  if (isLoading) return <LoadingState label="Loading platform stats..." />;

  return (
    <div>
      <h1>Admin Dashboard</h1>
      {error && <Alert type="error" message={error} />}

      {stats && (
        <div className="stats-grid">
          <div className="stat-tile">
            <div className="value">{stats.totalUsers}</div>
            <div className="label">Total users</div>
          </div>
          <div className="stat-tile">
            <div className="value">{stats.totalCandidates}</div>
            <div className="label">Candidates</div>
          </div>
          <div className="stat-tile">
            <div className="value">{stats.totalRecruiters}</div>
            <div className="label">Recruiters</div>
          </div>
          <div className="stat-tile">
            <div className="value">{stats.totalAdmins}</div>
            <div className="label">Admins</div>
          </div>
          <div className="stat-tile">
            <div className="value">{stats.totalCompanies}</div>
            <div className="label">Companies</div>
          </div>
        </div>
      )}
    </div>
  );
}
