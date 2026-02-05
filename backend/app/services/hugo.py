import os
import re
from datetime import datetime

from slugify import slugify

from app.config import settings


class HugoService:
    def __init__(self):
        self.repo_path = settings.HUGO_REPO_PATH
        self.content_dir = settings.HUGO_CONTENT_DIR

    def _get_posts_dir(self) -> str:
        posts_dir = os.path.join(self.repo_path, self.content_dir)
        os.makedirs(posts_dir, exist_ok=True)
        return posts_dir

    def generate_front_matter(
        self,
        title: str,
        author: str = "",
        tags: list[str] | None = None,
        category: str = "",
        date: datetime | None = None,
    ) -> str:
        """Generate Hugo YAML front matter."""
        if date is None:
            date = datetime.utcnow()

        lines = [
            "---",
            f'title: "{title}"',
            f"date: {date.strftime('%Y-%m-%dT%H:%M:%S+08:00')}",
        ]
        if author:
            lines.append(f'author: "{author}"')
        if tags:
            tags_str = ", ".join(f'"{t}"' for t in tags)
            lines.append(f"tags: [{tags_str}]")
        if category:
            lines.append(f'categories: ["{category}"]')
        lines.append("draft: false")
        lines.append("---")
        return "\n".join(lines)

    def generate_post(
        self,
        title: str,
        markdown_content: str,
        author: str = "",
        tags: list[str] | None = None,
        category: str = "",
    ) -> str:
        """Generate a complete Hugo post with front matter."""
        front_matter = self.generate_front_matter(title, author, tags, category)
        return f"{front_matter}\n\n{markdown_content}\n"

    def save_post(
        self,
        title: str,
        markdown_content: str,
        author: str = "",
        tags: list[str] | None = None,
        category: str = "",
    ) -> str:
        """Save a post as a markdown file in the Hugo content directory.

        Returns the file path of the saved post.
        """
        if not self.repo_path:
            raise ValueError("Hugo repo path not configured. Set HUGO_REPO_PATH in .env")

        posts_dir = self._get_posts_dir()
        filename = f"{slugify(title, allow_unicode=True)}.md"
        file_path = os.path.join(posts_dir, filename)

        post_content = self.generate_post(title, markdown_content, author, tags, category)
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(post_content)

        return file_path

    def preview_post(
        self,
        title: str,
        markdown_content: str,
        author: str = "",
        tags: list[str] | None = None,
        category: str = "",
    ) -> str:
        """Generate Hugo post content for preview without saving."""
        return self.generate_post(title, markdown_content, author, tags, category)


hugo_service = HugoService()
