from fastapi import APIRouter, Depends
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.content import Content
from app.models.publish_record import PublishRecord, ContentAnalytics
from app.schemas.publish import AnalyticsOut, AnalyticsOverview

router = APIRouter()


# ── Overview ──────────────────────────────────────────────────────────

@router.get("/overview", response_model=AnalyticsOverview)
def get_overview(db: Session = Depends(get_db)):
    total_contents = db.query(Content).count()
    total_published = db.query(PublishRecord).filter(PublishRecord.status == "published").count()

    channel_counts = (
        db.query(PublishRecord.channel, func.count(PublishRecord.id))
        .filter(PublishRecord.status.in_(["published", "draft"]))
        .group_by(PublishRecord.channel)
        .all()
    )
    channels = {ch: cnt for ch, cnt in channel_counts}

    return AnalyticsOverview(
        total_contents=total_contents,
        total_published=total_published,
        channels=channels,
    )


# ── Content analytics ─────────────────────────────────────────────────

@router.get("/{content_id}", response_model=list[AnalyticsOut])
def get_content_analytics(content_id: int, db: Session = Depends(get_db)):
    records = db.query(PublishRecord).filter(PublishRecord.content_id == content_id).all()
    if not records:
        return []
    record_ids = [r.id for r in records]
    analytics = (
        db.query(ContentAnalytics)
        .filter(ContentAnalytics.publish_record_id.in_(record_ids))
        .order_by(ContentAnalytics.collected_at.desc())
        .all()
    )
    return analytics

