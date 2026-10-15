export interface GithubOAuthUrlResponse {
  authorizationUrl: string;
  state: string;
}

export interface GithubRepository {
  id: number;
  name: string;
  fullName: string;
  description: string | null;
  htmlUrl: string;
  cloneUrl: string;
  defaultBranch: string;
  language: string | null;
  private: boolean;
  stargazersCount: number;
  forksCount: number;
  openIssuesCount: number;
  pushedAt: string | null;
  createdAt: string;
  updatedAt: string;
}

export interface ImportRepositoryRequest {
  repositoryId: number;
  repositoryName: string;
  cloneUrl: string;
  defaultBranch: string;
}

export type ImportStatus = 
  | "PENDING"
  | "CLONING"
  | "INDEXING"
  | "COMPLETED"
  | "FAILED";

export interface ImportStatusResponse {
  projectId: number;
  status: ImportStatus;
  message: string;
  progress: number;
  startedAt: string | null;
  completedAt: string | null;
}

export interface SemanticSearchRequest {
  projectId: number;
  query: string;
  maxResults?: number;
}

export interface SearchResult {
  filePath: string;
  content: string;
  score: number;
  startLine: number;
  endLine: number;
  language: string | null;
}

export interface SemanticSearchResponse {
  projectId: number;
  query: string;
  results: SearchResult[];
  totalResults: number;
}
