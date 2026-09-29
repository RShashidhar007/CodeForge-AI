export type Role = "CANDIDATE" | "RECRUITER" | "ADMIN";

export interface User {
  id: number;
  name: string;
  email: string;
  role: Role;
  enabled: boolean;
}

export interface LoginRequest {
  email: string;
  password: string;
}

export interface LoginResponse {
  token: string;
  tokenType: string;
  expiresInSeconds: number;
  user: User;
}

export interface RegisterCandidateRequest {
  name: string;
  email: string;
  password: string;
}

export interface RegisterRecruiterRequest {
  name: string;
  email: string;
  password: string;
<<<<<<< HEAD
  position?: string;
  phone?: string;
=======
  designation?: string;
  companyName?: string;
>>>>>>> 019e83b0908bbf90a27da40578fca8faea6942c8
}
