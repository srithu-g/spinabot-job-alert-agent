"""Add url column to job_listings table

Revision ID: 50feb01be51c
Revises: 66419ca24d01
Create Date: 2025-08-13 14:06:43.071356

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '50feb01be51c'
down_revision: Union[str, Sequence[str], None] = '66419ca24d01'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.add_column('job_listings', sa.Column('url', sa.String()))

def downgrade():
    op.drop_column('job_listings', 'url')
