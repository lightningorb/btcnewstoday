"""withdrawals

Revision ID: 4973e47de740
Revises: 3118f5b55715
Create Date: 2023-01-11 06:48:53.506273

"""
from alembic import op
import sqlalchemy as sa
import sqlmodel # added

from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '4973e47de740'
down_revision = '3118f5b55715'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('withdrawal',
    sa.Column('notes', postgresql.ARRAY(sa.BigInteger()), nullable=True),
    sa.Column('tweets', postgresql.ARRAY(sa.BigInteger()), nullable=True),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sqlmodel.sql.sqltypes.AutoString(), nullable=True),
    sa.Column('ln_address', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('date', sa.Integer(), nullable=False),
    sa.Column('amount_msat', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('amount_sent_msat', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('api_version', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('created_at', sa.Integer(), nullable=False),
    sa.Column('destination', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('msatoshi', sa.Integer(), nullable=False),
    sa.Column('msatoshi_sent', sa.Integer(), nullable=False),
    sa.Column('parts', sa.Integer(), nullable=False),
    sa.Column('payment_hash', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('payment_preimage', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('status', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.ForeignKeyConstraint(['username'], ['user.username'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_withdrawal_date'), 'withdrawal', ['date'], unique=False)
    op.create_index(op.f('ix_withdrawal_username'), 'withdrawal', ['username'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_withdrawal_username'), table_name='withdrawal')
    op.drop_index(op.f('ix_withdrawal_date'), table_name='withdrawal')
    op.drop_table('withdrawal')
    # ### end Alembic commands ###
