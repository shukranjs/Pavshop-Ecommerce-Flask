"""empty message

Revision ID: 3223cbbc9ca8
Revises: 95daaf68d1d2
Create Date: 2021-06-09 04:14:32.014112

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3223cbbc9ca8'
down_revision = '95daaf68d1d2'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('userpost', schema=None) as batch_op:
        batch_op.alter_column('author',
               existing_type=sa.INTEGER(),
               nullable=True)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('userpost', schema=None) as batch_op:
        batch_op.alter_column('author',
               existing_type=sa.INTEGER(),
               nullable=False)

    # ### end Alembic commands ###