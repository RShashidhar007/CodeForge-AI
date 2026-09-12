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
  totalAdmins: number;
  totalCompanies: number;
}

export interface PageResponse<T> {
  content: T[];
  totalElements: number;
  totalPages: number;
  number: number;
  size: number;
}
