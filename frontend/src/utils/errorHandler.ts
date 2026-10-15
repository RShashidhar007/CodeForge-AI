import axios from "axios";

/**
 * Parses GitHub-specific errors and returns user-friendly messages.
 * Handles common GitHub API error status codes.
 */
export function parseGithubError(error: unknown): string {
  if (axios.isAxiosError(error)) {
    if (!error.response) {
      return "Network error: could not reach GitHub API. Please check your connection.";
    }

    const status = error.response.status;
    const data = error.response.data;

    switch (status) {
      case 401:
        return "GitHub authentication failed. Please reconnect your GitHub account.";
      case 403: {
        // Check for rate limit
        const rateLimitRemaining = error.response.headers["x-ratelimit-remaining"];
        if (rateLimitRemaining === "0") {
          const resetTime = error.response.headers["x-ratelimit-reset"];
          if (resetTime) {
            const resetDate = new Date(parseInt(resetTime) * 1000);
            return `GitHub API rate limit exceeded. Try again after ${resetDate.toLocaleTimeString()}.`;
          }
          return "GitHub API rate limit exceeded. Please try again later.";
        }
        return "Access forbidden. You may not have permission to access this GitHub resource.";
      }
      case 404:
        return "GitHub resource not found. The repository or resource may have been deleted or you may not have access.";
      case 429:
        return "Too many requests to GitHub. Please wait a moment and try again.";
      case 502:
        return "GitHub API is temporarily unavailable. Please try again in a few moments.";
      default:
        if (data?.message) {
          return data.message;
        }
        return `GitHub API error (${status}). Please try again.`;
    }
  }

  return "An unexpected error occurred while communicating with GitHub.";
}
