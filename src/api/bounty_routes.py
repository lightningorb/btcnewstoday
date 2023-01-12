from slowapi import Limiter, _rate_limit_exceeded_handler
from limiter import *
import arrow
from typing import List
from sqlmodel import select
from fastapi import APIRouter, Depends
from auth_helpers import get_current_active_user
from db import get_session, Session
from fastapi import FastAPI, Request
from fastapi import Depends, FastAPI, HTTPException, status
from models import Tweet, User, NostrNote, BountyRates, BountyRatesRead, Withdrawal
from auth_routes import read_users_me
from sqlalchemy import func
from nameko.standalone.rpc import ClusterRpcProxy
from nameko.constants import AMQP_URI_CONFIG_KEY
import json

config = {
    AMQP_URI_CONFIG_KEY: "pyamqp://btcnewstoday:abc_abc_123_abc_abc_123-abc_abc_123@bndev-us-east-2.link"
}


router = APIRouter()


@router.get("/api/bounty/")
def bounty(
    article_id: int,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_active_user),
):
    midnight = int(
        arrow.utcnow().replace(hour=0, minute=0, second=0, microsecond=0).timestamp()
    )
    num_items = lambda x: session.exec(
        select(func.count(x.id)).where(x.article_id == article_id, x.approved == True)
    ).one()
    num_my_items_today = lambda x: session.exec(
        select(func.count(x.id)).where(
            x.contributor_username == current_user.username,
            x.date > midnight,
            x.approved == True,
        )
    ).one()

    sats_for_note = num_my_items_today(NostrNote) == 0
    sats_for_tweet = num_my_items_today(Tweet) == 0
    sats_for_today = sats_for_tweet == sats_for_note == True
    sats_for_note &= sats_for_today
    sats_for_tweet &= sats_for_today

    return dict(
        sats_for_tweet=sats_for_tweet,
        sats_for_note=sats_for_note,
        can_add_tweet=num_items(Tweet) < 25,
        can_add_note=num_items(NostrNote) < 25,
        note_bounty=100 * sats_for_note,
        tweet_bounty=100 * sats_for_tweet,
    )


@router.get("/api/bounty/rates/", response_model=BountyRatesRead)
def bounty_rates(session: Session = Depends(get_session)):
    return session.exec(select(BountyRates).order_by(BountyRates.date.desc())).one()


@router.get("/api/bounty/withdrawals/", response_model=List[Withdrawal])
def withdrawals(
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_active_user),
):
    return session.exec(
        select(Withdrawal)
        .where(Withdrawal.username == current_user.username)
        .order_by(Withdrawal.date.desc())
    ).all()


@router.post("/api/bounty/withdraw/")
@limiter.limit("1/minute")
def withdraw(
    request: Request,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_active_user),
):
    me = read_users_me(session=session, current_user=current_user)
    # for x in session.exec(select(Withdrawal)).all():
    # session.delete(x)
    session.commit()

    tweets = session.exec(
        select(Tweet).where(
            Tweet.contributor_username == current_user.username,
            Tweet.approved == True,
            Tweet.bounty_paid == False,
        )
    ).all()
    notes = session.exec(
        select(NostrNote).where(
            NostrNote.contributor_username == current_user.username,
            NostrNote.approved == True,
            NostrNote.bounty_paid == False,
        )
    ).all()
    total = sum([x.bounty_sats for x in tweets]) + sum([x.bounty_sats for x in notes])
    assert total == me.redeemable_sats
    wd = Withdrawal(
        username=current_user.username,
        ln_address=current_user.ln_address,
        notes=[x.id for x in notes],
        tweets=[x.id for x in tweets],
        amount_msat=f"{total * 1000}",
        amount_sent_msat="",
        api_version="",
        created_at=0,
        destination="",
        msatoshi=total * 1000,
        msatoshi_sent=0,
        parts=0,
        payment_hash="",
        payment_preimage="",
        status="New",
        date=arrow.utcnow().timestamp(),
    )
    for t in tweets:
        for _ in (
            session.query(Withdrawal).filter(Withdrawal.tweets.contains([t.id])).all()
        ):
            raise HTTPException(
                status_code=400,
                detail=f"Tweet: {t.id} has already been processed",
            )
    for n in notes:
        for _ in session.query(Withdrawal).filter(Withdrawal.notes.contains([n.id])):
            raise HTTPException(
                status_code=400,
                detail=f"Note: {n.id} has already been processed",
            )
    session.add(wd)
    session.commit()
    obj = wd.as_dict()
    obj["tweets"] = list(obj["tweets"])
    obj["notes"] = list(obj["notes"])
    obj = json.dumps(obj)
    if total:
        with ClusterRpcProxy(config) as p:
            print("p.withdraw.withdraw.call_async(data=obj)")
            p.withdraw.withdraw.call_async(data=obj)
            print("done")
            wd.status = "Queued"
            session.commit()
