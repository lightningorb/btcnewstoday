"""bounties

Revision ID: 3118f5b55715
Revises: f8bd1b743640
Create Date: 2023-01-06 12:40:42.203244

"""
from alembic import op
import sqlalchemy as sa
import sqlmodel # added



# revision identifiers, used by Alembic.
revision = '3118f5b55715'
down_revision = 'f8bd1b743640'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('bountyrates',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('notes', sa.Integer(), nullable=False),
    sa.Column('tweets', sa.Integer(), nullable=False),
    sa.Column('date', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_bountyrates_date'), 'bountyrates', ['date'], unique=False)
    op.drop_index('ix_articledeleted_link', table_name='articledeleted')
    op.drop_table('articledeleted')
    op.add_column('nostrnote', sa.Column('contributor_username', sqlmodel.sql.sqltypes.AutoString(), nullable=True))
    op.add_column('nostrnote', sa.Column('approved', sa.Boolean(), nullable=True))
    op.add_column('nostrnote', sa.Column('bounty_sats', sa.Integer(), nullable=True))
    op.add_column('nostrnote', sa.Column('bounty_paid', sa.Boolean(), nullable=True))
    op.add_column('nostrnote', sa.Column('date', sa.Integer(), nullable=True))
    op.drop_index('ix_nostrnote_author_pk', table_name='nostrnote')
    op.create_index(op.f('ix_nostrnote_approved'), 'nostrnote', ['approved'], unique=False)
    op.create_index(op.f('ix_nostrnote_contributor_username'), 'nostrnote', ['contributor_username'], unique=False)
    op.create_index(op.f('ix_nostrnote_date'), 'nostrnote', ['date'], unique=False)
    op.create_foreign_key(None, 'nostrnote', 'user', ['contributor_username'], ['username'])
    op.drop_column('nostrnote', 'author_pk')
    op.add_column('tweet', sa.Column('tweet_id', sa.BigInteger(), autoincrement=False, nullable=True))
    op.add_column('tweet', sa.Column('contributor_username', sqlmodel.sql.sqltypes.AutoString(), nullable=True))
    op.add_column('tweet', sa.Column('approved', sa.Boolean(), nullable=True))
    op.add_column('tweet', sa.Column('bounty_sats', sa.Integer(), nullable=True))
    op.add_column('tweet', sa.Column('bounty_paid', sa.Boolean(), nullable=True))
    op.add_column('tweet', sa.Column('date', sa.Integer(), nullable=True))
    op.create_index(op.f('ix_tweet_approved'), 'tweet', ['approved'], unique=False)
    op.create_index(op.f('ix_tweet_contributor_username'), 'tweet', ['contributor_username'], unique=False)
    op.create_index(op.f('ix_tweet_date'), 'tweet', ['date'], unique=False)
    op.create_foreign_key(None, 'tweet', 'user', ['contributor_username'], ['username'])
    op.add_column('user', sa.Column('ln_address', sqlmodel.sql.sqltypes.AutoString(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user', 'ln_address')
    op.drop_constraint(None, 'tweet', type_='foreignkey')
    op.drop_index(op.f('ix_tweet_date'), table_name='tweet')
    op.drop_index(op.f('ix_tweet_contributor_username'), table_name='tweet')
    op.drop_index(op.f('ix_tweet_approved'), table_name='tweet')
    op.drop_column('tweet', 'date')
    op.drop_column('tweet', 'bounty_paid')
    op.drop_column('tweet', 'bounty_sats')
    op.drop_column('tweet', 'approved')
    op.drop_column('tweet', 'contributor_username')
    op.drop_column('tweet', 'tweet_id')
    op.add_column('nostrnote', sa.Column('author_pk', sa.VARCHAR(), autoincrement=False, nullable=False))
    op.drop_constraint(None, 'nostrnote', type_='foreignkey')
    op.drop_index(op.f('ix_nostrnote_date'), table_name='nostrnote')
    op.drop_index(op.f('ix_nostrnote_contributor_username'), table_name='nostrnote')
    op.drop_index(op.f('ix_nostrnote_approved'), table_name='nostrnote')
    op.create_index('ix_nostrnote_author_pk', 'nostrnote', ['author_pk'], unique=False)
    op.drop_column('nostrnote', 'date')
    op.drop_column('nostrnote', 'bounty_paid')
    op.drop_column('nostrnote', 'bounty_sats')
    op.drop_column('nostrnote', 'approved')
    op.drop_column('nostrnote', 'contributor_username')
    op.create_table('articledeleted',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('link', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.PrimaryKeyConstraint('id', name='articledeleted_pkey')
    )
    op.create_index('ix_articledeleted_link', 'articledeleted', ['link'], unique=False)
    op.drop_index(op.f('ix_bountyrates_date'), table_name='bountyrates')
    op.drop_table('bountyrates')
    # ### end Alembic commands ###
