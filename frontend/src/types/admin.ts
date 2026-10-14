import type { Role } from "./auth";

export interface UserSummary {
  id: number;
  name: string;
  email: string;
  role: Role;
  enabled: boolean;
  createdAt: string;
}

export interface PlatformStats {
  totalUsers: number;
  totalCandidates: number;
  totalRecruiters: number;
  totalCompanies: number;
  totalProjects: number;
  enabledUsers: number;
  disabledUsers: number;
}

export interface PageResponse<T> {
  content: T[];
  totalElements: number;
  totalPages: number;
  page: number;
  last: boolean;
  size: number;
}
