import { apiClient } from "../apiClient";
import type { Project } from "../../types/project";

export const projectService = {
  listProjects(): Promise<Project[]> {
    return apiClient.get("/v1/projects").then((r) => r.data);
  },
};
