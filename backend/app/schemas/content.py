from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class ContentCreate(BaseModel):
    title: str
    content_markdown: str = ""
    source_type: str = "contribution"
    author: str = ""
    tags: list[str] = []
    category: str = ""
    cover_image: Optional[str] = None


class ContentUpdate(BaseModel):
    title: Optional[str] = None
    content_markdown: Optional[str] = None
    content_html: Optional[str] = None
    source_type: Optional[str] = None
    author: Optional[str] = None
    tags: Optional[list[str]] = None
    category: Optional[str] = None
    cover_image: Optional[str] = None


class ContentStatusUpdate(BaseModel):
    status: str


class ContentOut(BaseModel):
    id: int
    title: str
    content_markdown: str
    content_html: str
    source_type: str
    source_file: Optional[str]
    author: str
    tags: list[str]
    category: str
    cover_image: Optional[str]
    status: str
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class ContentListOut(BaseModel):
    id: int
    title: str
    source_type: str
    author: str
    tags: list[str]
    category: str
    status: str
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class PaginatedContents(BaseModel):
    items: list[ContentListOut]
    total: int
    page: int
    page_size: int
