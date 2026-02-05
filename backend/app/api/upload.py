import os
import uuid

from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session

from app.config import settings
from app.database import get_db
from app.models.content import Content
from app.schemas.content import ContentOut
from app.services.converter import convert_docx_to_markdown, convert_markdown_to_html, read_markdown_file

router = APIRouter()

ALLOWED_EXTENSIONS = {".docx", ".md", ".markdown"}


@router.post("/upload", response_model=ContentOut, status_code=201)
async def upload_file(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
):
    if not file.filename:
        raise HTTPException(400, "No filename provided")

    ext = os.path.splitext(file.filename)[1].lower()
    if ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(400, f"Unsupported file type: {ext}. Allowed: {ALLOWED_EXTENSIONS}")

    # Save uploaded file
    save_name = f"{uuid.uuid4().hex}{ext}"
    save_path = os.path.join(settings.UPLOAD_DIR, save_name)
    file_content = await file.read()

    if len(file_content) > settings.MAX_UPLOAD_SIZE:
        raise HTTPException(400, f"File too large. Max size: {settings.MAX_UPLOAD_SIZE // 1024 // 1024}MB")

    with open(save_path, "wb") as f:
        f.write(file_content)

    # Convert to markdown
    title = os.path.splitext(file.filename)[0]

    if ext == ".docx":
        markdown_text, image_paths = convert_docx_to_markdown(save_path)
    else:
        markdown_text = read_markdown_file(save_path)

    content_html = convert_markdown_to_html(markdown_text) if markdown_text else ""

    content = Content(
        title=title,
        content_markdown=markdown_text,
        content_html=content_html,
        source_type="contribution",
        source_file=save_name,
        status="draft",
    )
    db.add(content)
    db.commit()
    db.refresh(content)
    return content
