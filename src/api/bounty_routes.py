import arrow
from sqlmodel import select
from fastapi import APIRouter, Depends
from auth_helpers import get_current_active_user
from db import get_session, Session
from models import Tweet, User, NostrNote, BountyRates, BountyRatesRead
from sqlalchemy import func

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
