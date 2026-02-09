from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.core.dependencies import get_current_community
from app.core.security import encrypt_value, decrypt_value
from app.database import get_db
from app.models.content import Content
from app.models.publish_record import PublishRecord, ContentAnalytics
from app.schemas.publish import AnalyticsOut, AnalyticsOverview, ChannelConfigOut, ChannelConfigUpdate
from app.models.channel import ChannelConfig

router = APIRouter()

# Fields that should be encrypted in channel configs
SENSITIVE_FIELDS = {"app_secret", "cookie", "token", "secret", "password", "api_key"}


def _mask_sensitive_config(config: dict) -> dict:
    """Return a copy of config with sensitive values masked for display."""
    masked = {}
    for k, v in config.items():
        if any(sf in k.lower() for sf in SENSITIVE_FIELDS) and v:
            # Show only last 4 chars
            masked[k] = "••••••" + str(v)[-4:] if len(str(v)) > 4 else "••••"
        else:
            masked[k] = v
    return masked


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


# ── Channel settings (community-scoped) ───────────────────────────────

@router.get("/settings/channels", response_model=list[ChannelConfigOut])
def get_channel_configs(
    community_id: int = Depends(get_current_community),
    db: Session = Depends(get_db),
):
    configs = db.query(ChannelConfig).filter(
        ChannelConfig.community_id == community_id
    ).all()
    if not configs:
        # Initialize default configs for this community
        for ch in ["wechat", "hugo", "csdn", "zhihu"]:
            cfg = ChannelConfig(
                channel=ch, config={}, enabled=False,
                community_id=community_id,
            )
            db.add(cfg)
        db.commit()
        configs = db.query(ChannelConfig).filter(
            ChannelConfig.community_id == community_id
        ).all()

    # Mask sensitive values before returning
    result = []
    for cfg in configs:
        masked_config = _mask_sensitive_config(cfg.config) if cfg.config else {}
        result.append(ChannelConfigOut(
            id=cfg.id,
            channel=cfg.channel,
            config=masked_config,
            enabled=cfg.enabled,
        ))
    return result


@router.put("/settings/channels/{channel}", response_model=ChannelConfigOut)
def update_channel_config(
    channel: str,
    data: ChannelConfigUpdate,
    community_id: int = Depends(get_current_community),
    db: Session = Depends(get_db),
):
    valid_channels = {"wechat", "hugo", "csdn", "zhihu"}
    if channel not in valid_channels:
        raise HTTPException(400, f"Invalid channel. Must be one of {valid_channels}")

    cfg = db.query(ChannelConfig).filter(
        ChannelConfig.channel == channel,
        ChannelConfig.community_id == community_id,
    ).first()

    if not cfg:
        cfg = ChannelConfig(
            channel=channel,
            config={},
            enabled=data.enabled or False,
            community_id=community_id,
        )
        db.add(cfg)

    if data.config:
        # Merge with existing config, encrypt sensitive fields
        existing_config = dict(cfg.config or {})
        for k, v in data.config.items():
            if any(sf in k.lower() for sf in SENSITIVE_FIELDS):
                # Only update if the value is not a masked placeholder
                if v and not v.startswith("••••"):
                    existing_config[k] = encrypt_value(v)
            else:
                existing_config[k] = v
        # Reassign to trigger SQLAlchemy change detection on JSON column
        cfg.config = existing_config

    if data.enabled is not None:
        cfg.enabled = data.enabled

    db.commit()
    db.refresh(cfg)

    # Return masked config
    masked_config = _mask_sensitive_config(cfg.config) if cfg.config else {}
    return ChannelConfigOut(
        id=cfg.id,
        channel=cfg.channel,
        config=masked_config,
        enabled=cfg.enabled,
    )

