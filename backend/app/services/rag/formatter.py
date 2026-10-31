"""
KhetGPT Markdown Formatter & Sanitizer
Ensures clean, properly structured Markdown for agricultural responses
without broken syntax, missing spaces, or raw formatting symbols.
"""

import re
from typing import Optional

def sanitize_and_format_markdown(text: str, language: str = "en") -> str:
    """
    Cleans raw LLM markdown output to ensure full compliance with
    CommonMark / GitHub-Flavored Markdown specifications.
    """
    if not text:
        return ""

    formatted = text.strip()

    # 1. Fix headings missing space after hash (e.g. '###Heading' -> '### Heading')
    formatted = re.sub(r'^(#{1,6})([^\s#])', r'\1 \2', formatted, flags=re.MULTILINE)

    # 2. Fix bullet points missing space (e.g. '*Item' -> '* Item', '-Item' -> '- Item')
    formatted = re.sub(r'^([*+-])([^\s*+-])', r'\1 \2', formatted, flags=re.MULTILINE)

    # 3. Fix numbered lists missing space (e.g. '1.Item' -> '1. Item')
    formatted = re.sub(r'^(\d+\.)([^\s\d])', r'\1 \2', formatted, flags=re.MULTILINE)

    # 4. Ensure blank line before markdown tables (starting with '|')
    formatted = re.sub(r'([^\n])\n(\|.+?\|)', r'\1\n\n\2', formatted)

    # 5. Ensure blank line after markdown tables
    formatted = re.sub(r'(\|.+?\|)\n([^\n|])', r'\1\n\n\2', formatted)

    # 6. Fix unclosed bold tags (odd number of '**')
    bold_count = formatted.count("**")
    if bold_count % 2 != 0:
        # Close the trailing open bold
        formatted += "**"

    # 7. Normalize excessive blank lines (max 2 consecutive newlines)
    formatted = re.sub(r'\n{3,}', '\n\n', formatted)

    return formatted.strip()
