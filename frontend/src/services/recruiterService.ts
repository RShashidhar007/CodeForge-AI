import { apiClient } from "./apiClient";
import type { RecruiterProfile, RecruiterProfileUpdateRequest } from "../types/profile";

export const recruiterService = {
  getMyProfile: () => apiClient.get<RecruiterProfile>("/recruiters/me").then((r) => r.data),

  updateMyProfile: (payload: RecruiterProfileUpdateRequest) =>
    apiClient.put<RecruiterProfile>("/recruiters/me", payload).then((r) => r.data),
};
