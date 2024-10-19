"""initial migration

Revision ID: 47ff9cca610f
Revises: 
Create Date: 2024-10-19 14:20:30.444590

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '47ff9cca610f'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Create users table
    op.create_table(
        'users',
        sa.Column('id', sa.Integer, primary_key=True, index=True),
        sa.Column('name', sa.String(length=255), unique=True, index=True),
        sa.Column('email', sa.String(length=255), unique=True, index=True),
        sa.Column('password', sa.String),
        sa.Column('profile_picture', sa.String),
        sa.Column('created_at', postgresql.TIMESTAMP(), server_default=sa.text('now()'), nullable=True),
        sa.Column('last_login', postgresql.TIMESTAMP, nullable=True),
    )

    # Create oauth_providers table
    op.create_table(
        'oauth_providers',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('provider_name', sa.String(length=255), nullable=False),
        sa.Column('provider_url', sa.String(length=255), nullable=False),
        sa.UniqueConstraint('provider_name', name='uq_provider_name')
    )

    # Create user_providers table
    op.create_table(
        'user_providers',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('user_id', sa.Integer, sa.ForeignKey('users.id'), nullable=False),
        sa.Column('provider_id', sa.Integer, sa.ForeignKey('oauth_providers.id'), nullable=False),
        sa.Column('provider_user_id', sa.String(length=255), nullable=False),
        sa.Column('access_token', sa.Text, nullable=True),
        sa.Column('refresh_token', sa.Text, nullable=True),
        sa.Column('created_at', postgresql.TIMESTAMP, server_default=sa.text('now()'), nullable=True),
    )

    # Create digit_predictions table
    op.create_table(
        'digit_predictions',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('user_id', sa.Integer, sa.ForeignKey('users.id'), nullable=True),
        sa.Column('uploaded_image', sa.String, nullable=False),
        sa.Column('predicted_digit', sa.Integer, nullable=False),
        sa.Column('confidence', sa.Float, nullable=False),
        sa.Column('created_at', postgresql.TIMESTAMP, server_default=sa.text('now()'), nullable=False),
        sa.Column('status', sa.Integer, nullable=False),
    )


def downgrade() -> None:
    # Drop tables in reverse order of creation
    op.drop_table('digit_predictions')
    op.drop_table('user_providers')
    op.drop_table('oauth_providers')
    op.drop_table('users')
