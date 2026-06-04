from app.validators.style_validator import (
    extract_style_ids,
    validate_style_ids,
)


def test_extract_style_ids():

    text = (
        "Need sample for RI15104 and ST-2045."
    )

    ids = extract_style_ids(text)

    assert ids == [
        "RI15104",
        "ST-2045",
    ]


def test_remove_hallucinated_ids():

    source_text = (
        "Please arrange sample for RI15104."
    )

    extracted_ids = [
        "RI15104",
        "FAKE123",
    ]

    valid_ids = validate_style_ids(
        extracted_ids,
        source_text,
    )

    assert valid_ids == [
        "RI15104",
    ]


def test_remove_duplicate_ids():

    source_text = (
        "RI15104 sample request."
    )

    extracted_ids = [
        "RI15104",
        "RI15104",
    ]

    valid_ids = validate_style_ids(
        extracted_ids,
        source_text,
    )

    assert valid_ids == [
        "RI15104",
    ]


def test_invalid_pattern_rejected():

    source_text = (
        "Please arrange sample."
    )

    extracted_ids = [
        "12345",
        "ABCXYZ",
    ]

    valid_ids = validate_style_ids(
        extracted_ids,
        source_text,
    )

    assert valid_ids == []