"""migrate commit

Revision ID: 2a3e57505158
Revises: 49a05be7fb9f
Create Date: 2025-06-21 19:20:32.079175

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2a3e57505158'
down_revision = '49a05be7fb9f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('sequences', schema=None) as batch_op:
        batch_op.add_column(sa.Column('plan', sa.String(), nullable=False))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('sequences', schema=None) as batch_op:
        batch_op.drop_column('plan')

    # ### end Alembic commands ###
