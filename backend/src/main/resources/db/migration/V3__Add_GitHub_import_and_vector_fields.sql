-- V3: Add GitHub import and vector fields

-- Add import tracking fields to projects
ALTER TABLE projects ADD import_status NVARCHAR(50) NULL;
ALTER TABLE projects ADD import_id NVARCHAR(255) NULL;

-- Add vector ID field to code_chunks for Qdrant reference
ALTER TABLE code_chunks ADD vector_id NVARCHAR(255) NULL;
