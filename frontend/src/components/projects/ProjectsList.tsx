import { ExternalLink } from "lucide-react";
import type { Project } from "../../types/project";
import { SkeletonCard } from "../common/SkeletonCard";

interface ProjectsListProps {
  projects: Project[];
  loading?: boolean;
  onSelect?: (project: Project) => void;
  selectedId?: number;
}

export function ProjectsList({ projects, loading, onSelect, selectedId }: ProjectsListProps) {
  if (loading) {
    return <SkeletonCard count={3} />;
  }

  if (projects.length === 0) {
    return (
      <div className="empty-state">
        <p>No projects found. Import a repository from GitHub to get started.</p>
      </div>
    );
  }

  const formatDate = (dateString: string): string => {
    const date = new Date(dateString);
    return date.toLocaleDateString(undefined, {
      year: "numeric",
      month: "short",
      day: "numeric",
    });
  };

  return (
    <div>
      {projects.map((project) => (
        <div
          key={project.id}
          className="card"
          onClick={() => onSelect?.(project)}
          style={{
            cursor: onSelect ? "pointer" : "default",
            borderColor: selectedId === project.id ? "var(--color-primary)" : "var(--color-border)",
            borderWidth: selectedId === project.id ? "2px" : "1px",
          }}
        >
          <div>
            <h3 style={{ margin: "0 0 0.5rem", fontWeight: 700 }}>
              {project.name}
            </h3>
            {project.description && (
              <p style={{ margin: "0 0 0.5rem", color: "var(--color-muted)", fontSize: "0.9rem" }}>
                {project.description}
              </p>
            )}
            {project.repositoryUrl && (
              <a
                href={project.repositoryUrl}
                target="_blank"
                rel="noopener noreferrer"
                style={{
                  display: "inline-flex",
                  alignItems: "center",
                  gap: "0.3rem",
                  fontSize: "0.85rem",
                  marginBottom: "0.5rem",
                }}
                onClick={(e) => e.stopPropagation()}
              >
                <ExternalLink size={14} />
                {project.repositoryUrl}
              </a>
            )}
            <div style={{ fontSize: "0.8rem", color: "var(--color-muted)" }}>
              Updated {formatDate(project.updatedAt)}
            </div>
          </div>
        </div>
      ))}
    </div>
  );
}
