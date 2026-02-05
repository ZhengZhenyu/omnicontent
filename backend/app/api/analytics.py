from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.content import Content
from app.models.publish_record import PublishRecord, ContentAnalytics
from app.schemas.publish import AnalyticsOut, AnalyticsOverview, ChannelConfigOut, ChannelConfigUpdate
from app.models.channel import ChannelConfig

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


# ── Channel settings ──────────────────────────────────────────────────

@router.get("/settings/channels", response_model=list[ChannelConfigOut])
def get_channel_configs(db: Session = Depends(get_db)):
    configs = db.query(ChannelConfig).all()
    if not configs:
        # Initialize default configs
        for ch in ["wechat", "hugo", "csdn", "zhihu"]:
            cfg = ChannelConfig(channel=ch, config={}, enabled=False)
            db.add(cfg)
        db.commit()
        configs = db.query(ChannelConfig).all()
    return configs


@router.put("/settings/channels/{channel}", response_model=ChannelConfigOut)
def update_channel_config(channel: str, data: ChannelConfigUpdate, db: Session = Depends(get_db)):
    valid_channels = {"wechat", "hugo", "csdn", "zhihu"}
    if channel not in valid_channels:
        raise HTTPException(400, f"Invalid channel. Must be one of {valid_channels}")

    cfg = db.query(ChannelConfig).filter(ChannelConfig.channel == channel).first()
    if not cfg:
        cfg = ChannelConfig(channel=channel, config=data.config, enabled=data.enabled or False)
        db.add(cfg)
    else:
        if data.config:
            cfg.config = data.config
        if data.enabled is not None:
            cfg.enabled = data.enabled
    db.commit()
    db.refresh(cfg)
    return cfg
