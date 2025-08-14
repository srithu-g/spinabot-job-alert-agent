"""Create enhanced tables for authentication and resume storage

Revision ID: enhanced_tables_v2
Revises: 66419ca24d01
Create Date: 2024-01-01 12:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'enhanced_tables_v2'
down_revision = '66419ca24d01'
branch_labels = None
depends_on = None

def upgrade():
    # Create users table
    op.create_table('users',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=100), nullable=False),
        sa.Column('email', sa.String(length=100), nullable=False),
        sa.Column('password_hash', sa.String(length=255), nullable=False),
        sa.Column('linkedin_url', sa.String(length=255), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_users_email'), 'users', ['email'], unique=True)
    op.create_index(op.f('ix_users_id'), 'users', ['id'], unique=False)

    # Drop old user_preferences table and recreate with new structure
    op.drop_table('user_preferences')
    
    op.create_table('user_preferences',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('job_title', sa.String(length=100), nullable=False),
        sa.Column('location', sa.String(length=100), nullable=False),
        sa.Column('skills', sa.Text(), nullable=False),
        sa.Column('preferred_companies', sa.Text(), nullable=True),
        sa.Column('whatsapp_number', sa.String(length=20), nullable=True),
        sa.Column('linkedin_url', sa.String(length=255), nullable=True),
        sa.Column('email', sa.String(length=100), nullable=True),
        sa.Column('resume_filename', sa.String(length=255), nullable=True),
        sa.Column('resume_data', sa.LargeBinary(), nullable=True),
        sa.Column('resume_content', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_user_preferences_id'), 'user_preferences', ['id'], unique=False)

    # Update job_listings table with new columns
    op.add_column('job_listings', sa.Column('application_url', sa.String(length=500), nullable=True))
    op.add_column('job_listings', sa.Column('salary_range', sa.String(length=100), nullable=True))
    op.add_column('job_listings', sa.Column('job_type', sa.String(length=50), nullable=True))
    op.add_column('job_listings', sa.Column('experience_level', sa.String(length=50), nullable=True))
    op.add_column('job_listings', sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True))

def downgrade():
    # Remove new columns from job_listings
    op.drop_column('job_listings', 'created_at')
    op.drop_column('job_listings', 'experience_level')
    op.drop_column('job_listings', 'job_type')
    op.drop_column('job_listings', 'salary_range')
    op.drop_column('job_listings', 'application_url')

    # Drop user_preferences table
    op.drop_index(op.f('ix_user_preferences_id'), table_name='user_preferences')
    op.drop_table('user_preferences')

    # Drop users table
    op.drop_index(op.f('ix_users_id'), table_name='users')
    op.drop_index(op.f('ix_users_email'), table_name='users')
    op.drop_table('users')
