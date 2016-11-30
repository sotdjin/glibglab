"""empty message

Revision ID: 820e7b056cec
Revises: 956c8d4aa9d4
Create Date: 2016-11-26 02:03:50.143809

"""

# revision identifiers, used by Alembic.
revision = '820e7b056cec'
down_revision = '956c8d4aa9d4'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint(None, 'users', ['email'])
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'users', type_='unique')
    ### end Alembic commands ###
