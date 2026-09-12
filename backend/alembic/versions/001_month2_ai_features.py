"""Add Month 2 AI features: projects, files, code documents, chunks, conversations, analyses

Revision ID: 001_month2
Revises: 
Create Date: 2026-09-11 14:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '001_month2'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Create projects table
    op.create_table(
        'projects',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(255), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('github_url', sa.String(500), nullable=True),
        sa.Column('github_repo_name', sa.String(255), nullable=True),
        sa.Column('github_branch', sa.String(100), server_default='main'),
        sa.Column('github_token_id', sa.Integer(), nullable=True),
        sa.Column('is_active', sa.Boolean(), server_default='true'),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['github_token_id'], ['github_tokens.id'], ondelete='SET NULL'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('idx_projects_user_id', 'projects', ['user_id'])
    op.create_index('idx_projects_github_repo_name', 'projects', ['github_repo_name'])

    # Create files table
    op.create_table(
        'files',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('project_id', sa.Integer(), nullable=False),
        sa.Column('path', sa.String(500), nullable=False),
        sa.Column('filename', sa.String(255), nullable=False),
        sa.Column('file_size', sa.Integer(), nullable=True),
        sa.Column('content_hash', sa.String(64), nullable=True),
        sa.Column('language', sa.String(50), nullable=True),
        sa.Column('is_binary', sa.Boolean(), server_default='false'),
        sa.Column('last_synced_at', sa.DateTime(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['project_id'], ['projects.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('idx_files_project_id', 'files', ['project_id'])
    op.create_index('idx_files_path', 'files', ['path'])
    op.create_index('idx_files_content_hash', 'files', ['content_hash'])

    # Create github_tokens table
    op.create_table(
        'github_tokens',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('access_token', sa.Text(), nullable=False),
        sa.Column('refresh_token', sa.Text(), nullable=True),
        sa.Column('token_type', sa.String(50), server_default='Bearer'),
        sa.Column('scope', sa.String(500), nullable=True),
        sa.Column('expires_at', sa.DateTime(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('idx_github_tokens_user_id', 'github_tokens', ['user_id'])

    # Create code_documents table
    op.create_table(
        'code_documents',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('project_id', sa.Integer(), nullable=False),
        sa.Column('file_id', sa.Integer(), nullable=True),
        sa.Column('path', sa.String(500), nullable=False),
        sa.Column('language', sa.String(50), nullable=False),
        sa.Column('content_hash', sa.String(64), nullable=False),
        sa.Column('file_size', sa.Integer(), nullable=True),
        sa.Column('chunk_count', sa.Integer(), server_default='0'),
        sa.Column('indexed_at', sa.DateTime(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['project_id'], ['projects.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['file_id'], ['files.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('idx_code_documents_project_id', 'code_documents', ['project_id'])
    op.create_index('idx_code_documents_path', 'code_documents', ['path'])
    op.create_index('idx_code_documents_content_hash', 'code_documents', ['content_hash'])

    # Create code_chunks table (will use pgvector for embedding column)
    op.create_table(
        'code_chunks',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('document_id', sa.Integer(), nullable=False),
        sa.Column('project_id', sa.Integer(), nullable=False),
        sa.Column('chunk_index', sa.Integer(), nullable=False),
        sa.Column('content', sa.Text(), nullable=False),
        sa.Column('start_line', sa.Integer(), nullable=False),
        sa.Column('end_line', sa.Integer(), nullable=False),
        sa.Column('symbol_name', sa.String(255), nullable=True),
        sa.Column('language', sa.String(50), nullable=False),
        sa.Column('embedding_model', sa.String(100), nullable=True),
        sa.Column('token_count', sa.Integer(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['document_id'], ['code_documents.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['project_id'], ['projects.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('idx_code_chunks_document_id', 'code_chunks', ['document_id'])
    op.create_index('idx_code_chunks_project_id', 'code_chunks', ['project_id'])
    op.create_index('idx_code_chunks_symbol_name', 'code_chunks', ['symbol_name'])

    # Add embedding column using pgvector if available, otherwise TEXT
    # We'll add this after pgvector is enabled
    op.add_column('code_chunks', sa.Column('embedding', postgresql.UUID(), nullable=True))

    # Create ai_conversations table
    op.create_table(
        'ai_conversations',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('project_id', sa.Integer(), nullable=False),
        sa.Column('title', sa.String(255), nullable=True),
        sa.Column('context_type', sa.String(50), server_default='repository'),
        sa.Column('context_data', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['project_id'], ['projects.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('idx_ai_conversations_user_id', 'ai_conversations', ['user_id'])
    op.create_index('idx_ai_conversations_project_id', 'ai_conversations', ['project_id'])

    # Create ai_messages table
    op.create_table(
        'ai_messages',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('conversation_id', sa.Integer(), nullable=False),
        sa.Column('role', sa.String(20), nullable=False),
        sa.Column('content', sa.Text(), nullable=False),
        sa.Column('sources', sa.Text(), nullable=True),
        sa.Column('token_count', sa.Integer(), nullable=True),
        sa.Column('model_used', sa.String(100), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['conversation_id'], ['ai_conversations.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('idx_ai_messages_conversation_id', 'ai_messages', ['conversation_id'])

    # Create ai_analyses table
    op.create_table(
        'ai_analyses',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('project_id', sa.Integer(), nullable=False),
        sa.Column('document_id', sa.Integer(), nullable=True),
        sa.Column('analysis_type', sa.String(50), nullable=False),
        sa.Column('target_code', sa.Text(), nullable=True),
        sa.Column('result', sa.Text(), nullable=False),
        sa.Column('severity', sa.String(20), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['project_id'], ['projects.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['document_id'], ['code_documents.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('idx_ai_analyses_project_id', 'ai_analyses', ['project_id'])
    op.create_index('idx_ai_analyses_document_id', 'ai_analyses', ['document_id'])
    op.create_index('idx_ai_analyses_analysis_type', 'ai_analyses', ['analysis_type'])

    # Create repository_index_metadata table
    op.create_table(
        'repository_index_metadata',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('project_id', sa.Integer(), nullable=False),
        sa.Column('status', sa.String(50), server_default='NOT_INDEXED'),
        sa.Column('total_files', sa.Integer(), server_default='0'),
        sa.Column('indexed_files', sa.Integer(), server_default='0'),
        sa.Column('total_chunks', sa.Integer(), server_default='0'),
        sa.Column('last_indexed_at', sa.DateTime(), nullable=True),
        sa.Column('last_error', sa.Text(), nullable=True),
        sa.Column('embedding_model', sa.String(100), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['project_id'], ['projects.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('project_id')
    )
    op.create_index('idx_repository_index_metadata_project_id', 'repository_index_metadata', ['project_id'])
    op.create_index('idx_repository_index_metadata_status', 'repository_index_metadata', ['status'])


def downgrade() -> None:
    op.drop_index('idx_repository_index_metadata_status', table_name='repository_index_metadata')
    op.drop_index('idx_repository_index_metadata_project_id', table_name='repository_index_metadata')
    op.drop_table('repository_index_metadata')

    op.drop_index('idx_ai_analyses_analysis_type', table_name='ai_analyses')
    op.drop_index('idx_ai_analyses_document_id', table_name='ai_analyses')
    op.drop_index('idx_ai_analyses_project_id', table_name='ai_analyses')
    op.drop_table('ai_analyses')

    op.drop_index('idx_ai_messages_conversation_id', table_name='ai_messages')
    op.drop_table('ai_messages')

    op.drop_index('idx_ai_conversations_project_id', table_name='ai_conversations')
    op.drop_index('idx_ai_conversations_user_id', table_name='ai_conversations')
    op.drop_table('ai_conversations')

    op.drop_index('idx_code_chunks_symbol_name', table_name='code_chunks')
    op.drop_index('idx_code_chunks_project_id', table_name='code_chunks')
    op.drop_index('idx_code_chunks_document_id', table_name='code_chunks')
    op.drop_table('code_chunks')

    op.drop_index('idx_code_documents_content_hash', table_name='code_documents')
    op.drop_index('idx_code_documents_path', table_name='code_documents')
    op.drop_index('idx_code_documents_project_id', table_name='code_documents')
    op.drop_table('code_documents')

    op.drop_index('idx_github_tokens_user_id', table_name='github_tokens')
    op.drop_table('github_tokens')

    op.drop_index('idx_files_content_hash', table_name='files')
    op.drop_index('idx_files_path', table_name='files')
    op.drop_index('idx_files_project_id', table_name='files')
    op.drop_table('files')

    op.drop_index('idx_projects_github_repo_name', table_name='projects')
    op.drop_index('idx_projects_user_id', table_name='projects')
    op.drop_table('projects')
