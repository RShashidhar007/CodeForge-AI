import { useState, useEffect } from "react";
import { FileCode, Search, ChevronDown, ChevronUp } from "lucide-react";
import type { Project } from "../../types/project";
import type { SearchResult } from "../../types/github";
import { codeSearchService } from "../../services/api/codeSearchService";
import { showError } from "../../utils/toast";
import { parseGithubError } from "../../utils/errorHandler";
import { Spinner } from "../common/Spinner";

interface SemanticSearchPanelProps {
  projects: Project[];
  selectedProjectId: number | null;
  onProjectChange: (id: number) => void;
}

export function SemanticSearchPanel({
  projects,
  selectedProjectId,
  onProjectChange,
}: SemanticSearchPanelProps) {
  const [query, setQuery] = useState("");
  const [debouncedQuery, setDebouncedQuery] = useState("");
  const [results, setResults] = useState<SearchResult[]>([]);
  const [loading, setLoading] = useState(false);
  const [expandedResults, setExpandedResults] = useState<Set<string>>(new Set());

  // Debounce query input
  useEffect(() => {
    const timeout = setTimeout(() => {
      setDebouncedQuery(query);
    }, 300);

    return () => clearTimeout(timeout);
  }, [query]);

  // Trigger search when debounced query or project changes
  useEffect(() => {
    if (!debouncedQuery || !selectedProjectId) {
      setResults([]);
      return;
    }

    let mounted = true;

    const performSearch = async () => {
      setLoading(true);
      try {
        const response = await codeSearchService.semanticSearch({
          projectId: selectedProjectId,
          query: debouncedQuery,
          maxResults: 20,
        });
        if (!mounted) return;
        setResults(response.results);
      } catch (err) {
        if (!mounted) return;
        showError(parseGithubError(err));
        setResults([]);
      } finally {
        if (mounted) {
          setLoading(false);
        }
      }
    };

    performSearch();

    return () => {
      mounted = false;
    };
  }, [debouncedQuery, selectedProjectId]);

  const toggleExpanded = (resultKey: string) => {
    setExpandedResults((prev) => {
      const next = new Set(prev);
      if (next.has(resultKey)) {
        next.delete(resultKey);
      } else {
        next.add(resultKey);
      }
      return next;
    });
  };

  return (
    <div>
      {/* Project Selector */}
      <div className="card">
        <div className="form-group">
          <label htmlFor="project-selector">Project</label>
          <select
            id="project-selector"
            value={selectedProjectId || ""}
            onChange={(e) => onProjectChange(Number(e.target.value))}
            style={{
              width: "100%",
              padding: "0.6rem 0.75rem",
              borderRadius: "8px",
              border: "1px solid var(--color-border)",
              fontSize: "0.92rem",
              fontFamily: "inherit",
            }}
          >
            <option value="">Select a project</option>
            {projects.map((project) => (
              <option key={project.id} value={project.id}>
                {project.name}
              </option>
            ))}
          </select>
        </div>

        {/* Search Input */}
        <div className="form-group" style={{ marginBottom: 0 }}>
          <label htmlFor="search-input">Search Query</label>
          <div style={{ position: "relative" }}>
            <input
              id="search-input"
              type="text"
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              placeholder="Search for code..."
              disabled={!selectedProjectId}
              style={{
                width: "100%",
                padding: "0.6rem 2.5rem 0.6rem 0.75rem",
                borderRadius: "8px",
                border: "1px solid var(--color-border)",
                fontSize: "0.92rem",
                fontFamily: "inherit",
              }}
            />
            <div
              style={{
                position: "absolute",
                right: "0.75rem",
                top: "50%",
                transform: "translateY(-50%)",
                display: "flex",
                alignItems: "center",
                color: "var(--color-muted)",
              }}
            >
              {loading ? <Spinner size={18} /> : <Search size={18} />}
            </div>
          </div>
        </div>
      </div>

      {/* Results */}
      {debouncedQuery && results.length === 0 && !loading && (
        <div className="empty-state">
          <FileCode size={48} style={{ color: "var(--color-muted)", marginBottom: "0.5rem" }} />
          <div>No results found</div>
        </div>
      )}

      {!debouncedQuery && !loading && (
        <div className="empty-state">
          <FileCode size={48} style={{ color: "var(--color-muted)", marginBottom: "0.5rem" }} />
          <div>Enter a search query to find relevant code</div>
        </div>
      )}

      {results.length > 0 && (
        <div>
          {results.map((result, index) => {
            const resultKey = `${result.filePath}-${result.startLine}-${index}`;
            const isExpanded = expandedResults.has(resultKey);
            const scorePercent = Math.round(result.score * 100);
            const scoreColor = scorePercent > 70 ? "#059669" : "#6b7280";

            return (
              <div
                key={resultKey}
                className="card"
                style={{ cursor: "pointer" }}
                onClick={() => toggleExpanded(resultKey)}
              >
                {/* Header Row */}
                <div
                  style={{
                    display: "flex",
                    justifyContent: "space-between",
                    alignItems: "flex-start",
                    gap: "1rem",
                  }}
                >
                  <div style={{ flex: 1, minWidth: 0 }}>
                    <div style={{ display: "flex", alignItems: "center", gap: "0.5rem", marginBottom: "0.25rem" }}>
                      <FileCode size={16} style={{ color: "var(--color-muted)", flexShrink: 0 }} />
                      <span
                        style={{
                          fontFamily: "monospace",
                          fontWeight: 500,
                          fontSize: "0.9rem",
                          overflow: "hidden",
                          textOverflow: "ellipsis",
                          whiteSpace: "nowrap",
                        }}
                      >
                        {result.filePath}
                      </span>
                    </div>
                    <div style={{ fontSize: "0.8rem", color: "var(--color-muted)" }}>
                      Lines {result.startLine}-{result.endLine}
                      {result.language && ` • ${result.language}`}
                    </div>
                  </div>

                  <div style={{ display: "flex", alignItems: "center", gap: "0.5rem", flexShrink: 0 }}>
                    <span
                      style={{
                        fontSize: "0.75rem",
                        fontWeight: 600,
                        padding: "0.2rem 0.5rem",
                        borderRadius: "999px",
                        backgroundColor: scorePercent > 70 ? "#ecfdf5" : "#f3f4f6",
                        color: scoreColor,
                      }}
                    >
                      {scorePercent}%
                    </span>
                    {isExpanded ? <ChevronUp size={18} /> : <ChevronDown size={18} />}
                  </div>
                </div>

                {/* Expanded Code Preview */}
                {isExpanded && (
                  <pre
                    style={{
                      marginTop: "1rem",
                      padding: "0.75rem",
                      background: "#f5f5f5",
                      borderRadius: "6px",
                      fontSize: "0.8rem",
                      fontFamily: "monospace",
                      maxHeight: "300px",
                      overflow: "auto",
                      margin: "1rem 0 0",
                      whiteSpace: "pre-wrap",
                      wordBreak: "break-word",
                    }}
                  >
                    <code>{result.content}</code>
                  </pre>
                )}
              </div>
            );
          })}
        </div>
      )}
    </div>
  );
}
