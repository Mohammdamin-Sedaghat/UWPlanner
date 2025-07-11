"""added faculty to major

Revision ID: f7ba21a80ffc
Revises: 995ec30ba721
Create Date: 2025-06-07 13:01:15.076359

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f7ba21a80ffc'
down_revision = '995ec30ba721'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('major', schema=None) as batch_op:
        batch_op.add_column(sa.Column('faculty', sa.String(), server_default='MATH', nullable=False))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('major', schema=None) as batch_op:
        batch_op.drop_column('faculty')

    # ### end Alembic commands ###
