-- Add execution tracking fields to ai_tasks table
ALTER TABLE ai_tasks ADD execution_start_time DATETIME2 NULL;
ALTER TABLE ai_tasks ADD execution_end_time DATETIME2 NULL;
ALTER TABLE ai_tasks ADD error_message NVARCHAR(MAX) NULL;
