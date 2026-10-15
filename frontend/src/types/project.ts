export interface Project {
  id: number;
  name: string;
  description: string | null;
  repositoryUrl: string | null;
  createdAt: string;
  updatedAt: string;
}
