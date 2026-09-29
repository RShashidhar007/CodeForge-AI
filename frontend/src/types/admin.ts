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
<<<<<<< HEAD
  totalCompanies: number;
  totalProjects: number;
  enabledUsers: number;
  disabledUsers: number;
=======
  totalAdmins: number;
  totalCompanies: number;
>>>>>>> 019e83b0908bbf90a27da40578fca8faea6942c8
}

export interface PageResponse<T> {
  content: T[];
  totalElements: number;
  totalPages: number;
<<<<<<< HEAD
  page: number;
  last: boolean;
=======
  number: number;
>>>>>>> 019e83b0908bbf90a27da40578fca8faea6942c8
  size: number;
}
