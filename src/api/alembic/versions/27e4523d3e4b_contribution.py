"""contribution

Revision ID: f8bd1b743640
Revises: f8bd1b743640
Create Date: 2022-12-28 14:57:36.950298

"""
from alembic import op
import sqlalchemy as sa
import sqlmodel  # added


# revision identifiers, used by Alembic.
revision = "f8bd1b743640"
down_revision = ""
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "nostrnote",
        sa.Column(
            "contributor_username", sqlmodel.sql.sqltypes.AutoString(), nullable=True
        ),
    )
    op.add_column("nostrnote", sa.Column("bounty_sats", sa.Integer(), nullable=True))
    op.add_column("nostrnote", sa.Column("bounty_paid", sa.Boolean(), nullable=True))
    op.create_index(
        op.f("ix_nostrnote_contributor_username"),
        "nostrnote",
        ["contributor_username"],
        unique=False,
    )
    op.create_foreign_key(
        None, "nostrnote", "user", ["contributor_username"], ["username"]
    )
    op.add_column(
        "tweet",
        sa.Column(
            "contributor_username", sqlmodel.sql.sqltypes.AutoString(), nullable=True
        ),
    )
    op.add_column("tweet", sa.Column("bounty_sats", sa.Integer(), nullable=True))
    op.add_column("tweet", sa.Column("bounty_paid", sa.Boolean(), nullable=True))
    op.create_index(
        op.f("ix_tweet_contributor_username"),
        "tweet",
        ["contributor_username"],
        unique=False,
    )
    op.create_foreign_key(None, "tweet", "user", ["contributor_username"], ["username"])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, "tweet", type_="foreignkey")
    op.drop_index(op.f("ix_tweet_contributor_username"), table_name="tweet")
    op.drop_column("tweet", "bounty_paid")
    op.drop_column("tweet", "bounty_sats")
    op.drop_column("tweet", "contributor_username")
    op.drop_constraint(None, "nostrnote", type_="foreignkey")
    op.drop_index(op.f("ix_nostrnote_contributor_username"), table_name="nostrnote")
    op.drop_column("nostrnote", "bounty_paid")
    op.drop_column("nostrnote", "bounty_sats")
    op.drop_column("nostrnote", "contributor_username")
    # ### end Alembic commands ###