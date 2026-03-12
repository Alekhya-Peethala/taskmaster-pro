"""
Create tasks table

Revision ID: 001_create_tasks
Revises: 
Create Date: 2026-03-12

TaskMaster Pro - Initial Database Migration
Generated with GitHub Copilot assistance
Creates tasks table with all fields, constraints, and indexes
"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic
revision = '001_create_tasks'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    """
    Upgrade database schema: Create tasks table
    """
    op.create_table(
        'tasks',
        # Primary Key
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        
        # Core Fields
        sa.Column('title', sa.String(length=255), nullable=False),
        sa.Column('description', sa.String(length=65535), nullable=False),
        sa.Column('due_date', sa.Date(), nullable=False),
        sa.Column('priority', sa.String(length=50), nullable=False),
        sa.Column('status', sa.String(length=50), nullable=False),
        
        # Reminder Field
        sa.Column('reminder_sent', sa.Boolean(), nullable=False, server_default='0'),
        
        # Audit Fields
        sa.Column(
            'created_at',
            sa.TIMESTAMP(),
            server_default=sa.text('CURRENT_TIMESTAMP'),
            nullable=False
        ),
        sa.Column(
            'updated_at',
            sa.TIMESTAMP(),
            server_default=sa.text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'),
            nullable=False
        ),
        
        # Primary Key Constraint
        sa.PrimaryKeyConstraint('id'),
        
        # Check Constraints
        sa.CheckConstraint(
            "priority IN ('Low', 'Medium', 'High')",
            name='check_priority_values'
        ),
        sa.CheckConstraint(
            "status IN ('Pending', 'In Progress', 'Completed')",
            name='check_status_values'
        ),
        
        # MySQL Engine and Charset
        mysql_engine='InnoDB',
        mysql_charset='utf8mb4',
        mysql_collate='utf8mb4_unicode_ci'
    )
    
    # Create Performance Indexes (from data-model.md)
    op.create_index('idx_status', 'tasks', ['status'])
    op.create_index('idx_due_date', 'tasks', ['due_date'])
    op.create_index('idx_status_due_date', 'tasks', ['status', 'due_date'])
    op.create_index('idx_reminder_due', 'tasks', ['reminder_sent', 'due_date'])


def downgrade() -> None:
    """
    Downgrade database schema: Drop tasks table
    """
    op.drop_index('idx_reminder_due', table_name='tasks')
    op.drop_index('idx_status_due_date', table_name='tasks')
    op.drop_index('idx_due_date', table_name='tasks')
    op.drop_index('idx_status', table_name='tasks')
    op.drop_table('tasks')
