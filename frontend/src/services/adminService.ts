import { apiClient } from "./apiClient";
import type { PageResponse, PlatformStats, UserSummary } from "../types/admin";
import type { Role } from "../types/auth";

export const adminService = {
  getStats: () => apiClient.get<PlatformStats>("/admin/stats").then((r) => r.data),

  listUsers: (role?: Role, page = 0, size = 20) =>
    apiClient
      .get<PageResponse<UserSummary>>("/admin/users", { params: { role, page, size } })
      .then((r) => r.data),

  setUserEnabled: (id: number, enabled: boolean) =>
    apiClient.patch<UserSummary>(`/admin/users/${id}/status`, { enabled }).then((r) => r.data),
};
