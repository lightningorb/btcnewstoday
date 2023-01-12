import json
from nameko.rpc import rpc
from nameko.standalone.rpc import ClusterRpcProxy
from nameko.constants import AMQP_URI_CONFIG_KEY

from sqlmodel import Field, Session, SQLModel, create_engine, select, delete
import os

from db import *
from models import *

local_engine = create_engine(
    f"postgresql://btcnewstoday:abc_abc_123_abc_abc_123-abc_abc_123@localhost:5432/postgres"
)


class PostWithdrawlService:
    name = "post_withdrawal"

    @rpc
    def withdrawal_done(self, data, payment):
        session = Session(local_engine)
        data = json.loads(data)
        doc = session.exec(select(Withdrawal).where(Withdrawal.id == data["id"])).one()
        doc.status = data["status"]
        session.commit()
        if payment:
            payment = json.loads(payment)
            doc.amount_sent_msat = payment["amount_sent_msat"]
            doc.api_version = payment["api_version"]
            doc.created_at = payment["created_at"]
            doc.destination = payment["destination"]
            doc.msatoshi = payment["msatoshi"]
            doc.msatoshi_sent = payment["msatoshi_sent"]
            doc.parts = payment["parts"]
            doc.payment_hash = payment["payment_hash"]
            doc.payment_preimage = payment["payment_preimage"]
            for t in data["tweets"]:
                session.exec(
                    select(Tweet).where(Tweet.id == t)
                ).one().bounty_paid = True
            for t in data["notes"]:
                session.exec(
                    select(NostrNote).where(NostrNote.id == t)
                ).one().bounty_paid = True
        session.commit()
