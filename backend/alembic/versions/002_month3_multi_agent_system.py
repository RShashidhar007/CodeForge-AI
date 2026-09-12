"""Add Month 3 Multi-Agent AI Software Engineering System tables

Revision ID: 002_month3
Revises: 001_month2
Create Date: 2026-09-12 10:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '002_month3'
down_revision = '001_month2'
branch_labels = None
depends_on = None


def upgrade() -> None:
    """Create all Month 3 agent system tables."""
    
    # ===== AI Tasks Table =====
    op.create_table(
        'ai_tasks',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('project_id', sa.Integer(), nullable=False),
        sa.Column('title', sa.String(255), nullable=False),
        sa.Column('description', sa.Text(), nullable=False),
        sa.Column('task_type', sa.String(50), nullable=False),
        sa.Column('status', sa.String(50), nullable=False, server_default='QUEUED'),
        sa.Column('current_agent', sa.String(100), nullable=True),
        sa.Column('progress_percent', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(), nullable=False, server_default=sa.func.now()),
        sa.Column('completed_at', sa.DateTime(), nullable=True),
        sa.Column('error_message', sa.Text(), nullable=True),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['project_id'], ['projects.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('idx_ai_tasks_user_id', 'ai_tasks', ['user_id'])
    op.create_index('idx_ai_tasks_project_id', 'ai_tasks', ['project_id'])
    op.create_index('idx_ai_tasks_status', 'ai_tasks', ['status'])
    op.create_index('idx_ai_tasks_task_type', 'ai_tasks', ['task_type'])
    op.create_index('idx_ai_tasks_created_at', 'ai_tasks', ['created_at'])
    
    # ===== Agent Execution History =====
    op.create_table(
        'agent_executions',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('task_id', sa.Integer(), nullable=False),
        sa.Column('agent_name', sa.String(100), nullable=False),
        sa.Column('status', sa.String(50), nullable=False),
        sa.Column('input_summary', sa.Text(), nullable=True),
        sa.Column('output_summary', sa.Text(), nullable=True),
        sa.Column('tool_calls', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('tokens_used', sa.Integer(), nullable=True),
        sa.Column('started_at', sa.DateTime(), nullable=False, server_default=sa.func.now()),
        sa.Column('completed_at', sa.DateTime(), nullable=True),
        sa.Column('duration_seconds', sa.Float(), nullable=True),
        sa.Column('error_message', sa.Text(), nullable=True),
        sa.ForeignKeyConstraint(['task_id'], ['ai_tasks.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('idx_agent_executions_task_id', 'agent_executions', ['task_id'])
    op.create_index('idx_agent_executions_agent_name', 'agent_executions', ['agent_name'])
    op.create_index('idx_agent_executions_status', 'agent_executions', ['status'])
    
    # ===== Task Patches (Proposed Changes) =====
    op.create_table(
        'task_patches',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('task_id', sa.Integer(), nullable=False),
        sa.Column('agent_id', sa.String(100), nullable=True),
        sa.Column('target_files', sa.Text(), nullable=False),  # JSON array
        sa.Column('patch_content', sa.Text(), nullable=False),  # Unified diff
        sa.Column('validation_status', sa.String(50), nullable=False, server_default='PENDING'),
        sa.Column('review_status', sa.String(50), nullable=True),
        sa.Column('review_comments', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.func.now()),
        sa.Column('applied_at', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['task_id'], ['ai_tasks.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('idx_task_patches_task_id', 'task_patches', ['task_id'])
    op.create_index('idx_task_patches_validation_status', 'task_patches', ['validation_status'])
    op.create_index('idx_task_patches_review_status', 'task_patches', ['review_status'])
    
    # ===== Task Approvals =====
    op.create_table(
        'task_approvals',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('task_id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('action', sa.String(50), nullable=False),
        sa.Column('comment', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.func.now()),
        sa.ForeignKeyConstraint(['task_id'], ['ai_tasks.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('idx_task_approvals_task_id', 'task_approvals', ['task_id'])
    op.create_index('idx_task_approvals_user_id', 'task_approvals', ['user_id'])
    
    # ===== Test Results =====
    op.create_table(
        'task_test_results',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('task_id', sa.Integer(), nullable=False),
        sa.Column('execution_number', sa.Integer(), nullable=False),
        sa.Column('test_command', sa.String(255), nullable=False),
        sa.Column('exit_code', sa.Integer(), nullable=False),
        sa.Column('stdout', sa.Text(), nullable=True),
        sa.Column('stderr', sa.Text(), nullable=True),
        sa.Column('duration_seconds', sa.Float(), nullable=True),
        sa.Column('passed_count', sa.Integer(), nullable=True),
        sa.Column('failed_count', sa.Integer(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.func.now()),
        sa.ForeignKeyConstraint(['task_id'], ['ai_tasks.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('idx_task_test_results_task_id', 'task_test_results', ['task_id'])
    op.create_index('idx_task_test_results_execution_number', 'task_test_results', ['execution_number'])
    
    # ===== Task Workspaces (Branch/Container Tracking) =====
    op.create_table(
        'task_workspaces',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('task_id', sa.Integer(), nullable=False),
        sa.Column('workspace_type', sa.String(50), nullable=False),
        sa.Column('workspace_identifier', sa.String(255), nullable=False),
        sa.Column('status', sa.String(50), nullable=False, server_default='CREATED'),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.func.now()),
        sa.Column('cleaned_up_at', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['task_id'], ['ai_tasks.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('idx_task_workspaces_task_id', 'task_workspaces', ['task_id'])
    op.create_index('idx_task_workspaces_status', 'task_workspaces', ['status'])


def downgrade() -> None:
    """Drop all Month 3 agent system tables."""
    
    # Drop in reverse order of creation (respect foreign keys)
    op.drop_index('idx_task_workspaces_status', 'task_workspaces')
    op.drop_index('idx_task_workspaces_task_id', 'task_workspaces')
    op.drop_table('task_workspaces')
    
    op.drop_index('idx_task_test_results_execution_number', 'task_test_results')
    op.drop_index('idx_task_test_results_task_id', 'task_test_results')
    op.drop_table('task_test_results')
    
    op.drop_index('idx_task_approvals_user_id', 'task_approvals')
    op.drop_index('idx_task_approvals_task_id', 'task_approvals')
    op.drop_table('task_approvals')
    
    op.drop_index('idx_task_patches_review_status', 'task_patches')
    op.drop_index('idx_task_patches_validation_status', 'task_patches')
    op.drop_index('idx_task_patches_task_id', 'task_patches')
    op.drop_table('task_patches')
    
    op.drop_index('idx_agent_executions_status', 'agent_executions')
    op.drop_index('idx_agent_executions_agent_name', 'agent_executions')
    op.drop_index('idx_agent_executions_task_id', 'agent_executions')
    op.drop_table('agent_executions')
    
    op.drop_index('idx_ai_tasks_created_at', 'ai_tasks')
    op.drop_index('idx_ai_tasks_task_type', 'ai_tasks')
    op.drop_index('idx_ai_tasks_status', 'ai_tasks')
    op.drop_index('idx_ai_tasks_project_id', 'ai_tasks')
    op.drop_index('idx_ai_tasks_user_id', 'ai_tasks')
    op.drop_table('ai_tasks')
