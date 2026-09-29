import { apiClient } from "../apiClient";

// NOTE: apiClient's baseURL already ends with the backend context path
// (/api), and it converts snake_case response keys to camelCase, so all
// types here are camelCase and paths start at /v1.

export interface SourceReference {
  file: string;
  startLine: number;
  endLine: number;
  symbol?: string;
}

export interface ChatRequest {
  question: string;
  conversationId?: number;
  topK?: number;
}

export interface ChatResponse {
  conversationId: number;
  answer: string;
  sources: SourceReference[];
  chunksRetrieved: number;
}

export interface CodeAnalysisRequest {
  code: string;
  filepath: string;
  startLine: number;
  endLine: number;
  language: string;
  testFramework?: string;
}

// The backend returns a single shape for explain/bugs/improve/tests; only the
// field relevant to the endpoint is populated.
export interface CodeAnalysisResponse {
  analysis?: string;
  explanation?: string;
  suggestions?: string;
  tests?: string;
  testFramework?: string;
  sources?: SourceReference[];
}

export type CodeExplanationRequest = CodeAnalysisRequest;
export type BugDetectionRequest = CodeAnalysisRequest;
export type CodeImprovementRequest = CodeAnalysisRequest;
export type TestGenerationRequest = CodeAnalysisRequest;
export type CodeExplanationResponse = CodeAnalysisResponse;
export type BugDetectionResponse = CodeAnalysisResponse;
export type CodeImprovementResponse = CodeAnalysisResponse;
export type TestGenerationResponse = CodeAnalysisResponse;

export interface IndexStatusResponse {
  status: string;
  totalFiles: number;
  indexedFiles: number;
  totalChunks: number;
  progress: number;
  lastIndexedAt?: string;
  lastError?: string;
}

const base = (projectId: number) => `/v1/projects/${projectId}/ai`;

export const aiService = {
  chat: (projectId: number, request: ChatRequest) =>
    apiClient.post<ChatResponse>(`${base(projectId)}/chat`, request).then((r) => r.data),

  explainCode: (projectId: number, request: CodeAnalysisRequest) =>
    apiClient.post<CodeAnalysisResponse>(`${base(projectId)}/explain`, request).then((r) => r.data),

  detectBugs: (projectId: number, request: CodeAnalysisRequest) =>
    apiClient.post<CodeAnalysisResponse>(`${base(projectId)}/bugs`, request).then((r) => r.data),

  improveCode: (projectId: number, request: CodeAnalysisRequest) =>
    apiClient.post<CodeAnalysisResponse>(`${base(projectId)}/improve`, request).then((r) => r.data),

  generateTests: (projectId: number, request: CodeAnalysisRequest) =>
    apiClient.post<CodeAnalysisResponse>(`${base(projectId)}/tests`, request).then((r) => r.data),

  getIndexingStatus: (projectId: number) =>
    apiClient.get<IndexStatusResponse>(`${base(projectId)}/status`).then((r) => r.data),

  // The backend returns the conversation's most recent answer, not the full
  // message list.
  getConversationHistory: (projectId: number, conversationId: number) =>
    apiClient.get<ChatResponse>(`${base(projectId)}/conversations/${conversationId}/history`).then((r) => r.data),
};
