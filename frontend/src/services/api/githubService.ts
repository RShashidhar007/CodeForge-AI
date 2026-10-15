import { apiClient } from "../apiClient";
import type {
  GithubOAuthUrlResponse,
  GithubRepository,
  ImportRepositoryRequest,
  ImportStatusResponse,
} from "../../types/github";

export const githubService = {
  getOAuthUrl(): Promise<GithubOAuthUrlResponse> {
    return apiClient.get("/github/oauth/authorize").then((r) => r.data);
  },

  handleOAuthCallback(code: string, state: string): Promise<{ message: string }> {
    return apiClient.post("/github/oauth/callback", { code, state }).then((r) => r.data);
  },

  listRepositories(): Promise<GithubRepository[]> {
    return apiClient.get("/github/repositories").then((r) => r.data);
  },

  importRepository(request: ImportRepositoryRequest): Promise<{ projectId: string; message: string }> {
    return apiClient.post("/github/import", request).then((r) => r.data);
  },

  getImportStatus(projectId: number): Promise<ImportStatusResponse> {
    return apiClient.get(`/github/import/${projectId}/status`).then((r) => r.data);
  },

  unlinkGithub(): Promise<{ message: string }> {
    return apiClient.delete("/github/tokens").then((r) => r.data);
  },
};
