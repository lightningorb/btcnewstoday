"""add date to article

Revision ID: d663013bd4a9
Revises: 9c67e9723d05
Create Date: 2022-11-10 12:53:52.940780

"""
from alembic import op
import sqlalchemy as sa
import sqlmodel # added



# revision identifiers, used by Alembic.
revision = 'd663013bd4a9'
down_revision = '9c67e9723d05'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('article', sa.Column('date', sa.Integer(), nullable=True))
    op.create_index(op.f('ix_article_date'), 'article', ['date'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_article_date'), table_name='article')
    op.drop_column('article', 'date')
    # ### end Alembic commands ###
