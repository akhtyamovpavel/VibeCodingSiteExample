"""add hints table

Revision ID: 20250916_01_add_hints_table
Revises: 622a3a0b0cc2
Create Date: 2025-09-16 00:00:00
"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '20250916_01_add_hints_table'
down_revision = '622a3a0b0cc2'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        'hints',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('assignment_id', sa.Integer(), sa.ForeignKey('assignments.id'), nullable=False),
        sa.Column('order_index', sa.Integer(), nullable=True, server_default=sa.text('0')),
        sa.Column('text', sa.Text(), nullable=False),
        sa.Column('penalty', sa.Integer(), nullable=True, server_default=sa.text('10')),
        sa.Column('created_at', sa.DateTime(), nullable=True, server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(), nullable=True, server_default=sa.func.now()),
    )
    op.create_index(op.f('ix_hints_id'), 'hints', ['id'], unique=False)


def downgrade() -> None:
    op.drop_index(op.f('ix_hints_id'), table_name='hints')
    op.drop_table('hints')
