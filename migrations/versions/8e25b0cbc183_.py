"""empty message

Revision ID: 8e25b0cbc183
Revises: d24d61a0c751
Create Date: 2021-11-08 10:07:11.571543

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8e25b0cbc183'
down_revision = 'd24d61a0c751'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('item', sa.Column('img', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('item', 'img')
    # ### end Alembic commands ###