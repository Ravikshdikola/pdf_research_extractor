import re

from typing import Optional

def extract_bracket_content(s: str) -> Optional[str]:
    """
    Extract first occurrence of content inside square brackets [] from a string.
    Returns content without brackets or None if no brackets found.
    """
    match = re.search(r'\[([^\[\]]+)\]', s)
    if match:
        return match.group(1).strip()
    return None
