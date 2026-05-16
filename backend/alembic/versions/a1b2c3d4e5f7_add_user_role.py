"""add_user_role

Revision ID: a1b2c3d4e5f7
Revises: a1b2c3d4e5f6
Create Date: 2026-05-14 15:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


revision = 'a1b2c3d4e5f7'
down_revision = 'a1b2c3d4e5f6'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Aggiungi colonna username
    op.add_column('users', sa.Column('username', sa.String(), nullable=True))
    
    # Aggiungi colonna role
    op.add_column('users', sa.Column('role', sa.String(), nullable=True, server_default='observer'))
    
    # Rendi email nullable
    op.alter_column('users', 'email',
               existing_type=sa.String(),
               nullable=True)
    
    # Crea indice su username
    op.create_unique_constraint('uq_users_username', 'users', ['username'])
    op.create_index(op.f('ix_users_username'), 'users', ['username'], unique=True)


def downgrade() -> None:
    op.drop_index(op.f('ix_users_username'), table_name='users')
    op.drop_constraint('uq_users_username', 'users', type_='unique')
    op.alter_column('users', 'email',
               existing_type=sa.String(),
               nullable=False)
    op.drop_column('users', 'role')
    op.drop_column('users', 'username')