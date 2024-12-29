"""initial migration

Revision ID: 26fd97ce915b
Revises: 
Create Date: 2024-12-28 02:40:46.407819

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '26fd97ce915b'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # Create the `events` table
    op.create_table(
        'events',
        sa.Column('id', sa.Integer, primary_key=True, index=True),
        sa.Column('description', sa.String, nullable=False),
        sa.Column('time', sa.DateTime, nullable=False),
    )

def downgrade():
    # Drop the `events` table
    op.drop_table('events')
