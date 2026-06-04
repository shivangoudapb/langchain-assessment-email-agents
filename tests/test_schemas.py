import pytest

from pydantic import ValidationError

from app.models.schemas import (
    ClassificationOutput,
    EmailCategory,
)


def test_valid_confidence():

    result = ClassificationOutput(
        category=EmailCategory.SAMPLING,
        request_intent="mockup sample",
        extracted_ids=["RI15104"],
        confidence=0.95,
    )

    assert result.confidence == 0.95


def test_confidence_above_one_fails():

    with pytest.raises(ValidationError):

        ClassificationOutput(
            category=EmailCategory.SAMPLING,
            request_intent="mockup sample",
            extracted_ids=["RI15104"],
            confidence=1.5,
        )


def test_confidence_below_zero_fails():

    with pytest.raises(ValidationError):

        ClassificationOutput(
            category=EmailCategory.SAMPLING,
            request_intent="mockup sample",
            extracted_ids=["RI15104"],
            confidence=-0.1,
        )