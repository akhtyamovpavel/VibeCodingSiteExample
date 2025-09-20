"""create courses topics assignments

Revision ID: 622a3a0b0cc2
Revises: None
Create Date: 2025-09-20 21:43:40.905485

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '622a3a0b0cc2'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        'courses',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('title', sa.String(length=200), nullable=False),
        sa.Column('description', sa.Text(), nullable=False),
        sa.Column('duration_hours', sa.Integer(), nullable=True, server_default=sa.text('0')),
        sa.Column('difficulty_level', sa.String(length=50), nullable=True, server_default=sa.text("'beginner'")),
        sa.Column('created_at', sa.DateTime(), nullable=True, server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(), nullable=True, server_default=sa.func.now()),
    )
    op.create_index(op.f('ix_courses_id'), 'courses', ['id'], unique=False)

    op.create_table(
        'topics',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('title', sa.String(length=200), nullable=False),
        sa.Column('description', sa.Text(), nullable=False),
        sa.Column('content', sa.Text(), nullable=False),
        sa.Column('order_index', sa.Integer(), nullable=True, server_default=sa.text('0')),
        sa.Column('duration_minutes', sa.Integer(), nullable=True, server_default=sa.text('0')),
        sa.Column('course_id', sa.Integer(), sa.ForeignKey('courses.id'), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=True, server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(), nullable=True, server_default=sa.func.now()),
    )
    op.create_index(op.f('ix_topics_id'), 'topics', ['id'], unique=False)

    op.create_table(
        'assignments',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('title', sa.String(length=200), nullable=False),
        sa.Column('description', sa.Text(), nullable=False),
        sa.Column('instructions', sa.Text(), nullable=False),
        sa.Column('difficulty_level', sa.String(length=50), nullable=True, server_default=sa.text("'easy'")),
        sa.Column('estimated_hours', sa.Integer(), nullable=True, server_default=sa.text('1')),
        sa.Column('is_required', sa.Boolean(), nullable=True, server_default=sa.text('1')),
        sa.Column('topic_id', sa.Integer(), sa.ForeignKey('topics.id'), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=True, server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(), nullable=True, server_default=sa.func.now()),
    )
    op.create_index(op.f('ix_assignments_id'), 'assignments', ['id'], unique=False)


def downgrade() -> None:
    op.drop_index(op.f('ix_assignments_id'), table_name='assignments')
    op.drop_table('assignments')
    op.drop_index(op.f('ix_topics_id'), table_name='topics')
    op.drop_table('topics')
    op.drop_index(op.f('ix_courses_id'), table_name='courses')
    op.drop_table('courses')
