"""empty message

Revision ID: 214dc7418373
Revises: 6ba4ce924e17
Create Date: 2018-08-31 19:20:23.243443

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '214dc7418373'
down_revision = '6ba4ce924e17'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('actions', sa.Column('checked', sa.Boolean(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('actions', 'checked')
    # ### end Alembic commands ###
