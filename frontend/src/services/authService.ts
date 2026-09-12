import { apiClient } from "./apiClient";
import type {
  LoginRequest,
  LoginResponse,
  RegisterCandidateRequest,
  RegisterRecruiterRequest,
  User,
} from "../types/auth";

export const authService = {
  registerCandidate: (payload: RegisterCandidateRequest) =>
    apiClient.post<User>("/auth/register/candidate", payload).then((r) => r.data),

  registerRecruiter: (payload: RegisterRecruiterRequest) =>
    apiClient.post<User>("/auth/register/recruiter", payload).then((r) => r.data),

  login: (payload: LoginRequest) =>
    apiClient.post<LoginResponse>("/auth/login", payload).then((r) => r.data),
};
