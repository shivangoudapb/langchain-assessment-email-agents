import re
from typing import List


STYLE_ID_PATTERN = re.compile(
    r"\b(?:RI\d{4,8}|ST-\d{3,8})\b",
    re.IGNORECASE
)


def extract_style_ids(text: str) -> List[str]:
    matches = STYLE_ID_PATTERN.findall(text)

    seen = set()
    result = []

    for match in matches:
        normalized = match.upper()

        if normalized not in seen:
            seen.add(normalized)
            result.append(normalized)

    return result


def validate_style_ids(
    extracted_ids: List[str],
    source_text: str
) -> List[str]:

    source_text_upper = source_text.upper()

    valid_ids = []
    seen = set()

    for style_id in extracted_ids:

        normalized = style_id.upper().strip()

        if not STYLE_ID_PATTERN.fullmatch(normalized):
            continue

        if normalized not in source_text_upper:
            continue

        if normalized in seen:
            continue

        seen.add(normalized)
        valid_ids.append(normalized)

    return valid_ids