import { useEffect, useState } from "react";
import { adminService } from "../../services/adminService";
import { extractErrorMessage } from "../../services/apiClient";
import { Alert } from "../../components/Alert";
import { LoadingState } from "../../components/LoadingState";
import { EmptyState } from "../../components/EmptyState";
import type { Role } from "../../types/auth";
import type { UserSummary } from "../../types/admin";

const ROLE_FILTERS: { label: string; value: Role | "ALL" }[] = [
  { label: "All", value: "ALL" },
  { label: "Candidates", value: "CANDIDATE" },
  { label: "Recruiters", value: "RECRUITER" },
  { label: "Admins", value: "ADMIN" },
];

export function AdminUsersPage() {
  const [users, setUsers] = useState<UserSummary[]>([]);
  const [roleFilter, setRoleFilter] = useState<Role | "ALL">("ALL");
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  function load() {
    setIsLoading(true);
    setError(null);
    adminService
      .listUsers(roleFilter === "ALL" ? undefined : roleFilter)
      .then((page) => setUsers(page.content))
      .catch((err) => setError(extractErrorMessage(err)))
      .finally(() => setIsLoading(false));
  }

  useEffect(load, [roleFilter]);

  async function toggleEnabled(user: UserSummary) {
    try {
      const updated = await adminService.setUserEnabled(user.id, !user.enabled);
      setUsers((prev) => prev.map((u) => (u.id === updated.id ? updated : u)));
    } catch (err) {
      setError(extractErrorMessage(err));
    }
  }

  return (
    <div>
      <h1>Users</h1>
      {error && <Alert type="error" message={error} />}

      <div className="role-toggle" style={{ maxWidth: 420, marginBottom: "1.25rem" }}>
        {ROLE_FILTERS.map((f) => (
          <button
            key={f.value}
            type="button"
            className={roleFilter === f.value ? "active" : ""}
            onClick={() => setRoleFilter(f.value)}
          >
            {f.label}
          </button>
        ))}
      </div>

      <div className="card">
        {isLoading ? (
          <LoadingState label="Loading users..." />
        ) : users.length === 0 ? (
          <EmptyState message="No users found for this filter." />
        ) : (
          <table className="data-table">
            <thead>
              <tr>
                <th>Name</th>
                <th>Email</th>
                <th>Role</th>
                <th>Status</th>
                <th>Joined</th>
                <th></th>
              </tr>
            </thead>
            <tbody>
              {users.map((u) => (
                <tr key={u.id}>
                  <td>{u.name}</td>
                  <td>{u.email}</td>
                  <td>{u.role}</td>
                  <td>
                    <span className={`status-pill ${u.enabled ? "enabled" : "disabled"}`}>
                      {u.enabled ? "Enabled" : "Disabled"}
                    </span>
                  </td>
                  <td>{new Date(u.createdAt).toLocaleDateString()}</td>
                  <td>
                    {u.role !== "ADMIN" && (
                      <button className="btn btn-secondary" onClick={() => toggleEnabled(u)}>
                        {u.enabled ? "Disable" : "Enable"}
                      </button>
                    )}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </div>
    </div>
  );
}
