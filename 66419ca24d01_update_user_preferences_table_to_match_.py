"""Update user_preferences table to match models.py

Revision ID: 66419ca24d01
Revises: 634a8a7a9c98
Create Date: 2025-08-13 00:28:14.579634

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '66419ca24d01'
down_revision: Union[str, Sequence[str], None] = '634a8a7a9c98'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    # Drop existing columns
    op.drop_column('user_preferences', 'user_id')
    op.drop_column('user_preferences', 'preferences')

    # Add new columns
    op.add_column('user_preferences', sa.Column('name', sa.String(), nullable=False))
    op.add_column('user_preferences', sa.Column('job_title', sa.String(), nullable=False))
    op.add_column('user_preferences', sa.Column('location', sa.String(), nullable=False))
    op.add_column('user_preferences', sa.Column('skills', sa.String(), nullable=False))
    op.add_column('user_preferences', sa.Column('whatsapp_number', sa.String(), nullable=False))

def downgrade():
    # Reverse the changes (for downgrading)
    op.add_column('user_preferences', sa.Column('user_id', sa.String(length=50)))
    op.add_column('user_preferences', sa.Column('preferences', sa.Text()))

    op.drop_column('user_preferences', 'name')
    op.drop_column('user_preferences', 'job_title')
    op.drop_column('user_preferences', 'location')
    op.drop_column('user_preferences', 'skills')
    op.drop_column('user_preferences', 'whatsapp_number')