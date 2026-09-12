import { apiClient } from "./apiClient";
import type { CandidateProfile, CandidateProfileUpdateRequest } from "../types/profile";

export const candidateService = {
  getMyProfile: () => apiClient.get<CandidateProfile>("/candidates/me").then((r) => r.data),

  updateMyProfile: (payload: CandidateProfileUpdateRequest) =>
    apiClient.put<CandidateProfile>("/candidates/me", payload).then((r) => r.data),
};
