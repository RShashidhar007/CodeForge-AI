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
  designation?: string;
  companyName?: string;
}
