"""cazzata_date_to_datetime

Revision ID: a1b2c3d4e5f6
Revises: 102c6d5855e9
Create Date: 2026-05-14 13:20:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a1b2c3d4e5f6'
down_revision = '102c6d5855e9'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.alter_column('cazzate', 'date',
               existing_type=sa.Date(),
               type_=sa.DateTime(),
               existing_nullable=False,
               postgresql_using='date::timestamp')


def downgrade() -> None:
    op.alter_column('cazzate', 'date',
               existing_type=sa.DateTime(),
               type_=sa.Date(),
               existing_nullable=False,
               postgresql_using='date::date')
