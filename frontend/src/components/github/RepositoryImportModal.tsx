import { useState, useEffect } from "react";
import { CheckCircle, XCircle, X } from "lucide-react";
import { ProgressBar } from "../common/ProgressBar";
import { githubService } from "../../services/api/githubService";
import { projectService } from "../../services/api/projectService";
import { parseGithubError } from "../../utils/errorHandler";
import { showSuccess, showError } from "../../utils/toast";
import type { GithubRepository, ImportStatusResponse } from "../../types/github";
import type { Project } from "../../types/project";

interface RepositoryImportModalProps {
  repository: GithubRepository;
  onClose: () => void;
}

export function RepositoryImportModal({ repository, onClose }: RepositoryImportModalProps) {
  const [projects, setProjects] = useState<Project[]>([]);
  const [selectedProjectId, setSelectedProjectId] = useState<number | null>(null);
  const [importing, setImporting] = useState(false);
  const [importStatus, setImportStatus] = useState<ImportStatusResponse | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [loadingProjects, setLoadingProjects] = useState(true);

  useEffect(() => {
    projectService
      .listProjects()
      .then((data) => {
        setProjects(data);
        if (data.length > 0) {
          setSelectedProjectId(data[0].id);
        }
      })
      .catch((err) => {
        setError("Failed to load projects: " + (err.message || "Unknown error"));
      })
      .finally(() => setLoadingProjects(false));
  }, []);

  useEffect(() => {
    if (!importing || !selectedProjectId) return;

    let mounted = true;
    const intervalId = setInterval(async () => {
      try {
        const status = await githubService.getImportStatus(selectedProjectId);
        if (!mounted) return;

        setImportStatus(status);

        if (status.status === "COMPLETED") {
          clearInterval(intervalId);
          showSuccess("Import completed successfully!");
          setImporting(false);
        } else if (status.status === "FAILED") {
          clearInterval(intervalId);
          setError(status.error || "Import failed");
          setImporting(false);
        }
      } catch (err) {
        if (!mounted) return;
        clearInterval(intervalId);
        setError(parseGithubError(err));
        setImporting(false);
      }
    }, 2000);

    return () => {
      mounted = false;
      clearInterval(intervalId);
    };
  }, [importing, selectedProjectId]);

  const handleImport = async () => {
    if (!selectedProjectId) {
      showError("Please select a project");
      return;
    }

    setImporting(true);
    setError(null);
    setImportStatus(null);

    try {
      // Extract owner and repo from fullName (e.g., "owner/repo")
      const [owner, repo] = repository.fullName.split("/");
      
      await githubService.importRepository({
        owner,
        repo,
        projectId: selectedProjectId,
      });

      showSuccess("Import started");
    } catch (err) {
      setError(parseGithubError(err));
      setImporting(false);
    }
  };

  const isInProgress = importStatus?.status === "PENDING" || importStatus?.status === "CLONING" || importStatus?.status === "INDEXING";

  return (
    <div
      style={{
        position: "fixed",
        top: 0,
        left: 0,
        right: 0,
        bottom: 0,
        backgroundColor: "rgba(0, 0, 0, 0.5)",
        display: "flex",
        alignItems: "center",
        justifyContent: "center",
        zIndex: 999,
      }}
      onClick={(e) => {
        if (e.target === e.currentTarget && !isInProgress) {
          onClose();
        }
      }}
    >
      <div
        className="card"
        style={{
          width: "95%",
          maxWidth: "600px",
          zIndex: 1000,
          position: "relative",
        }}
      >
        <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: "1rem" }}>
          <h2 style={{ margin: 0 }}>Import Repository</h2>
          <button
            className="btn btn-secondary"
            onClick={onClose}
            disabled={isInProgress}
            style={{ padding: "0.25rem 0.5rem" }}
          >
            <X size={20} />
          </button>
        </div>

        <div style={{ marginBottom: "1rem" }}>
          <strong>{repository.fullName}</strong>
          {repository.description && <p style={{ color: "var(--color-muted)", marginTop: "0.5rem" }}>{repository.description}</p>}
        </div>

        {loadingProjects ? (
          <p>Loading projects...</p>
        ) : projects.length === 0 ? (
          <div className="alert alert-warning">
            No projects available. Please create a project first.
          </div>
        ) : (
          <div style={{ marginBottom: "1rem" }}>
            <label htmlFor="project-select" style={{ display: "block", marginBottom: "0.5rem" }}>
              Select Project:
            </label>
            <select
              id="project-select"
              className="form-control"
              value={selectedProjectId || ""}
              onChange={(e) => setSelectedProjectId(Number(e.target.value))}
              disabled={importing}
              style={{
                width: "100%",
                padding: "0.5rem",
                borderRadius: "4px",
                border: "1px solid var(--color-border)",
                backgroundColor: "var(--color-bg)",
                color: "var(--color-text)",
              }}
            >
              {projects.map((project) => (
                <option key={project.id} value={project.id}>
                  {project.name}
                </option>
              ))}
            </select>
          </div>
        )}

        {error && (
          <div className="alert alert-error" style={{ marginBottom: "1rem", display: "flex", alignItems: "center", gap: "0.5rem" }}>
            <XCircle size={20} />
            {error}
          </div>
        )}

        {importStatus && (
          <div style={{ marginBottom: "1rem" }}>
            {importStatus.status === "COMPLETED" ? (
              <div className="alert alert-success" style={{ display: "flex", alignItems: "center", gap: "0.5rem" }}>
                <CheckCircle size={20} />
                Import complete!
              </div>
            ) : isInProgress ? (
              <div>
                <p style={{ marginBottom: "0.5rem", fontSize: "0.9rem" }}>
                  Status: {importStatus.status}
                  {importStatus.currentStep && ` - ${importStatus.currentStep}`}
                </p>
                <ProgressBar percentage={importStatus.progressPercentage} showLabel />
              </div>
            ) : null}
          </div>
        )}

        {!importing && !importStatus && projects.length > 0 && (
          <button className="btn btn-primary" onClick={handleImport} style={{ width: "100%" }}>
            Import
          </button>
        )}
      </div>
    </div>
  );
}
