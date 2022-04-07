"""empty message

Revision ID: 0d3478ecd025
Revises: 6edea356615b
Create Date: 2022-04-07 19:54:46.605392

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0d3478ecd025'
down_revision = '6edea356615b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('predictionmodel',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('prediction_key', sa.String(length=36), nullable=False),
    sa.Column('text_message', sa.String(length=360), nullable=False),
    sa.Column('prediction', sa.Integer(), nullable=True),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
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
    # ### end Alembic commands ###
