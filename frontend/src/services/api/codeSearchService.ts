import { apiClient } from "../apiClient";
import type { SemanticSearchRequest, SemanticSearchResponse } from "../../types/github";

export const codeSearchService = {
  semanticSearch(request: SemanticSearchRequest): Promise<SemanticSearchResponse> {
    return apiClient.post("/code/search", request).then((r) => r.data);
  },
};
