-- ================================================================
-- CodeForge AI - Initial Database Schema (Flyway V1)
-- ================================================================
-- This migration creates the complete schema for CodeForge AI
-- Generated from JPA entity definitions
-- Database: Microsoft SQL Server 2022
-- ================================================================

-- ================================================================
-- USERS TABLE (Base entity for all roles)
-- ================================================================
CREATE TABLE users (
    id BIGINT PRIMARY KEY IDENTITY(1,1),
    name NVARCHAR(150) NOT NULL,
    email NVARCHAR(255) NOT NULL UNIQUE,
    password_hash NVARCHAR(MAX) NOT NULL,
    role VARCHAR(50) NOT NULL CHECK (role IN ('CANDIDATE', 'RECRUITER', 'ADMIN')),
    enabled BIT NOT NULL DEFAULT 1,
    created_at DATETIME2 NOT NULL DEFAULT GETUTCDATE(),
    updated_at DATETIME2 NOT NULL DEFAULT GETUTCDATE()
);

CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_role ON users(role);

-- ================================================================
-- CANDIDATE TABLE (One-to-one with users)
-- ================================================================
CREATE TABLE candidates (
    id BIGINT PRIMARY KEY IDENTITY(1,1),
    user_id BIGINT NOT NULL UNIQUE,
    phone NVARCHAR(20),
    location NVARCHAR(255),
    bio NVARCHAR(MAX),
    skills NVARCHAR(MAX),
    github_url NVARCHAR(500),
    linkedin_url NVARCHAR(500),
    profile_picture_path NVARCHAR(500),
    created_at DATETIME2 NOT NULL DEFAULT GETUTCDATE(),
    updated_at DATETIME2 NOT NULL DEFAULT GETUTCDATE(),
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

CREATE INDEX idx_candidates_user_id ON candidates(user_id);

-- ================================================================
-- COMPANY TABLE
-- ================================================================
CREATE TABLE companies (
    id BIGINT PRIMARY KEY IDENTITY(1,1),
    name NVARCHAR(255) NOT NULL,
    website NVARCHAR(500),
    location NVARCHAR(255),
    description NVARCHAR(MAX),
    logo_path NVARCHAR(500),
    created_at DATETIME2 NOT NULL DEFAULT GETUTCDATE(),
    updated_at DATETIME2 NOT NULL DEFAULT GETUTCDATE()
);

-- ================================================================
-- RECRUITER TABLE (One-to-one with users)
-- ================================================================
CREATE TABLE recruiters (
    id BIGINT PRIMARY KEY IDENTITY(1,1),
    user_id BIGINT NOT NULL UNIQUE,
    phone NVARCHAR(20),
    position NVARCHAR(255),
    bio NVARCHAR(MAX),
    company_id BIGINT,
    company_name NVARCHAR(255),
    profile_picture_path NVARCHAR(500),
    created_at DATETIME2 NOT NULL DEFAULT GETUTCDATE(),
    updated_at DATETIME2 NOT NULL DEFAULT GETUTCDATE(),
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (company_id) REFERENCES companies(id) ON DELETE SET NULL
);

CREATE INDEX idx_recruiters_user_id ON recruiters(user_id);
CREATE INDEX idx_recruiters_company_id ON recruiters(company_id);

-- ================================================================
-- PROJECT TABLE (For storing repository metadata)
-- ================================================================
CREATE TABLE projects (
    id BIGINT PRIMARY KEY IDENTITY(1,1),
    name NVARCHAR(255) NOT NULL,
    description NVARCHAR(MAX),
    github_url NVARCHAR(500),
    github_repository_name NVARCHAR(255),
    github_owner NVARCHAR(255),
    repository_url NVARCHAR(500),
    owner_id BIGINT NOT NULL,
    last_synced_at DATETIME2,
    created_at DATETIME2 NOT NULL DEFAULT GETUTCDATE(),
    updated_at DATETIME2 NOT NULL DEFAULT GETUTCDATE(),
    FOREIGN KEY (owner_id) REFERENCES users(id) ON DELETE CASCADE
);

CREATE INDEX idx_projects_owner_id ON projects(owner_id);
CREATE INDEX idx_projects_github_url ON projects(github_url);

-- ================================================================
-- FILE TABLE (For storing file metadata)
-- ================================================================
CREATE TABLE files (
    id BIGINT PRIMARY KEY IDENTITY(1,1),
    project_id BIGINT NOT NULL,
    name NVARCHAR(255) NOT NULL,
    path NVARCHAR(MAX) NOT NULL,
    content NVARCHAR(MAX),
    language NVARCHAR(50),
    file_size BIGINT,
    last_modified_at DATETIME2,
    created_at DATETIME2 NOT NULL DEFAULT GETUTCDATE(),
    updated_at DATETIME2 NOT NULL DEFAULT GETUTCDATE(),
    FOREIGN KEY (project_id) REFERENCES projects(id) ON DELETE CASCADE
);

CREATE INDEX idx_files_project_id ON files(project_id);
CREATE INDEX idx_files_language ON files(language);

-- ================================================================
-- CODE_DOCUMENT TABLE (For RAG - document-level metadata)
-- ================================================================
CREATE TABLE code_documents (
    id BIGINT PRIMARY KEY IDENTITY(1,1),
    project_id BIGINT NOT NULL,
    file_id BIGINT,
    file_path NVARCHAR(MAX) NOT NULL,
    file_name NVARCHAR(255) NOT NULL,
    language NVARCHAR(50),
    content NVARCHAR(MAX),
    content_hash NVARCHAR(64),
    indexed_at DATETIME2,
    created_at DATETIME2 NOT NULL DEFAULT GETUTCDATE(),
    updated_at DATETIME2 NOT NULL DEFAULT GETUTCDATE(),
    FOREIGN KEY (project_id) REFERENCES projects(id) ON DELETE CASCADE,
    FOREIGN KEY (file_id) REFERENCES files(id) ON DELETE NO ACTION
);

CREATE INDEX idx_code_documents_project_id ON code_documents(project_id);
CREATE INDEX idx_code_documents_language ON code_documents(language);

-- ================================================================
-- CODE_CHUNK TABLE (For RAG - code chunk embeddings)
-- ================================================================
CREATE TABLE code_chunks (
    id BIGINT PRIMARY KEY IDENTITY(1,1),
    code_document_id BIGINT NOT NULL,
    content NVARCHAR(MAX) NOT NULL,
    start_line BIGINT,
    end_line BIGINT,
    language NVARCHAR(50),
    symbol_name NVARCHAR(500),
    embedding VARBINARY(MAX),
    created_at DATETIME2 NOT NULL DEFAULT GETUTCDATE(),
    FOREIGN KEY (code_document_id) REFERENCES code_documents(id) ON DELETE CASCADE
);

CREATE INDEX idx_code_chunks_document_id ON code_chunks(code_document_id);
CREATE INDEX idx_code_chunks_language ON code_chunks(language);

-- ================================================================
-- AI_CONVERSATION TABLE (Stores conversation threads)
-- ================================================================
CREATE TABLE ai_conversations (
    id BIGINT PRIMARY KEY IDENTITY(1,1),
    project_id BIGINT NOT NULL,
    user_id BIGINT NOT NULL,
    title NVARCHAR(500),
    context_summary NVARCHAR(MAX),
    created_at DATETIME2 NOT NULL DEFAULT GETUTCDATE(),
    updated_at DATETIME2 NOT NULL DEFAULT GETUTCDATE(),
    FOREIGN KEY (project_id) REFERENCES projects(id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE NO ACTION
);

CREATE INDEX idx_ai_conversations_project_id ON ai_conversations(project_id);
CREATE INDEX idx_ai_conversations_user_id ON ai_conversations(user_id);

-- ================================================================
-- AI_MESSAGE TABLE (Individual messages in conversations)
-- ================================================================
CREATE TABLE ai_messages (
    id BIGINT PRIMARY KEY IDENTITY(1,1),
    conversation_id BIGINT NOT NULL,
    role VARCHAR(50) NOT NULL CHECK (role IN ('USER', 'ASSISTANT', 'SYSTEM')),
    content NVARCHAR(MAX) NOT NULL,
    sources NVARCHAR(MAX),
    tokens_used INT,
    processing_time_ms BIGINT,
    created_at DATETIME2 NOT NULL DEFAULT GETUTCDATE(),
    FOREIGN KEY (conversation_id) REFERENCES ai_conversations(id) ON DELETE CASCADE
);

CREATE INDEX idx_ai_messages_conversation_id ON ai_messages(conversation_id);
CREATE INDEX idx_ai_messages_created_at ON ai_messages(created_at);

-- ================================================================
-- AI_TASK TABLE (For async AI task execution)
-- ================================================================
CREATE TABLE ai_tasks (
    id BIGINT PRIMARY KEY IDENTITY(1,1),
    user_id BIGINT NOT NULL,
    project_id BIGINT,
    task_type VARCHAR(100) NOT NULL,
    input_data NVARCHAR(MAX),
    output_data NVARCHAR(MAX),
    status VARCHAR(50) NOT NULL DEFAULT 'PENDING' CHECK (status IN ('PENDING', 'RUNNING', 'COMPLETED', 'FAILED')),
    error_message NVARCHAR(MAX),
    execution_start_time DATETIME2,
    execution_end_time DATETIME2,
    executed_by_agent_id NVARCHAR(255),
    created_at DATETIME2 NOT NULL DEFAULT GETUTCDATE(),
    updated_at DATETIME2 NOT NULL DEFAULT GETUTCDATE(),
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (project_id) REFERENCES projects(id) ON DELETE NO ACTION
);

CREATE INDEX idx_ai_tasks_user_id ON ai_tasks(user_id);
CREATE INDEX idx_ai_tasks_status ON ai_tasks(status);
CREATE INDEX idx_ai_tasks_created_at ON ai_tasks(created_at);

-- ================================================================
-- AI_ANALYSIS TABLE (Results of code analysis)
-- ================================================================
CREATE TABLE ai_analyses (
    id BIGINT PRIMARY KEY IDENTITY(1,1),
    code_document_id BIGINT,
    analysis_type VARCHAR(100),
    analysis_result NVARCHAR(MAX),
    summary NVARCHAR(MAX),
    performed_by_user_id BIGINT,
    created_at DATETIME2 NOT NULL DEFAULT GETUTCDATE(),
    FOREIGN KEY (code_document_id) REFERENCES code_documents(id) ON DELETE SET NULL,
    FOREIGN KEY (performed_by_user_id) REFERENCES users(id) ON DELETE SET NULL
);

CREATE INDEX idx_ai_analyses_document_id ON ai_analyses(code_document_id);
CREATE INDEX idx_ai_analyses_type ON ai_analyses(analysis_type);

-- ================================================================
-- GITHUB_TOKEN TABLE (For OAuth integration)
-- ================================================================
CREATE TABLE github_tokens (
    id BIGINT PRIMARY KEY IDENTITY(1,1),
    user_id BIGINT NOT NULL UNIQUE,
    access_token NVARCHAR(MAX) NOT NULL,
    refresh_token NVARCHAR(MAX),
    expires_at DATETIME2,
    scopes NVARCHAR(500),
    created_at DATETIME2 NOT NULL DEFAULT GETUTCDATE(),
    updated_at DATETIME2 NOT NULL DEFAULT GETUTCDATE(),
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

CREATE INDEX idx_github_tokens_user_id ON github_tokens(user_id);

-- ================================================================
-- AGENT_EXECUTION TABLE (For tracking agent task execution)
-- ================================================================
CREATE TABLE agent_executions (
    id BIGINT PRIMARY KEY IDENTITY(1,1),
    ai_task_id BIGINT,
    agent_id NVARCHAR(255),
    status VARCHAR(50),
    start_time DATETIME2,
    end_time DATETIME2,
    result_summary NVARCHAR(MAX),
    created_at DATETIME2 NOT NULL DEFAULT GETUTCDATE(),
    FOREIGN KEY (ai_task_id) REFERENCES ai_tasks(id) ON DELETE SET NULL
);

CREATE INDEX idx_agent_executions_task_id ON agent_executions(ai_task_id);
CREATE INDEX idx_agent_executions_agent_id ON agent_executions(agent_id);

-- ================================================================
-- REPOSITORY_INDEX_METADATA TABLE (For tracking indexing progress)
-- ================================================================
CREATE TABLE repository_index_metadata (
    id BIGINT PRIMARY KEY IDENTITY(1,1),
    project_id BIGINT NOT NULL UNIQUE,
    total_files BIGINT,
    indexed_files BIGINT,
    total_chunks BIGINT,
    last_indexed_at DATETIME2,
    status VARCHAR(50),
    created_at DATETIME2 NOT NULL DEFAULT GETUTCDATE(),
    updated_at DATETIME2 NOT NULL DEFAULT GETUTCDATE(),
    FOREIGN KEY (project_id) REFERENCES projects(id) ON DELETE CASCADE
);

-- ================================================================
-- TASK_WORKSPACE TABLE (For task execution environment)
-- ================================================================
CREATE TABLE task_workspaces (
    id BIGINT PRIMARY KEY IDENTITY(1,1),
    ai_task_id BIGINT NOT NULL UNIQUE,
    workspace_path NVARCHAR(MAX),
    clone_depth INT,
    branch_name NVARCHAR(255),
    created_at DATETIME2 NOT NULL DEFAULT GETUTCDATE(),
    updated_at DATETIME2 NOT NULL DEFAULT GETUTCDATE(),
    FOREIGN KEY (ai_task_id) REFERENCES ai_tasks(id) ON DELETE CASCADE
);

-- ================================================================
-- TASK_PATCH TABLE (For storing generated patches)
-- ================================================================
CREATE TABLE task_patches (
    id BIGINT PRIMARY KEY IDENTITY(1,1),
    ai_task_id BIGINT NOT NULL,
    patch_content NVARCHAR(MAX),
    file_path NVARCHAR(MAX),
    created_at DATETIME2 NOT NULL DEFAULT GETUTCDATE(),
    FOREIGN KEY (ai_task_id) REFERENCES ai_tasks(id) ON DELETE CASCADE
);

CREATE INDEX idx_task_patches_task_id ON task_patches(ai_task_id);

-- ================================================================
-- TASK_TEST_RESULT TABLE (For storing test results)
-- ================================================================
CREATE TABLE task_test_results (
    id BIGINT PRIMARY KEY IDENTITY(1,1),
    ai_task_id BIGINT NOT NULL,
    test_name NVARCHAR(500),
    status VARCHAR(50),
    output NVARCHAR(MAX),
    created_at DATETIME2 NOT NULL DEFAULT GETUTCDATE(),
    FOREIGN KEY (ai_task_id) REFERENCES ai_tasks(id) ON DELETE CASCADE
);

CREATE INDEX idx_task_test_results_task_id ON task_test_results(ai_task_id);

-- ================================================================
-- TASK_APPROVAL TABLE (For task review and approval workflow)
-- ================================================================
CREATE TABLE task_approvals (
    id BIGINT PRIMARY KEY IDENTITY(1,1),
    ai_task_id BIGINT NOT NULL UNIQUE,
    approved_by_user_id BIGINT,
    approval_status VARCHAR(50),
    comments NVARCHAR(MAX),
    created_at DATETIME2 NOT NULL DEFAULT GETUTCDATE(),
    updated_at DATETIME2 NOT NULL DEFAULT GETUTCDATE(),
    FOREIGN KEY (ai_task_id) REFERENCES ai_tasks(id) ON DELETE CASCADE,
    FOREIGN KEY (approved_by_user_id) REFERENCES users(id) ON DELETE SET NULL
);

-- ================================================================
-- Schema creation complete
-- ================================================================
-- This schema supports:
-- 1. User authentication and role-based access
-- 2. Candidate and recruiter profiles
-- 3. GitHub OAuth integration
-- 4. Code document storage and RAG
-- 5. AI conversation history
-- 6. Async task execution and monitoring
-- 7. Code analysis results
-- ================================================================
