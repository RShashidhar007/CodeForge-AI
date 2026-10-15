import { useState, useEffect } from "react";
import { Code, Link2, Unlink, Star } from "lucide-react";
import { githubService } from "../../services/api/githubService";
import { RepositoryImportModal } from "../../components/github/RepositoryImportModal";
import { parseGithubError } from "../../utils/errorHandler";
import { showSuccess, showError } from "../../utils/toast";
import type { GithubRepository } from "../../types/github";

export function GithubIntegrationPage() {
  const [connected, setConnected] = useState(false);
  const [repositories, setRepositories] = useState<GithubRepository[]>([]);
  const [loading, setLoading] = useState(true);
  const [selectedRepo, setSelectedRepo] = useState<GithubRepository | null>(null);

  const checkConnection = async () => {
    setLoading(true);
    try {
      const repos = await githubService.listRepositories();
      setRepositories(repos);
      setConnected(true);
    } catch {
      setConnected(false);
      setRepositories([]);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    checkConnection();

    // Listen for OAuth success/error messages from popup
    const handleMessage = (event: MessageEvent) => {
      if (event.data.type === "github-oauth-success") {
        showSuccess("GitHub connected successfully!");
        checkConnection();
      } else if (event.data.type === "github-oauth-error") {
        showError(event.data.error || "GitHub connection failed");
      }
    };

    window.addEventListener("message", handleMessage);
    return () => window.removeEventListener("message", handleMessage);
  }, []);

  const handleConnect = async () => {
    try {
      const { authorizationUrl } = await githubService.getOAuthUrl();
      window.open(authorizationUrl, "GitHub OAuth", "width=600,height=700");
    } catch (err) {
      showError(parseGithubError(err));
    }
  };

  const handleUnlink = async () => {
    try {
      await githubService.unlinkGithub();
      showSuccess("GitHub account unlinked");
      setConnected(false);
      setRepositories([]);
    } catch (err) {
      showError(parseGithubError(err));
    }
  };

  const handleImportClick = (repo: GithubRepository) => {
    setSelectedRepo(repo);
  };

  const handleCloseModal = () => {
    setSelectedRepo(null);
  };

  if (loading) {
    return (
      <div>
        <h1>GitHub Integration</h1>
        <p>Loading...</p>
      </div>
    );
  }

  return (
    <div>
      <h1>GitHub Integration</h1>
      <p className="subtitle">Connect your GitHub account to import repositories</p>

      <div className="card" style={{ marginBottom: "2rem" }}>
        <div style={{ display: "flex", alignItems: "center", gap: "1rem", marginBottom: "1rem" }}>
          <Code size={32} />
          <div style={{ flex: 1 }}>
            <h2 style={{ margin: 0 }}>GitHub Connection</h2>
            <p style={{ color: "var(--color-muted)", fontSize: "0.9rem", margin: 0 }}>
              {connected ? "Your GitHub account is connected" : "Connect your GitHub account to access repositories"}
            </p>
          </div>
          {connected ? (
            <button className="btn btn-secondary" onClick={handleUnlink} style={{ display: "flex", alignItems: "center", gap: "0.5rem" }}>
              <Unlink size={16} />
              Unlink
            </button>
          ) : (
            <button className="btn btn-primary" onClick={handleConnect} style={{ display: "flex", alignItems: "center", gap: "0.5rem" }}>
              <Link2 size={16} />
              Connect
            </button>
          )}
        </div>
      </div>

      {connected && repositories.length > 0 && (
        <div>
          <h2>Your Repositories</h2>
          <div
            style={{
              display: "grid",
              gridTemplateColumns: "repeat(auto-fill, minmax(300px, 1fr))",
              gap: "1rem",
            }}
          >
            {repositories.map((repo) => (
              <div key={repo.id} className="card">
                <h3 style={{ margin: "0 0 0.5rem 0", fontSize: "1.1rem" }}>{repo.name}</h3>
                {repo.description && (
                  <p style={{ color: "var(--color-muted)", fontSize: "0.9rem", marginBottom: "0.75rem" }}>
                    {repo.description}
                  </p>
                )}
                <div style={{ display: "flex", gap: "1rem", fontSize: "0.85rem", color: "var(--color-muted)", marginBottom: "1rem" }}>
                  {repo.language && <span>{repo.language}</span>}
                  <span style={{ display: "flex", alignItems: "center", gap: "0.25rem" }}>
                    <Star size={14} />
                    {repo.stargazersCount}
                  </span>
                </div>
                <button className="btn btn-primary" onClick={() => handleImportClick(repo)} style={{ width: "100%" }}>
                  Import
                </button>
              </div>
            ))}
          </div>
        </div>
      )}

      {connected && repositories.length === 0 && (
        <div className="alert alert-info">No repositories found in your GitHub account.</div>
      )}

      {selectedRepo && <RepositoryImportModal repository={selectedRepo} onClose={handleCloseModal} />}
    </div>
  );
}
