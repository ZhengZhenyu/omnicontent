class CSDNService:
    """CSDN publishing service.

    CSDN natively supports Markdown, so the primary function is to format
    content for copy-paste into CSDN's editor.
    """

    def format_for_csdn(
        self,
        title: str,
        markdown_content: str,
        tags: list[str] | None = None,
        category: str = "",
    ) -> dict:
        """Format content for CSDN publishing.

        Returns a dict with title, formatted markdown, and metadata
        for the user to copy-paste into CSDN.
        """
        # CSDN supports standard Markdown, so minimal transformation needed
        # Add CSDN-specific metadata hints as comments at the top
        header_lines = []
        if tags:
            header_lines.append(f"<!-- tags: {', '.join(tags)} -->")
        if category:
            header_lines.append(f"<!-- category: {category} -->")

        formatted_content = markdown_content
        if header_lines:
            formatted_content = "\n".join(header_lines) + "\n\n" + markdown_content

        return {
            "title": title,
            "content": formatted_content,
            "tags": tags or [],
            "category": category,
            "format": "markdown",
            "platform": "csdn",
        }


csdn_service = CSDNService()
