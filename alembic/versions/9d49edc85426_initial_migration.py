"""Initial migration

Revision ID: 9d49edc85426
Revises: 
Create Date: 2024-09-17 22:26:03.451602

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = '9d49edc85426'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Create users table
    op.create_table(
        'users',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('name', sa.String(length=255), nullable=False, unique=True),
        sa.Column('email', sa.String(length=255), nullable=False, unique=True),
        sa.Column('profile_picture', sa.String(length=255)),
        sa.Column('created_at', sa.DateTime(), server_default=sa.func.now()),
        sa.Column('last_login', sa.DateTime())
    )
    
    # Create oauth_providers table
    op.create_table(
        'oauth_providers',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('provider_name', sa.String(length=255), unique=True, nullable=False),
        sa.Column('provider_url', sa.String(length=255), nullable=False)
    )
    
    # Create user_providers table
    op.create_table(
        'user_providers',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('user_id', sa.Integer, sa.ForeignKey('users.id'), nullable=False),
        sa.Column('provider_id', sa.Integer, sa.ForeignKey('oauth_providers.id'), nullable=False),
        sa.Column('provider_user_id', sa.String(length=255), unique=True, nullable=False),
        sa.Column('access_token', sa.Text),
        sa.Column('refresh_token', sa.Text),
        sa.Column('created_at', sa.DateTime(), server_default=sa.func.now())
    )


def downgrade() -> None:
    # Drop user_providers table
    op.drop_table('user_providers')
    
    # Drop oauth_providers table
    op.drop_table('oauth_providers')
    
    # Drop users table
    op.drop_table('users')
