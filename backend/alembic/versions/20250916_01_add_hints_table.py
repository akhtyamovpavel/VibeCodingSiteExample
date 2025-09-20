"""add hints table

Revision ID: 20250916_01_add_hints_table
Revises: 
Create Date: 2025-09-16 00:00:00
"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '20250916_01_add_hints_table'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        'hints',
        sa.Column('id', sa.Integer(), primary_key=True, index=True),
        sa.Column('assignment_id', sa.Integer(), sa.ForeignKey('assignments.id', ondelete='CASCADE'), nullable=False),
        sa.Column('order_index', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('text', sa.Text(), nullable=False),
        sa.Column('penalty', sa.Integer(), nullable=False, server_default='10'),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.text('(CURRENT_TIMESTAMP)')),
        sa.Column('updated_at', sa.DateTime(), nullable=False, server_default=sa.text('(CURRENT_TIMESTAMP)')),
    )
    op.create_index('ix_hints_assignment_order', 'hints', ['assignment_id', 'order_index'], unique=True)


def downgrade() -> None:
    op.drop_index('ix_hints_assignment_order', table_name='hints')
    op.drop_table('hints')


