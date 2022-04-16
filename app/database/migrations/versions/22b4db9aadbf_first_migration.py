"""first migration

Revision ID: 22b4db9aadbf
Revises: 
Create Date: 2022-04-15 22:44:37.512266

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '22b4db9aadbf'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('usermodel',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('email', sa.String(length=120), nullable=False),
    sa.Column('password', sa.String(length=255), nullable=False),
    sa.Column('full_name', sa.String(length=200), nullable=True),
    sa.Column('username', sa.String(length=200), nullable=False),
    sa.Column('document_number', sa.String(length=14), nullable=False),
    sa.Column('phone', sa.String(length=13), nullable=True),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('document_number')
    )
    op.create_index(op.f('ix_usermodel_email'), 'usermodel', ['email'], unique=True)
    op.create_index(op.f('ix_usermodel_username'), 'usermodel', ['username'], unique=True)
    op.create_table('predictionmodel',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('prediction_key', sa.String(length=36), nullable=False),
    sa.Column('text_message', sa.String(length=360), nullable=False),
    sa.Column('prediction', sa.Integer(), nullable=True),
    sa.Column('owner_id', sa.Integer(), nullable=True),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.ForeignKeyConstraint(['owner_id'], ['usermodel.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('prediction_key'),
    sa.UniqueConstraint('text_message')
    )
    op.create_index(op.f('ix_predictionmodel_created_at'), 'predictionmodel', ['created_at'], unique=False)
    op.create_index(op.f('ix_predictionmodel_id'), 'predictionmodel', ['id'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_predictionmodel_id'), table_name='predictionmodel')
    op.drop_index(op.f('ix_predictionmodel_created_at'), table_name='predictionmodel')
    op.drop_table('predictionmodel')
    op.drop_index(op.f('ix_usermodel_username'), table_name='usermodel')
    op.drop_index(op.f('ix_usermodel_email'), table_name='usermodel')
    op.drop_table('usermodel')
    # ### end Alembic commands ###