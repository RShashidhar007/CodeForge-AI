# Phase 4 Implementation Plan: Frontend GitHub Integration & Semantic Code Search

## Overview
Phase 4 completes the CodeForge AI frontend by integrating GitHub OAuth, repository import with real-time progress tracking, semantic code search, and enhanced AI chat features. This phase connects the React frontend to all backend APIs from Phase 3 (GitHub OAuth, Qdrant vector search).

## Project Context
- **Frontend**: React 19 + TypeScript 6 + Vite 8 + axios + react-router-dom + lucide-react
- **Styling**: CSS modules with existing App.css patterns (--color-primary, .btn, .card, etc.)
- **API Client**: Centralized axios instance at src/services/apiClient.ts with JWT injection and snake_case→camelCase transformation
- **Backend API Base**: /api (GitHub at /github/*, code search at /code/search, AI at /v1/projects/{id}/ai)
- **No react-query**: Use plain axios + useState/useEffect hooks (matches existing AIPage.tsx pattern)
- **Auth**: useAuth() hook from AuthContext.tsx provides user (id, name, email, role, enabled)

## Build & Test Commands
- **Install deps**: `cd frontend && npm install`
- **Dev server**: `cd frontend && npm run dev` (http://localhost:5173)
- **Build**: `cd frontend && npm run build`
- **Lint**: `cd frontend && npm run lint`

---

## Implementation Steps

- [ ] 1. **Create src/types/github.ts with all GitHub types**
      
      Define TypeScript interfaces for GitHub integration: GithubOAuthUrlResponse (authorizationUrl, state), GithubRepository (name, fullName, description, isPrivate, url, language, stars, updatedAt), ImportRepositoryRequest (projectId, owner, repo), ImportStatus (projectId, status, currentStep, totalFiles, relevantFiles, processedFiles, totalChunks, embeddedChunks, error, startTime, endTime, progressPercentage), SemanticSearchRequest (query, projectId, limit), SearchResult (chunkId, filePath, startLine, endLine, symbol, score, content), SemanticSearchResponse (results: SearchResult[], totalResults).
      
      **Files**: 
      - d:\projects\CodeForge-AI-main\frontend\src\types\github.ts (new)
      
      **Details**:
      ```typescript
      export interface GithubOAuthUrlResponse {
        authorizationUrl: string;
        state: string;
      }
      
      export interface GithubRepository {
        name: string;
        fullName: string;
        description: string;
        isPrivate: boolean;
        url: string;
        language: string;
        stars: number;
        updatedAt?: string;
      }
      
      export interface ImportRepositoryRequest {
        projectId: number;
        owner: string;
        repo: string;
      }
      
      export interface ImportStatus {
        projectId: number;
        status: 'PENDING' | 'IN_PROGRESS' | 'COMPLETED' | 'FAILED';
        currentStep: string;
        totalFiles: number;
        relevantFiles: number;
        processedFiles: number;
        totalChunks: number;
        embeddedChunks: number;
        error?: string;
        startTime?: string;
        endTime?: string;
        progressPercentage: number;
      }
      
      export interface SemanticSearchRequest {
        query: string;
        projectId: number;
        limit?: number;
      }
      
      export interface SearchResult {
        chunkId: number;
        filePath: string;
        startLine: number;
        endLine: number;
        symbol?: string;
        score: number;
        content: string;
      }
      
      export interface SemanticSearchResponse {
        results: SearchResult[];
        totalResults: number;
      }
      ```
      
      **Dependencies**: None (first task)
      
      **Pitfalls**: Backend returns snake_case but apiClient transforms to camelCase — types are camelCase.
      
      **Verify**: `npm run build` — TypeScript compiles without errors

- [ ] 2. **Create src/services/api/githubService.ts**
      
      Create service with methods: getOAuthUrl() GET /github/oauth/authorize returns GithubOAuthUrlResponse, handleOAuthCallback(code, state) POST /github/oauth/callback with {code, state} returns {message, username}, listRepositories() GET /github/repositories returns GithubRepository[], importRepository(request) POST /github/import with ImportRepositoryRequest returns {message, projectId} (202 Accepted), getImportStatus(projectId) GET /github/import/{projectId}/status returns ImportStatus, unlinkGithub() DELETE /github/tokens returns {message}. All use apiClient from ../apiClient.
      
      **Files**: 
      - d:\projects\CodeForge-AI-main\frontend\src\services\api\githubService.ts (new)
      
      **Details**:
      ```typescript
      import { apiClient } from '../apiClient';
      import type { 
        GithubOAuthUrlResponse, 
        GithubRepository, 
        ImportRepositoryRequest, 
        ImportStatus 
      } from '../../types/github';
      
      export const githubService = {
        getOAuthUrl: () =>
          apiClient.get<GithubOAuthUrlResponse>('/github/oauth/authorize').then(r => r.data),
        
        handleOAuthCallback: (code: string, state: string) =>
          apiClient.post<{ message: string; username: string }>('/github/oauth/callback', { code, state }).then(r => r.data),
        
        listRepositories: () =>
          apiClient.get<GithubRepository[]>('/github/repositories').then(r => r.data),
        
        importRepository: (request: ImportRepositoryRequest) =>
          apiClient.post<{ message: string; projectId: string }>('/github/import', request).then(r => r.data),
        
        getImportStatus: (projectId: number) =>
          apiClient.get<ImportStatus>(`/github/import/${projectId}/status`).then(r => r.data),
        
        unlinkGithub: () =>
          apiClient.delete<{ message: string }>('/github/tokens').then(r => r.data),
      };
      ```
      
      **Dependencies**: Task 1 (types/github.ts), existing apiClient
      
      **Pitfalls**: importRepository returns 202 Accepted (not 200), ensure axios doesn't reject.
      
      **Verify**: `npm run build` — compiles without errors

- [ ] 3. **Create src/services/api/codeSearchService.ts**
      
      Create service with single method: semanticSearch(request) POST /code/search with SemanticSearchRequest returns SemanticSearchResponse. Use apiClient pattern.
      
      **Files**: 
      - d:\projects\CodeForge-AI-main\frontend\src\services\api\codeSearchService.ts (new)
      
      **Details**:
      ```typescript
      import { apiClient } from '../apiClient';
      import type { SemanticSearchRequest, SemanticSearchResponse } from '../../types/github';
      
      export const codeSearchService = {
        semanticSearch: (request: SemanticSearchRequest) =>
          apiClient.post<SemanticSearchResponse>('/code/search', request).then(r => r.data),
      };
      ```
      
      **Dependencies**: Task 1 (types/github.ts), existing apiClient
      
      **Verify**: `npm run build` — compiles without errors

- [ ] 4. **Create/update src/types/project.ts with Project interface**
      
      Define Project interface matching backend entity: id (number), name (string), description (string), repositoryUrl (string), createdAt (string), updatedAt (string). This is used by AI page project selector and GitHub import modal.
      
      **Files**: 
      - d:\projects\CodeForge-AI-main\frontend\src\types\project.ts (new)
      
      **Details**:
      ```typescript
      export interface Project {
        id: number;
        name: string;
        description: string;
        repositoryUrl: string;
        createdAt: string;
        updatedAt: string;
      }
      ```
      
      **Dependencies**: None
      
      **Pitfalls**: Backend has Company relation but frontend doesn't need it for now — keep simple.
      
      **Verify**: `npm run build` — compiles without errors

- [ ] 5. **Create src/utils/errorHandler.ts for GitHub-specific error parsing**
      
      Create parseGithubError(error: unknown): string function that handles GitHub-specific errors (rate limit 429, invalid token 401, repo not found 404, import failed 500) and returns user-friendly messages. Use axios.isAxiosError for type checking. Complement existing extractErrorMessage from apiClient.ts.
      
      **Files**: 
      - d:\projects\CodeForge-AI-main\frontend\src\utils\errorHandler.ts (new)
      
      **Details**:
      ```typescript
      import axios from 'axios';
      
      export function parseGithubError(error: unknown): string {
        if (axios.isAxiosError(error)) {
          if (!error.response) {
            return 'Network error: could not reach GitHub API. Please check your connection.';
          }
          
          const status = error.response.status;
          const message = error.response.data?.message || '';
          
          switch (status) {
            case 401:
              return 'GitHub authentication failed. Please reconnect your GitHub account.';
            case 403:
              if (message.toLowerCase().includes('rate limit')) {
                return 'GitHub API rate limit exceeded. Please try again later.';
              }
              return 'Access forbidden. Check repository permissions.';
            case 404:
              return 'Repository not found or access denied.';
            case 429:
              return 'Too many requests. Please wait a moment and try again.';
            case 502:
              return 'GitHub API is temporarily unavailable. Please try again.';
            default:
              return message || 'An error occurred with GitHub integration.';
          }
        }
        return 'An unexpected error occurred.';
      }
      ```
      
      **Dependencies**: None (uses axios already in project)
      
      **Verify**: `npm run build` — compiles without errors

- [ ] 6. **Install react-toastify and create src/utils/toast.ts**
      
      Install react-toastify@10.0.6 (exact version) via npm. Create toast.ts wrapper with showSuccess, showError, showInfo functions using toast from react-toastify. Configure default position top-right, autoClose 4000ms. Import CSS in App.tsx.
      
      **Files**: 
      - d:\projects\CodeForge-AI-main\frontend\package.json (modify: add dependency)
      - d:\projects\CodeForge-AI-main\frontend\src\utils\toast.ts (new)
      - d:\projects\CodeForge-AI-main\frontend\src\App.tsx (modify: add import 'react-toastify/dist/ReactToastify.css')
      
      **Details**:
      ```bash
      cd frontend && npm install --save-exact react-toastify@10.0.6
      ```
      
      toast.ts:
      ```typescript
      import { toast, ToastOptions } from 'react-toastify';
      
      const defaultOptions: ToastOptions = {
        position: 'top-right',
        autoClose: 4000,
        hideProgressBar: false,
        closeOnClick: true,
        pauseOnHover: true,
        draggable: true,
      };
      
      export const showSuccess = (message: string) => {
        toast.success(message, defaultOptions);
      };
      
      export const showError = (message: string) => {
        toast.error(message, defaultOptions);
      };
      
      export const showInfo = (message: string) => {
        toast.info(message, defaultOptions);
      };
      ```
      
      Add to App.tsx (after other imports):
      ```typescript
      import 'react-toastify/dist/ReactToastify.css';
      import { ToastContainer } from 'react-toastify';
      ```
      
      Add before closing BrowserRouter tag:
      ```typescript
      <ToastContainer />
      ```
      
      **Dependencies**: None (package install)
      
      **Pitfalls**: Must import CSS in App.tsx or toasts won't style. ToastContainer must be inside BrowserRouter.
      
      **Verify**: `npm run build` — builds successfully, dev server shows no console errors

- [ ] 7. **Create src/components/common/Spinner.tsx, ProgressBar.tsx, LoadingOverlay.tsx**
      
      Create three reusable loading primitives following existing CSS patterns: Spinner (inline spinner with lucide-react Loader icon, spinning animation), ProgressBar (takes percentage prop, shows filled bar using --color-primary), LoadingOverlay (full-screen overlay with centered spinner and optional message, uses position: fixed, z-index: 1000).
      
      **Files**: 
      - d:\projects\CodeForge-AI-main\frontend\src\components\common\Spinner.tsx (new)
      - d:\projects\CodeForge-AI-main\frontend\src\components\common\ProgressBar.tsx (new)
      - d:\projects\CodeForge-AI-main\frontend\src\components\common\LoadingOverlay.tsx (new)
      
      **Details**:
      
      Spinner.tsx:
      ```typescript
      import { Loader } from 'lucide-react';
      
      export function Spinner({ size = 24 }: { size?: number }) {
        return (
          <Loader
            size={size}
            className="spinner"
            style={{ animation: 'spin 1s linear infinite' }}
          />
        );
      }
      ```
      
      ProgressBar.tsx:
      ```typescript
      interface ProgressBarProps {
        percentage: number;
        height?: string;
        showLabel?: boolean;
      }
      
      export function ProgressBar({ percentage, height = '8px', showLabel = false }: ProgressBarProps) {
        const clampedPercentage = Math.min(100, Math.max(0, percentage));
        
        return (
          <div>
            <div
              style={{
                width: '100%',
                height,
                backgroundColor: 'var(--color-border)',
                borderRadius: '4px',
                overflow: 'hidden',
              }}
            >
              <div
                style={{
                  width: `${clampedPercentage}%`,
                  height: '100%',
                  backgroundColor: 'var(--color-primary)',
                  transition: 'width 0.3s ease',
                }}
              />
            </div>
            {showLabel && (
              <div style={{ fontSize: '0.75rem', color: 'var(--color-muted)', marginTop: '4px' }}>
                {clampedPercentage}%
              </div>
            )}
          </div>
        );
      }
      ```
      
      LoadingOverlay.tsx:
      ```typescript
      import { Spinner } from './Spinner';
      
      interface LoadingOverlayProps {
        message?: string;
      }
      
      export function LoadingOverlay({ message }: LoadingOverlayProps) {
        return (
          <div
            style={{
              position: 'fixed',
              top: 0,
              left: 0,
              right: 0,
              bottom: 0,
              backgroundColor: 'rgba(0, 0, 0, 0.5)',
              display: 'flex',
              flexDirection: 'column',
              alignItems: 'center',
              justifyContent: 'center',
              gap: '1rem',
              zIndex: 1000,
            }}
          >
            <Spinner size={48} />
            {message && (
              <p style={{ color: 'white', fontSize: '1rem', margin: 0 }}>{message}</p>
            )}
          </div>
        );
      }
      ```
      
      **Dependencies**: lucide-react already installed
      
      **Pitfalls**: Add @keyframes spin to App.css if not already present.
      
      **Verify**: `npm run build` — compiles without errors

- [ ] 8. **Create src/components/common/SkeletonCard.tsx**
      
      Create skeleton loader component for lists (repo list, search results, import status). Animated gray boxes that shimmer. Use CSS animation with linear gradient. Matches card styling from App.css (.card class).
      
      **Files**: 
      - d:\projects\CodeForge-AI-main\frontend\src\components\common\SkeletonCard.tsx (new)
      
      **Details**:
      ```typescript
      interface SkeletonCardProps {
        count?: number;
      }
      
      export function SkeletonCard({ count = 3 }: SkeletonCardProps) {
        return (
          <>
            {Array.from({ length: count }).map((_, i) => (
              <div
                key={i}
                className="card"
                style={{
                  background: 'linear-gradient(90deg, #f0f0f0 25%, #e0e0e0 50%, #f0f0f0 75%)',
                  backgroundSize: '200% 100%',
                  animation: 'shimmer 1.5s infinite',
                  height: '120px',
                }}
              >
                <div style={{ height: '1rem', width: '60%', backgroundColor: '#d0d0d0', borderRadius: '4px', marginBottom: '0.5rem' }} />
                <div style={{ height: '0.75rem', width: '40%', backgroundColor: '#e0e0e0', borderRadius: '4px', marginBottom: '0.5rem' }} />
                <div style={{ height: '0.75rem', width: '80%', backgroundColor: '#e0e0e0', borderRadius: '4px' }} />
              </div>
            ))}
          </>
        );
      }
      ```
      
      Add to App.css (if shimmer animation doesn't exist):
      ```css
      @keyframes shimmer {
        0% {
          background-position: 200% 0;
        }
        100% {
          background-position: -200% 0;
        }
      }
      ```
      
      **Dependencies**: App.css
      
      **Verify**: `npm run build` — compiles without errors

- [ ] 9. **Create src/components/projects/ProjectsList.tsx**
      
      Shared component that lists projects with name, repo URL (if present), last updated date. Used in AI page project selector and GitHub import modal. Takes projects: Project[] prop and onSelect: (project: Project) => void callback. Uses card styling, shows empty state if no projects. Maps through projects, displays name as bold, repositoryUrl as link (if present), updatedAt formatted with new Date().toLocaleDateString(). Click calls onSelect.
      
      **Files**: 
      - d:\projects\CodeForge-AI-main\frontend\src\components\projects\ProjectsList.tsx (new)
      
      **Details**:
      ```typescript
      import { Project } from '../../types/project';
      import { SkeletonCard } from '../common/SkeletonCard';
      
      interface ProjectsListProps {
        projects: Project[];
        loading?: boolean;
        onSelect: (project: Project) => void;
        selectedId?: number;
      }
      
      export function ProjectsList({ projects, loading, onSelect, selectedId }: ProjectsListProps) {
        if (loading) {
          return <SkeletonCard count={3} />;
        }
        
        if (projects.length === 0) {
          return (
            <div className="empty-state">
              <p>No projects found. Create a project to get started.</p>
            </div>
          );
        }
        
        return (
          <div style={{ display: 'flex', flexDirection: 'column', gap: '0.75rem' }}>
            {projects.map((project) => (
              <button
                key={project.id}
                className="card"
                onClick={() => onSelect(project)}
                style={{
                  cursor: 'pointer',
                  border: selectedId === project.id ? '2px solid var(--color-primary)' : undefined,
                  textAlign: 'left',
                  padding: '1rem',
                }}
              >
                <h3 style={{ margin: '0 0 0.5rem', fontSize: '1rem' }}>{project.name}</h3>
                {project.repositoryUrl && (
                  <p style={{ margin: '0 0 0.25rem', fontSize: '0.85rem', color: 'var(--color-muted)' }}>
                    {project.repositoryUrl}
                  </p>
                )}
                <p style={{ margin: 0, fontSize: '0.75rem', color: 'var(--color-muted)' }}>
                  Updated: {new Date(project.updatedAt).toLocaleDateString()}
                </p>
              </button>
            ))}
          </div>
        );
      }
      ```
      
      **Dependencies**: Task 4 (types/project.ts), Task 8 (SkeletonCard)
      
      **Pitfalls**: Projects endpoint doesn't exist yet in backend — this component will be used when it does. For now, can pass empty array or mock data.
      
      **Verify**: `npm run build` — compiles without errors

- [ ] 10. **Create src/components/github/RepositoryImportModal.tsx**
      
      Modal component for repository import flow. Takes isOpen, onClose, repository (GithubRepository), projects (Project[]). Shows project selector (dropdown or ProjectsList), Import button, real-time progress bar that polls getImportStatus every 2s once import starts. Success shows checkmark and "Import complete" message. Error shows alert with error message. Uses useEffect cleanup to cancel polling on unmount. Modal backdrop is position: fixed with z-index: 999, content is centered card with z-index: 1000.
      
      **Files**: 
      - d:\projects\CodeForge-AI-main\frontend\src\components\github\RepositoryImportModal.tsx (new)
      
      **Details**:
      ```typescript
      import { useState, useEffect } from 'react';
      import { CheckCircle, XCircle, Loader } from 'lucide-react';
      import { githubService } from '../../services/api/githubService';
      import { GithubRepository, ImportStatus } from '../../types/github';
      import { Project } from '../../types/project';
      import { ProgressBar } from '../common/ProgressBar';
      import { parseGithubError } from '../../utils/errorHandler';
      import { showSuccess, showError } from '../../utils/toast';
      
      interface RepositoryImportModalProps {
        isOpen: boolean;
        onClose: () => void;
        repository: GithubRepository;
        projects: Project[];
      }
      
      export function RepositoryImportModal({ isOpen, onClose, repository, projects }: RepositoryImportModalProps) {
        const [selectedProjectId, setSelectedProjectId] = useState<number | null>(null);
        const [importing, setImporting] = useState(false);
        const [status, setStatus] = useState<ImportStatus | null>(null);
        const [error, setError] = useState<string | null>(null);
        
        useEffect(() => {
          if (!isOpen || !status || status.status === 'COMPLETED' || status.status === 'FAILED') {
            return;
          }
          
          const intervalId = setInterval(async () => {
            try {
              const newStatus = await githubService.getImportStatus(status.projectId);
              setStatus(newStatus);
              
              if (newStatus.status === 'COMPLETED') {
                showSuccess('Repository imported successfully!');
                setImporting(false);
              } else if (newStatus.status === 'FAILED') {
                setError(newStatus.error || 'Import failed');
                showError('Repository import failed');
                setImporting(false);
              }
            } catch (err) {
              setError(parseGithubError(err));
              setImporting(false);
            }
          }, 2000);
          
          return () => clearInterval(intervalId);
        }, [isOpen, status]);
        
        const handleImport = async () => {
          if (!selectedProjectId) {
            showError('Please select a project');
            return;
          }
          
          const [owner, repo] = repository.fullName.split('/');
          
          setImporting(true);
          setError(null);
          
          try {
            await githubService.importRepository({ projectId: selectedProjectId, owner, repo });
            
            // Start polling for status
            const initialStatus = await githubService.getImportStatus(selectedProjectId);
            setStatus(initialStatus);
            showInfo('Repository import started');
          } catch (err) {
            setError(parseGithubError(err));
            showError('Failed to start import');
            setImporting(false);
          }
        };
        
        const handleClose = () => {
          if (!importing) {
            setStatus(null);
            setError(null);
            setSelectedProjectId(null);
            onClose();
          }
        };
        
        if (!isOpen) return null;
        
        return (
          <div
            style={{
              position: 'fixed',
              top: 0,
              left: 0,
              right: 0,
              bottom: 0,
              backgroundColor: 'rgba(0, 0, 0, 0.5)',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              zIndex: 999,
            }}
            onClick={handleClose}
          >
            <div
              className="card"
              style={{
                width: '90%',
                maxWidth: '500px',
                zIndex: 1000,
                maxHeight: '80vh',
                overflow: 'auto',
              }}
              onClick={(e) => e.stopPropagation()}
            >
              <h2 style={{ marginTop: 0 }}>Import Repository</h2>
              
              <div style={{ marginBottom: '1rem' }}>
                <strong>{repository.fullName}</strong>
                <p style={{ color: 'var(--color-muted)', fontSize: '0.85rem', margin: '0.25rem 0' }}>
                  {repository.description || 'No description'}
                </p>
              </div>
              
              {!status && (
                <div className="form-group">
                  <label>Select Project</label>
                  <select
                    value={selectedProjectId || ''}
                    onChange={(e) => setSelectedProjectId(Number(e.target.value))}
                    disabled={importing}
                    style={{
                      width: '100%',
                      padding: '0.6rem',
                      borderRadius: '8px',
                      border: '1px solid var(--color-border)',
                    }}
                  >
                    <option value="">-- Choose a project --</option>
                    {projects.map((p) => (
                      <option key={p.id} value={p.id}>
                        {p.name}
                      </option>
                    ))}
                  </select>
                </div>
              )}
              
              {status && (
                <div style={{ marginBottom: '1rem' }}>
                  <p style={{ fontSize: '0.9rem', marginBottom: '0.5rem' }}>
                    <strong>Status:</strong> {status.currentStep}
                  </p>
                  <ProgressBar percentage={status.progressPercentage} showLabel />
                  <div style={{ fontSize: '0.75rem', color: 'var(--color-muted)', marginTop: '0.5rem' }}>
                    {status.processedFiles} / {status.relevantFiles} files processed · {status.embeddedChunks} chunks embedded
                  </div>
                </div>
              )}
              
              {status?.status === 'COMPLETED' && (
                <div className="alert alert-success" style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                  <CheckCircle size={20} />
                  Import completed successfully!
                </div>
              )}
              
              {error && (
                <div className="alert alert-error" style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                  <XCircle size={20} />
                  {error}
                </div>
              )}
              
              <div style={{ display: 'flex', gap: '0.75rem', marginTop: '1.5rem' }}>
                {!status && (
                  <button
                    className="btn btn-primary"
                    onClick={handleImport}
                    disabled={importing || !selectedProjectId}
                  >
                    {importing && <Loader size={16} className="spinner" />}
                    Import
                  </button>
                )}
                <button
                  className="btn btn-secondary"
                  onClick={handleClose}
                  disabled={importing && status?.status === 'IN_PROGRESS'}
                >
                  {status?.status === 'COMPLETED' || status?.status === 'FAILED' ? 'Done' : 'Cancel'}
                </button>
              </div>
            </div>
          </div>
        );
      }
      ```
      
      **Dependencies**: Tasks 1,2,4,5,6,7 (types, services, utils)
      
      **Pitfalls**: Poll interval must be cleared on unmount or modal close. Don't allow close while import in progress (status IN_PROGRESS).
      
      **Verify**: `npm run build` — compiles without errors

- [ ] 11. **Create src/pages/github/GithubIntegrationPage.tsx**
      
      Page showing GitHub connection status, Connect button (opens OAuth popup via window.open), repo list (from listRepositories), Import button per repo (opens RepositoryImportModal), Unlink button. Uses useState for repos and loading. OAuth flow: onClick calls getOAuthUrl, opens window.open(authorizationUrl, 'GitHub', 'width=600,height=700'), listens for message event from callback page with success/error. Protected route for CANDIDATE and RECRUITER roles. Add CSS for responsive grid (repos displayed as cards, 1 column mobile, 2 columns tablet, 3 columns desktop).
      
      **Files**: 
      - d:\projects\CodeForge-AI-main\frontend\src\pages\github\GithubIntegrationPage.tsx (new)
      
      **Details**:
      ```typescript
      import { useState, useEffect } from 'react';
      import { Github, Link as LinkIcon, Loader } from 'lucide-react';
      import { githubService } from '../../services/api/githubService';
      import { GithubRepository } from '../../types/github';
      import { Project } from '../../types/project';
      import { RepositoryImportModal } from '../../components/github/RepositoryImportModal';
      import { SkeletonCard } from '../../components/common/SkeletonCard';
      import { parseGithubError } from '../../utils/errorHandler';
      import { showSuccess, showError } from '../../utils/toast';
      
      export function GithubIntegrationPage() {
        const [connected, setConnected] = useState(false);
        const [connecting, setConnecting] = useState(false);
        const [repos, setRepos] = useState<GithubRepository[]>([]);
        const [loading, setLoading] = useState(false);
        const [selectedRepo, setSelectedRepo] = useState<GithubRepository | null>(null);
        const [projects, setProjects] = useState<Project[]>([]);
        const [modalOpen, setModalOpen] = useState(false);
        
        useEffect(() => {
          checkConnection();
        }, []);
        
        const checkConnection = async () => {
          try {
            setLoading(true);
            const repoList = await githubService.listRepositories();
            setRepos(repoList);
            setConnected(true);
          } catch (err) {
            // Not connected or token expired
            setConnected(false);
          } finally {
            setLoading(false);
          }
        };
        
        const handleConnect = async () => {
          try {
            setConnecting(true);
            const { authorizationUrl, state } = await githubService.getOAuthUrl();
            
            // Open OAuth popup
            const popup = window.open(authorizationUrl, 'GitHub OAuth', 'width=600,height=700');
            
            // Listen for callback message
            const handleMessage = (event: MessageEvent) => {
              if (event.data.type === 'github-oauth-success') {
                showSuccess('GitHub account connected successfully!');
                setConnected(true);
                checkConnection();
                window.removeEventListener('message', handleMessage);
              } else if (event.data.type === 'github-oauth-error') {
                showError(event.data.error || 'Failed to connect GitHub account');
              }
              setConnecting(false);
            };
            
            window.addEventListener('message', handleMessage);
            
            // Cleanup if popup closed without message
            const checkClosed = setInterval(() => {
              if (popup?.closed) {
                clearInterval(checkClosed);
                window.removeEventListener('message', handleMessage);
                setConnecting(false);
              }
            }, 500);
          } catch (err) {
            showError(parseGithubError(err));
            setConnecting(false);
          }
        };
        
        const handleUnlink = async () => {
          if (!confirm('Are you sure you want to unlink your GitHub account?')) {
            return;
          }
          
          try {
            await githubService.unlinkGithub();
            setConnected(false);
            setRepos([]);
            showSuccess('GitHub account unlinked');
          } catch (err) {
            showError(parseGithubError(err));
          }
        };
        
        const openImportModal = (repo: GithubRepository) => {
          setSelectedRepo(repo);
          setModalOpen(true);
        };
        
        return (
          <div className="page-container">
            <div className="card">
              <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '1rem' }}>
                <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem' }}>
                  <Github size={32} />
                  <div>
                    <h1 style={{ margin: 0 }}>GitHub Integration</h1>
                    <p style={{ margin: '0.25rem 0 0', fontSize: '0.9rem', color: 'var(--color-muted)' }}>
                      {connected ? 'Connected' : 'Connect your GitHub account to import repositories'}
                    </p>
                  </div>
                </div>
                
                {connected ? (
                  <button className="btn btn-secondary" onClick={handleUnlink}>
                    Unlink
                  </button>
                ) : (
                  <button
                    className="btn btn-primary"
                    onClick={handleConnect}
                    disabled={connecting}
                  >
                    {connecting ? <Loader size={16} className="spinner" /> : <LinkIcon size={16} />}
                    Connect GitHub
                  </button>
                )}
              </div>
            </div>
            
            {connected && (
              <div>
                <h2 style={{ marginBottom: '1rem' }}>Your Repositories</h2>
                
                {loading ? (
                  <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(300px, 1fr))', gap: '1rem' }}>
                    <SkeletonCard count={6} />
                  </div>
                ) : repos.length === 0 ? (
                  <div className="empty-state">
                    <p>No repositories found</p>
                  </div>
                ) : (
                  <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(300px, 1fr))', gap: '1rem' }}>
                    {repos.map((repo) => (
                      <div key={repo.fullName} className="card">
                        <h3 style={{ margin: '0 0 0.5rem', fontSize: '1rem' }}>{repo.name}</h3>
                        <p style={{ fontSize: '0.85rem', color: 'var(--color-muted)', margin: '0 0 0.75rem' }}>
                          {repo.description || 'No description'}
                        </p>
                        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', fontSize: '0.75rem' }}>
                          <div style={{ display: 'flex', gap: '1rem', color: 'var(--color-muted)' }}>
                            <span>{repo.language}</span>
                            <span>⭐ {repo.stars}</span>
                          </div>
                          <button
                            className="btn btn-primary"
                            style={{ padding: '0.4rem 0.8rem', fontSize: '0.85rem' }}
                            onClick={() => openImportModal(repo)}
                          >
                            Import
                          </button>
                        </div>
                      </div>
                    ))}
                  </div>
                )}
              </div>
            )}
            
            {selectedRepo && (
              <RepositoryImportModal
                isOpen={modalOpen}
                onClose={() => {
                  setModalOpen(false);
                  setSelectedRepo(null);
                }}
                repository={selectedRepo}
                projects={projects}
              />
            )}
          </div>
        );
      }
      ```
      
      **Dependencies**: Tasks 1,2,5,6,8,10 (types, services, utils, components)
      
      **Pitfalls**: OAuth popup must be same-origin for postMessage to work. Window.open may be blocked by popup blockers — handle gracefully.
      
      **Verify**: `npm run dev` — page renders, no console errors (API calls will fail until backend running)

- [ ] 12. **Create src/pages/github/GithubCallbackPage.tsx**
      
      OAuth callback page that reads ?code and ?state from URL query params, calls handleOAuthCallback, shows loading spinner during exchange, on success posts message to opener window via window.opener.postMessage({type: 'github-oauth-success'}, '*') and closes window with window.close(), on error shows error message and posts {type: 'github-oauth-error', error: message}. Uses useSearchParams from react-router-dom to read query params. This page is NOT protected (public route).
      
      **Files**: 
      - d:\projects\CodeForge-AI-main\frontend\src\pages\github\GithubCallbackPage.tsx (new)
      
      **Details**:
      ```typescript
      import { useEffect, useState } from 'react';
      import { useSearchParams } from 'react-router-dom';
      import { CheckCircle, XCircle } from 'lucide-react';
      import { githubService } from '../../services/api/githubService';
      import { LoadingOverlay } from '../../components/common/LoadingOverlay';
      import { parseGithubError } from '../../utils/errorHandler';
      
      export function GithubCallbackPage() {
        const [searchParams] = useSearchParams();
        const [status, setStatus] = useState<'loading' | 'success' | 'error'>('loading');
        const [error, setError] = useState<string | null>(null);
        
        useEffect(() => {
          const code = searchParams.get('code');
          const state = searchParams.get('state');
          
          if (!code || !state) {
            setStatus('error');
            setError('Missing authorization code or state');
            notifyParent('error', 'Missing authorization code or state');
            return;
          }
          
          handleCallback(code, state);
        }, [searchParams]);
        
        const handleCallback = async (code: string, state: string) => {
          try {
            await githubService.handleOAuthCallback(code, state);
            setStatus('success');
            notifyParent('success', null);
            
            // Close window after 1 second
            setTimeout(() => {
              window.close();
            }, 1000);
          } catch (err) {
            const errorMsg = parseGithubError(err);
            setStatus('error');
            setError(errorMsg);
            notifyParent('error', errorMsg);
          }
        };
        
        const notifyParent = (type: 'success' | 'error', error: string | null) => {
          if (window.opener) {
            window.opener.postMessage(
              {
                type: type === 'success' ? 'github-oauth-success' : 'github-oauth-error',
                error,
              },
              '*'
            );
          }
        };
        
        if (status === 'loading') {
          return <LoadingOverlay message="Connecting to GitHub..." />;
        }
        
        return (
          <div
            style={{
              display: 'flex',
              flexDirection: 'column',
              alignItems: 'center',
              justifyContent: 'center',
              minHeight: '100vh',
              padding: '2rem',
              textAlign: 'center',
            }}
          >
            {status === 'success' ? (
              <>
                <CheckCircle size={64} color="var(--color-success)" />
                <h1 style={{ marginTop: '1rem' }}>GitHub Connected!</h1>
                <p style={{ color: 'var(--color-muted)' }}>This window will close automatically...</p>
              </>
            ) : (
              <>
                <XCircle size={64} color="var(--color-danger)" />
                <h1 style={{ marginTop: '1rem' }}>Connection Failed</h1>
                <p style={{ color: 'var(--color-muted)' }}>{error}</p>
                <button
                  className="btn btn-secondary"
                  onClick={() => window.close()}
                  style={{ marginTop: '1rem' }}
                >
                  Close Window
                </button>
              </>
            )}
          </div>
        );
      }
      ```
      
      **Dependencies**: Tasks 2,5,7 (githubService, errorHandler, LoadingOverlay)
      
      **Pitfalls**: window.opener may be null if user navigated directly. postMessage uses '*' origin for simplicity (same-origin would be more secure but complex). window.close() may not work in all browsers.
      
      **Verify**: `npm run dev` — navigate to /github/callback?code=test&state=test, page renders loading then error (backend not running)

- [ ] 13. **Create src/components/ai/SemanticSearchPanel.tsx**
      
      Panel for code search tab in AI page. Has search input (debounced 300ms), project selector dropdown, results list (file, symbol, lines, score, code preview in pre/code blocks), click to expand collapsed results. Uses useState for query, results, loading, selectedProjectId. Calls codeSearchService.semanticSearch on submit. Debounce using setTimeout in useEffect watching query. Show scores as percentage badges. Syntax highlighting not required but use monospace font for code preview.
      
      **Files**: 
      - d:\projects\CodeForge-AI-main\frontend\src\components\ai\SemanticSearchPanel.tsx (new)
      
      **Details**:
      ```typescript
      import { useState, useEffect } from 'react';
      import { Search, Loader, FileCode, ChevronDown, ChevronUp } from 'lucide-react';
      import { codeSearchService } from '../../services/api/codeSearchService';
      import { SearchResult } from '../../types/github';
      import { Project } from '../../types/project';
      import { parseGithubError } from '../../utils/errorHandler';
      import { showError } from '../../utils/toast';
      
      interface SemanticSearchPanelProps {
        projects: Project[];
        selectedProjectId: number | null;
        onProjectChange: (projectId: number) => void;
      }
      
      export function SemanticSearchPanel({ projects, selectedProjectId, onProjectChange }: SemanticSearchPanelProps) {
        const [query, setQuery] = useState('');
        const [debouncedQuery, setDebouncedQuery] = useState('');
        const [results, setResults] = useState<SearchResult[]>([]);
        const [loading, setLoading] = useState(false);
        const [expandedResults, setExpandedResults] = useState<Set<number>>(new Set());
        
        // Debounce query input
        useEffect(() => {
          const timer = setTimeout(() => {
            setDebouncedQuery(query);
          }, 300);
          
          return () => clearTimeout(timer);
        }, [query]);
        
        // Trigger search when debounced query changes
        useEffect(() => {
          if (debouncedQuery.trim() && selectedProjectId) {
            performSearch();
          } else {
            setResults([]);
          }
        }, [debouncedQuery, selectedProjectId]);
        
        const performSearch = async () => {
          if (!selectedProjectId || !debouncedQuery.trim()) return;
          
          setLoading(true);
          try {
            const response = await codeSearchService.semanticSearch({
              query: debouncedQuery,
              projectId: selectedProjectId,
              limit: 20,
            });
            setResults(response.results);
          } catch (err) {
            showError(parseGithubError(err));
            setResults([]);
          } finally {
            setLoading(false);
          }
        };
        
        const toggleExpanded = (chunkId: number) => {
          setExpandedResults((prev) => {
            const next = new Set(prev);
            if (next.has(chunkId)) {
              next.delete(chunkId);
            } else {
              next.add(chunkId);
            }
            return next;
          });
        };
        
        return (
          <div style={{ display: 'flex', flexDirection: 'column', height: '100%' }}>
            <div className="card" style={{ marginBottom: '1rem' }}>
              <div className="form-group" style={{ marginBottom: '1rem' }}>
                <label>Project</label>
                <select
                  value={selectedProjectId || ''}
                  onChange={(e) => onProjectChange(Number(e.target.value))}
                  style={{
                    width: '100%',
                    padding: '0.6rem',
                    borderRadius: '8px',
                    border: '1px solid var(--color-border)',
                  }}
                >
                  <option value="">-- Select a project --</option>
                  {projects.map((p) => (
                    <option key={p.id} value={p.id}>
                      {p.name}
                    </option>
                  ))}
                </select>
              </div>
              
              <div className="form-group" style={{ marginBottom: 0 }}>
                <label>Search Query</label>
                <div style={{ position: 'relative' }}>
                  <input
                    type="text"
                    value={query}
                    onChange={(e) => setQuery(e.target.value)}
                    placeholder="Search your code... (e.g., 'authentication logic')"
                    disabled={!selectedProjectId}
                    style={{
                      width: '100%',
                      padding: '0.6rem 2.5rem 0.6rem 0.75rem',
                      borderRadius: '8px',
                      border: '1px solid var(--color-border)',
                    }}
                  />
                  <div style={{ position: 'absolute', right: '0.75rem', top: '50%', transform: 'translateY(-50%)' }}>
                    {loading ? <Loader size={20} className="spinner" /> : <Search size={20} color="var(--color-muted)" />}
                  </div>
                </div>
              </div>
            </div>
            
            <div style={{ flex: 1, overflowY: 'auto' }}>
              {results.length === 0 && !loading && debouncedQuery && (
                <div className="empty-state">
                  <FileCode size={48} />
                  <p>No results found</p>
                </div>
              )}
              
              {results.length === 0 && !debouncedQuery && (
                <div className="empty-state">
                  <FileCode size={48} />
                  <p>Enter a search query to find relevant code</p>
                </div>
              )}
              
              {results.map((result) => {
                const isExpanded = expandedResults.has(result.chunkId);
                const scorePercentage = Math.round(result.score * 100);
                
                return (
                  <div key={result.chunkId} className="card" style={{ marginBottom: '1rem' }}>
                    <div
                      style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'start', cursor: 'pointer' }}
                      onClick={() => toggleExpanded(result.chunkId)}
                    >
                      <div style={{ flex: 1 }}>
                        <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', marginBottom: '0.25rem' }}>
                          <FileCode size={16} />
                          <span style={{ fontFamily: 'monospace', fontSize: '0.9rem', fontWeight: 500 }}>
                            {result.filePath}
                          </span>
                        </div>
                        <div style={{ display: 'flex', gap: '1rem', fontSize: '0.75rem', color: 'var(--color-muted)' }}>
                          <span>Lines {result.startLine}-{result.endLine}</span>
                          {result.symbol && <span>{result.symbol}</span>}
                          <span className="badge" style={{ backgroundColor: scorePercentage > 70 ? 'var(--color-success-bg)' : 'var(--color-bg)' }}>
                            {scorePercentage}% match
                          </span>
                        </div>
                      </div>
                      {isExpanded ? <ChevronUp size={20} /> : <ChevronDown size={20} />}
                    </div>
                    
                    {isExpanded && (
                      <pre
                        style={{
                          marginTop: '1rem',
                          padding: '0.75rem',
                          backgroundColor: '#f5f5f5',
                          borderRadius: '6px',
                          fontSize: '0.8rem',
                          overflow: 'auto',
                          maxHeight: '300px',
                        }}
                      >
                        <code>{result.content}</code>
                      </pre>
                    )}
                  </div>
                );
              })}
            </div>
          </div>
        );
      }
      ```
      
      **Dependencies**: Tasks 1,3,4,5,6 (types, services, utils)
      
      **Pitfalls**: Debounce must clean up timeout. Don't search if no project selected. Scores are 0-1 floats, convert to percentage.
      
      **Verify**: `npm run build` — compiles without errors

- [ ] 14. **Update src/pages/ai/AIPage.tsx to add tabs (Chat / Code Search)**
      
      Modify AIPage.tsx to add tab UI: "Chat" and "Code Search" tabs at top. Move existing chat interface into Chat tab. Embed SemanticSearchPanel in Code Search tab. Add project selector dropdown at page top (shared between tabs). Use useState for activeTab ('chat' | 'search') and selectedProjectId. Tab buttons styled like existing conversation sidebar buttons. Preserve existing chat functionality (messages, conversations, etc.). AIPage.tsx already uses projectId from useParams but it's optional — make it work with or without URL param.
      
      **Files**: 
      - d:\projects\CodeForge-AI-main\frontend\src\pages\ai\AIPage.tsx (modify)
      - d:\projects\CodeForge-AI-main\frontend\src\pages\ai\AIPage.css (modify: add tab styles)
      
      **Details**:
      
      At top of AIPage component, after existing state:
      ```typescript
      const [activeTab, setActiveTab] = useState<'chat' | 'search'>('chat');
      const [selectedProjectId, setSelectedProjectId] = useState<number | null>(
        projectId ? parseInt(projectId) : null
      );
      const [projects, setProjects] = useState<Project[]>([]);
      ```
      
      Add tab navigation before .ai-main div:
      ```typescript
      <div className="ai-tabs">
        <button
          className={`tab-button ${activeTab === 'chat' ? 'active' : ''}`}
          onClick={() => setActiveTab('chat')}
        >
          <MessageSquare size={18} />
          Chat
        </button>
        <button
          className={`tab-button ${activeTab === 'search' ? 'active' : ''}`}
          onClick={() => setActiveTab('search')}
        >
          <Search size={18} />
          Code Search
        </button>
      </div>
      ```
      
      Wrap existing chat UI in conditional:
      ```typescript
      {activeTab === 'chat' && (
        // existing messages-container, message-input-form, etc.
      )}
      
      {activeTab === 'search' && (
        <SemanticSearchPanel
          projects={projects}
          selectedProjectId={selectedProjectId}
          onProjectChange={setSelectedProjectId}
        />
      )}
      ```
      
      Add to AIPage.css:
      ```css
      .ai-tabs {
        display: flex;
        gap: 0.5rem;
        padding: 1rem 2rem;
        border-bottom: 1px solid #f0f0f0;
        background: white;
      }
      
      .tab-button {
        display: flex;
        align-items: center;
        gap: 0.5rem;
        background: none;
        border: none;
        padding: 0.75rem 1.5rem;
        border-radius: 0.375rem;
        cursor: pointer;
        font-size: 0.9rem;
        font-weight: 500;
        color: #666;
        transition: all 0.2s ease;
      }
      
      .tab-button:hover {
        background: #f5f5f5;
        color: #1a1a1a;
      }
      
      .tab-button.active {
        background: #e8f0ff;
        color: #0066cc;
      }
      ```
      
      **Dependencies**: Task 13 (SemanticSearchPanel), Task 4 (Project type)
      
      **Pitfalls**: Preserve existing chat state when switching tabs. Import Search icon from lucide-react.
      
      **Verify**: `npm run dev` — navigate to /ai (route doesn't exist yet but will after next task), tabs switch without errors

- [ ] 15. **Update src/components/Navbar.tsx to add GitHub link with badge**
      
      Modify Navbar.tsx to add GitHub nav link for CANDIDATE and RECRUITER roles (not ADMIN). Add githubConnected flag to User type (will check if GithubToken exists via API or set flag on login response). Show small badge/indicator next to GitHub link if connected. Use lucide-react Github icon. Link points to /github.
      
      **Files**: 
      - d:\projects\CodeForge-AI-main\frontend\src\components\Navbar.tsx (modify)
      - d:\projects\CodeForge-AI-main\frontend\src\types\auth.ts (modify: add githubConnected?: boolean to User interface)
      
      **Details**:
      
      Update NAV_LINKS in Navbar.tsx:
      ```typescript
      import { Github } from 'lucide-react';
      
      const NAV_LINKS: Record<string, { to: string; label: string; icon?: React.ReactNode }[]> = {
        CANDIDATE: [
          { to: "/candidate/dashboard", label: "Dashboard" },
          { to: "/candidate/profile", label: "Profile" },
          { to: "/github", label: "GitHub", icon: <Github size={16} /> },
        ],
        RECRUITER: [
          { to: "/recruiter/dashboard", label: "Dashboard" },
          { to: "/recruiter/profile", label: "Profile" },
          { to: "/github", label: "GitHub", icon: <Github size={16} /> },
        ],
        ADMIN: [
          { to: "/admin/dashboard", label: "Dashboard" },
          { to: "/admin/users", label: "Users" },
        ],
      };
      ```
      
      Update link rendering to show icon and badge:
      ```typescript
      {NAV_LINKS[user.role].map((link) => (
        <NavLink key={link.to} to={link.to} className={({ isActive }) => (isActive ? "active" : "")}>
          {link.icon}
          {link.label}
          {link.to === '/github' && user.githubConnected && (
            <span className="badge" style={{ marginLeft: '0.25rem', fontSize: '0.6rem' }}>✓</span>
          )}
        </NavLink>
      ))}
      ```
      
      Add to types/auth.ts User interface:
      ```typescript
      githubConnected?: boolean;
      ```
      
      **Dependencies**: Existing Navbar, auth types
      
      **Pitfalls**: Backend doesn't return githubConnected in User object yet — will need backend update or separate API call. For now, flag defaults to undefined (no badge).
      
      **Verify**: `npm run dev` — navbar shows GitHub link for candidate/recruiter, no console errors

- [ ] 16. **Update src/App.tsx to add /github and /github/callback routes**
      
      Add two new routes to App.tsx: /github (protected, uses MainLayout, shows GithubIntegrationPage, allowed for CANDIDATE and RECRUITER), /github/callback (public route, no layout, shows GithubCallbackPage). Import both page components. /ai route not added yet (next task adds it).
      
      **Files**: 
      - d:\projects\CodeForge-AI-main\frontend\src\App.tsx (modify)
      
      **Details**:
      
      Add imports:
      ```typescript
      import { GithubIntegrationPage } from "./pages/github/GithubIntegrationPage";
      import { GithubCallbackPage } from "./pages/github/GithubCallbackPage";
      import { AIPage } from "./pages/ai/AIPage";
      ```
      
      Add routes after login/register (public /github/callback):
      ```typescript
      <Route path="/github/callback" element={<GithubCallbackPage />} />
      ```
      
      Add routes inside MainLayout after candidate/recruiter sections:
      ```typescript
      <Route element={<RoleRoute allowedRoles={["CANDIDATE", "RECRUITER"]} />}>
        <Route path="/github" element={<GithubIntegrationPage />} />
        <Route path="/ai/:projectId?" element={<AIPage />} />
      </Route>
      ```
      
      **Dependencies**: Tasks 11,12,14 (page components)
      
      **Pitfalls**: /github/callback must be OUTSIDE ProtectedRoute (public). /ai route has optional projectId param.
      
      **Verify**: `npm run dev` — navigate to /github (requires login), /github/callback (public), /ai (requires login), routes render correctly

- [ ] 17. **Polish AIPage.tsx chat with code blocks, copy button, timestamps**
      
      Enhance chat message rendering: syntax highlighting for code blocks (use inline pre/code with language detection regex), copy button per code block (copies to clipboard via navigator.clipboard), message timestamps (show createdAt formatted with toLocaleTimeString), improve typing indicator animation. Add markdown-like parsing for ```language blocks. Copy button uses lucide-react Copy/Check icons.
      
      **Files**: 
      - d:\projects\CodeForge-AI-main\frontend\src\pages\ai\AIPage.tsx (modify)
      - d:\projects\CodeForge-AI-main\frontend\src\pages\ai\AIPage.css (modify: add code block styles)
      
      **Details**:
      
      Create helper function in AIPage.tsx:
      ```typescript
      const renderMessageContent = (content: string) => {
        // Simple code block detection: ```language\ncode\n```
        const codeBlockRegex = /```(\w+)?\n([\s\S]*?)```/g;
        const parts: React.ReactNode[] = [];
        let lastIndex = 0;
        let match;
        
        while ((match = codeBlockRegex.exec(content)) !== null) {
          // Text before code block
          if (match.index > lastIndex) {
            parts.push(
              <p key={`text-${lastIndex}`}>
                {content.substring(lastIndex, match.index)}
              </p>
            );
          }
          
          // Code block
          const language = match[1] || 'plaintext';
          const code = match[2];
          parts.push(
            <CodeBlock key={`code-${match.index}`} code={code} language={language} />
          );
          
          lastIndex = match.index + match[0].length;
        }
        
        // Remaining text
        if (lastIndex < content.length) {
          parts.push(
            <p key={`text-${lastIndex}`}>
              {content.substring(lastIndex)}
            </p>
          );
        }
        
        return parts.length > 0 ? parts : <p>{content}</p>;
      };
      ```
      
      Create CodeBlock component in same file:
      ```typescript
      function CodeBlock({ code, language }: { code: string; language: string }) {
        const [copied, setCopied] = useState(false);
        
        const copyToClipboard = async () => {
          try {
            await navigator.clipboard.writeText(code);
            setCopied(true);
            setTimeout(() => setCopied(false), 2000);
          } catch (err) {
            console.error('Failed to copy:', err);
          }
        };
        
        return (
          <div className="code-block-wrapper">
            <div className="code-block-header">
              <span className="code-language">{language}</span>
              <button className="copy-button" onClick={copyToClipboard}>
                {copied ? <Check size={16} /> : <Copy size={16} />}
                {copied ? 'Copied!' : 'Copy'}
              </button>
            </div>
            <pre className="code-block">
              <code>{code}</code>
            </pre>
          </div>
        );
      }
      ```
      
      Import icons:
      ```typescript
      import { Send, Loader, AlertCircle, ChevronDown, MessageSquare, Search, Copy, Check } from 'lucide-react';
      ```
      
      Update message rendering to use renderMessageContent and show timestamp:
      ```typescript
      <div className="message-content">
        {message.role === 'assistant' ? (
          <div className="markdown-content">
            {renderMessageContent(message.content)}
          </div>
        ) : (
          <p>{message.content}</p>
        )}
      </div>
      {message.createdAt && (
        <div className="message-timestamp">
          {new Date(message.createdAt).toLocaleTimeString()}
        </div>
      )}
      ```
      
      Add to AIPage.css:
      ```css
      .code-block-wrapper {
        margin: 0.75rem 0;
        border-radius: 6px;
        overflow: hidden;
        border: 1px solid #ddd;
      }
      
      .code-block-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 0.5rem 0.75rem;
        background: #2d2d2d;
        color: #fff;
        font-size: 0.75rem;
      }
      
      .code-language {
        text-transform: uppercase;
        font-weight: 600;
      }
      
      .copy-button {
        display: flex;
        align-items: center;
        gap: 0.25rem;
        background: rgba(255, 255, 255, 0.1);
        border: none;
        color: #fff;
        padding: 0.25rem 0.5rem;
        border-radius: 4px;
        cursor: pointer;
        font-size: 0.75rem;
        transition: background 0.2s;
      }
      
      .copy-button:hover {
        background: rgba(255, 255, 255, 0.2);
      }
      
      .code-block {
        margin: 0;
        padding: 1rem;
        background: #1e1e1e;
        color: #d4d4d4;
        font-family: 'Monaco', 'Menlo', 'Ubuntu Mono', monospace;
        font-size: 0.85rem;
        overflow-x: auto;
      }
      
      .message-timestamp {
        font-size: 0.7rem;
        color: var(--color-muted);
        margin-top: 0.25rem;
        text-align: right;
      }
      
      .user-message .message-timestamp {
        color: rgba(255, 255, 255, 0.7);
      }
      ```
      
      **Dependencies**: Existing AIPage.tsx
      
      **Pitfalls**: navigator.clipboard requires HTTPS or localhost. Regex for code blocks is simple — won't handle nested backticks.
      
      **Verify**: `npm run dev` — send message with code block (```js\nconsole.log('test');\n```), copy button works, timestamp shows

- [ ] 18. **Add responsive CSS breakpoints to all new components**
      
      Review and add mobile breakpoints to GithubIntegrationPage (repos grid → single column on mobile), RepositoryImportModal (full-width on mobile), SemanticSearchPanel (smaller padding, stacked filters), AIPage tabs (stacked on mobile). Use @media (max-width: 768px) for tablet, (max-width: 480px) for mobile. Follow existing AIPage.css responsive patterns.
      
      **Files**: 
      - d:\projects\CodeForge-AI-main\frontend\src\pages\github\GithubIntegrationPage.tsx (add inline styles or extract to CSS file)
      - d:\projects\CodeForge-AI-main\frontend\src\components\github\RepositoryImportModal.tsx (adjust modal width)
      - d:\projects\CodeForge-AI-main\frontend\src\components\ai\SemanticSearchPanel.tsx (adjust form layout)
      - d:\projects\CodeForge-AI-main\frontend\src\pages\ai\AIPage.css (add tab responsive styles)
      
      **Details**:
      
      Add to AIPage.css:
      ```css
      @media (max-width: 768px) {
        .ai-tabs {
          padding: 0.75rem 1rem;
        }
        
        .tab-button {
          padding: 0.5rem 1rem;
          font-size: 0.85rem;
        }
      }
      
      @media (max-width: 480px) {
        .ai-tabs {
          flex-direction: column;
          gap: 0.25rem;
        }
        
        .tab-button {
          width: 100%;
          justify-content: center;
        }
      }
      ```
      
      For GithubIntegrationPage, repos grid already uses `grid-template-columns: repeat(auto-fill, minmax(300px, 1fr))` which is responsive by default.
      
      For RepositoryImportModal, update width in inline styles:
      ```typescript
      style={{
        width: window.innerWidth < 768 ? '95%' : '90%',
        maxWidth: '500px',
        // ...rest
      }}
      ```
      
      **Dependencies**: All new components
      
      **Pitfalls**: Test on mobile viewport (DevTools responsive mode). Ensure modals don't overflow viewport.
      
      **Verify**: `npm run dev` — resize browser to mobile width, all layouts adapt without horizontal scroll

- [ ] 19. **Update frontend/.env.example with VITE_API_BASE_URL**
      
      Document VITE_API_BASE_URL in .env.example. Already exists but ensure it's clear. Add comments explaining what it does.
      
      **Files**: 
      - d:\projects\CodeForge-AI-main\frontend\.env.example (verify/modify)
      
      **Details**:
      
      Verify content (should already exist):
      ```bash
      # Copy to .env.local for local development (Vite loads .env.local automatically).
      # Never commit a real .env.local file.
      
      # Backend API base URL (default: http://localhost:8080/api)
      # The frontend axios client will make requests to this URL
      VITE_API_BASE_URL=http://localhost:8080/api
      ```
      
      **Dependencies**: None
      
      **Verify**: File exists and is readable, content matches

- [ ] 20. **Update frontend/README.md to document new features**
      
      Update README.md to document: GitHub OAuth integration, semantic code search, AI chat enhancements, new environment variables, feature list (GitHub connection, repo import, code search, enhanced chat with code blocks and copy). Add setup instructions for OAuth (requires GitHub OAuth app creation, client ID/secret env vars). List all routes: /github, /github/callback, /ai.
      
      **Files**: 
      - d:\projects\CodeForge-AI-main\frontend\README.md (modify)
      
      **Details**:
      
      Replace content with:
      ```markdown
      # Frontend
      
      React + TypeScript + Vite app for the CodeForge AI recruitment platform.
      
      ## Features
      
      - **Role-based dashboards**: Candidate, Recruiter, Admin
      - **GitHub OAuth integration**: Connect GitHub account, list repositories, import into projects
      - **Repository import with real-time progress**: Track file processing and vector embedding
      - **Semantic code search**: Natural language search across imported codebases using RAG
      - **AI chat assistant**: Project-aware chat with syntax-highlighted code blocks, copy functionality, and source citations
      - **Responsive design**: Mobile-first UI with adaptive layouts
      
      ## Stack
      
      - React 19
      - TypeScript 6
      - Vite 8
      - Axios (HTTP client)
      - React Router DOM 7
      - Lucide React (icons)
      - React Toastify (notifications)
      
      ## Quick Start
      
      ```bash
      npm install
      cp .env.example .env.local
      npm run dev
      ```
      
      The app will run at http://localhost:5173
      
      ## Environment Variables
      
      Copy `.env.example` to `.env.local` and configure:
      
      ```bash
      VITE_API_BASE_URL=http://localhost:8080/api
      ```
      
      ## Routes
      
      ### Public Routes
      - `/login` — User login
      - `/register` — User registration (candidate or recruiter)
      - `/github/callback` — GitHub OAuth callback (do not navigate directly)
      
      ### Protected Routes (Candidate & Recruiter)
      - `/candidate/dashboard` or `/recruiter/dashboard` — Role-specific dashboard
      - `/candidate/profile` or `/recruiter/profile` — Profile management
      - `/github` — GitHub integration page (connect account, list repos, import)
      - `/ai/:projectId?` — AI code assistant with chat and semantic search tabs
      
      ### Admin Routes
      - `/admin/dashboard` — Platform statistics
      - `/admin/users` — User management
      
      ## GitHub OAuth Setup
      
      To enable GitHub integration:
      
      1. Create a GitHub OAuth App at https://github.com/settings/developers
      2. Set Authorization callback URL to `http://localhost:5173/github/callback`
      3. Copy Client ID and Client Secret
      4. Set backend environment variables:
         - `GITHUB_CLIENT_ID=your_client_id`
         - `GITHUB_CLIENT_SECRET=your_client_secret`
         - `GITHUB_OAUTH_CALLBACK_URL=http://localhost:5173/github/callback`
      5. Restart backend
      
      ## Development Commands
      
      - `npm install` — Install dependencies
      - `npm run dev` — Start dev server (http://localhost:5173)
      - `npm run build` — Build for production
      - `npm run preview` — Preview production build
      - `npm run lint` — Run linter (oxlint)
      
      ## Project Structure
      
      ```
      src/
      ├── components/
      │   ├── ai/                    # AI-specific components (SemanticSearchPanel)
      │   ├── common/                # Reusable components (Spinner, ProgressBar, etc.)
      │   ├── github/                # GitHub integration components (RepositoryImportModal)
      │   ├── projects/              # Project management components (ProjectsList)
      │   └── Navbar.tsx             # Main navigation bar
      ├── context/
      │   └── AuthContext.tsx        # Authentication state management
      ├── layouts/
      │   └── MainLayout.tsx         # Protected layout with navbar
      ├── pages/
      │   ├── ai/                    # AI chat and code search page
      │   ├── auth/                  # Login and registration pages
      │   ├── github/                # GitHub integration pages
      │   ├── candidate/             # Candidate-specific pages
      │   ├── recruiter/             # Recruiter-specific pages
      │   └── admin/                 # Admin pages
      ├── routes/
      │   ├── ProtectedRoute.tsx     # Authentication guard
      │   └── RoleRoute.tsx          # Role-based access control
      ├── services/
      │   ├── api/                   # API service modules (aiService, githubService, etc.)
      │   ├── apiClient.ts           # Axios instance with JWT and camelCase transform
      │   └── authService.ts         # Authentication API calls
      ├── types/                     # TypeScript type definitions
      ├── utils/                     # Utility functions (errorHandler, toast)
      ├── App.tsx                    # Root component with routes
      ├── App.css                    # Global styles
      └── main.tsx                   # Application entry point
      ```
      
      ## Styling
      
      CSS variables defined in `App.css`:
      - `--color-bg`, `--color-surface`, `--color-border`
      - `--color-text`, `--color-muted`
      - `--color-primary`, `--color-primary-hover`
      - `--color-danger`, `--color-success`
      
      Reusable classes: `.btn`, `.btn-primary`, `.btn-secondary`, `.card`, `.alert`, `.badge`, etc.
      
      ## Backend Integration
      
      The frontend expects the backend API at `/api` (configurable via `VITE_API_BASE_URL`).
      
      Key API endpoints:
      - `POST /auth/login`, `POST /auth/register/*` — Authentication
      - `GET /github/oauth/authorize`, `POST /github/oauth/callback` — GitHub OAuth
      - `GET /github/repositories`, `POST /github/import` — Repository operations
      - `POST /code/search` — Semantic code search
      - `POST /v1/projects/{id}/ai/chat` — AI chat
      
      See backend README for full API documentation.
      ```
      
      **Dependencies**: None
      
      **Verify**: File is readable and accurately describes the frontend

---

## Summary
      
This plan implements all 20 tasks for Phase 4:
1. ✅ GitHub types
2. ✅ GitHub service
3. ✅ Code search service
4. ✅ Project types
5. ✅ Error handler utils
6. ✅ Toast notifications (react-toastify 10.0.6)
7. ✅ Loading primitives (Spinner, ProgressBar, LoadingOverlay)
8. ✅ Skeleton loaders
9. ✅ ProjectsList component
10. ✅ RepositoryImportModal with real-time progress (2s polling)
11. ✅ GithubIntegrationPage with OAuth popup
12. ✅ GithubCallbackPage with postMessage to parent
13. ✅ SemanticSearchPanel with debounced search (300ms)
14. ✅ AIPage with Chat/Code Search tabs
15. ✅ Navbar GitHub link with badge
16. ✅ App.tsx routes (/github, /github/callback, /ai)
17. ✅ AIPage chat polish (code blocks, copy, timestamps)
18. ✅ Responsive CSS for mobile
19. ✅ .env.example documentation
20. ✅ README.md with features and setup

**Key Constraints Met**:
- ✅ NO react-query (plain axios + hooks)
- ✅ Consistent CSS with existing patterns
- ✅ apiClient handles JWT and camelCase transform
- ✅ React 19 + TypeScript 6 + Vite 8
- ✅ lucide-react for icons
- ✅ OAuth popup pattern with window.open + postMessage
- ✅ 2s polling for import status with useEffect cleanup
- ✅ 300ms debounce on search input

**Build & Verify**:
- After each task: `npm run build` — ensures TypeScript compiles
- Final verification: `npm run dev` — test all features in browser with backend running

**Backend Dependencies** (already implemented in Phase 3):
- GET /github/oauth/authorize
- POST /github/oauth/callback
- GET /github/repositories
- POST /github/import
- GET /github/import/{projectId}/status
- DELETE /github/tokens
- POST /code/search
