"""Initial migration

Revision ID: e9cd28f55bad
Revises: 
Create Date: 2025-06-02 20:44:27.549450

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e9cd28f55bad'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('olives',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('country', sa.String(), nullable=False),
    sa.Column('region', sa.String(), nullable=False),
    sa.Column('color', sa.String(), nullable=False),
    sa.Column('rarity', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('producers',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('address', sa.String(), nullable=False),
    sa.Column('capacity', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(), nullable=False),
    sa.Column('_password', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('username')
    )
    op.create_table('oils',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('year', sa.Integer(), nullable=False),
    sa.Column('price', sa.Float(), nullable=False),
    sa.Column('isActive', sa.Boolean(), nullable=False),
    sa.Column('acidity', sa.Float(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('producer_id', sa.Integer(), nullable=False),
    sa.Column('olive_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['olive_id'], ['olives.id'], name=op.f('fk_oils_olive_id_olives')),
    sa.ForeignKeyConstraint(['producer_id'], ['producers.id'], name=op.f('fk_oils_producer_id_producers')),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], name=op.f('fk_oils_user_id_users')),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('oils')
    op.drop_table('users')
    op.drop_table('producers')
    op.drop_table('olives')
    # ### end Alembic commands ###
