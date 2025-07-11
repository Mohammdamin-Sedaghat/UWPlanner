"""fixed coop removal...?

Revision ID: 6adf1dc2fcf3
Revises: ef5ae93aa188
Create Date: 2025-06-29 18:36:49.241957

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6adf1dc2fcf3'
down_revision = 'ef5ae93aa188'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.add_column(sa.Column('coop', sa.Boolean(), server_default=sa.text('True'), nullable=False))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.drop_column('coop')

    # ### end Alembic commands ###
