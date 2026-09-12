import api from './axiosConfig';

export interface ChatRequest {
  question: string;
  conversation_id?: number;
  top_k?: number;
}

export interface ChatResponse {
  conversation_id: number;
  answer: string;
  sources: Array<{
    file: string;
    start_line: number;
    end_line: number;
    symbol?: string;
  }>;
  chunks_retrieved: number;
}

export interface CodeExplanationRequest {
  code: string;
  filepath: string;
  start_line: number;
  end_line: number;
  language: string;
}

export interface CodeExplanationResponse {
  explanation: string;
  sources: Array<{
    file: string;
    start_line: number;
    end_line: number;
  }>;
}

export interface BugDetectionRequest {
  code: string;
  filepath: string;
  start_line: number;
  end_line: number;
  language: string;
}

export interface BugDetectionResponse {
  analysis: string;
  sources: Array<{
    file: string;
    start_line: number;
    end_line: number;
  }>;
}

export interface CodeImprovementRequest {
  code: string;
  filepath: string;
  start_line: number;
  end_line: number;
  language: string;
}

export interface CodeImprovementResponse {
  suggestions: string;
  sources: Array<{
    file: string;
    start_line: number;
    end_line: number;
  }>;
}

export interface TestGenerationRequest {
  code: string;
  filepath: string;
  start_line: number;
  end_line: number;
  language: string;
  test_framework?: string;
}

export interface TestGenerationResponse {
  tests: string;
  test_framework: string;
  sources: Array<{
    file: string;
    start_line: number;
    end_line: number;
  }>;
}

export interface IndexStatusResponse {
  status: string;
  total_files: number;
  indexed_files: number;
  total_chunks: number;
  progress: number;
  last_indexed_at?: string;
  last_error?: string;
}

export interface ConversationMessage {
  role: 'user' | 'assistant';
  content: string;
  created_at: string;
  sources?: string;
}

export interface ConversationHistoryResponse {
  messages: ConversationMessage[];
  conversation_id: number;
}

class AIService {
  /**
   * Chat with AI about the repository
   */
  async chat(
    projectId: number,
    request: ChatRequest
  ): Promise<ChatResponse> {
    const response = await api.post<ChatResponse>(
      `/api/v1/projects/${projectId}/ai/chat`,
      request
    );
    return response.data;
  }

  /**
   * Explain selected code
   */
  async explainCode(
    projectId: number,
    request: CodeExplanationRequest
  ): Promise<CodeExplanationResponse> {
    const response = await api.post<CodeExplanationResponse>(
      `/api/v1/projects/${projectId}/ai/explain`,
      request
    );
    return response.data;
  }

  /**
   * Detect bugs in code
   */
  async detectBugs(
    projectId: number,
    request: BugDetectionRequest
  ): Promise<BugDetectionResponse> {
    const response = await api.post<BugDetectionResponse>(
      `/api/v1/projects/${projectId}/ai/bugs`,
      request
    );
    return response.data;
  }

  /**
   * Get code improvement suggestions
   */
  async improveCode(
    projectId: number,
    request: CodeImprovementRequest
  ): Promise<CodeImprovementResponse> {
    const response = await api.post<CodeImprovementResponse>(
      `/api/v1/projects/${projectId}/ai/improve`,
      request
    );
    return response.data;
  }

  /**
   * Generate unit tests
   */
  async generateTests(
    projectId: number,
    request: TestGenerationRequest
  ): Promise<TestGenerationResponse> {
    const response = await api.post<TestGenerationResponse>(
      `/api/v1/projects/${projectId}/ai/tests`,
      request
    );
    return response.data;
  }

  /**
   * Get repository indexing status
   */
  async getIndexingStatus(
    projectId: number
  ): Promise<IndexStatusResponse> {
    const response = await api.get<IndexStatusResponse>(
      `/api/v1/projects/${projectId}/ai/status`
    );
    return response.data;
  }

  /**
   * Get conversation history
   */
  async getConversationHistory(
    projectId: number,
    conversationId: number
  ): Promise<ConversationHistoryResponse> {
    const response = await api.get<ConversationHistoryResponse>(
      `/api/v1/projects/${projectId}/ai/conversations/${conversationId}/history`
    );
    return response.data;
  }
}

export const aiService = new AIService();
