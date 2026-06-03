from enum import Enum
from typing import List

from pydantic import BaseModel, Field


class EmailCategory(str, Enum):
    SAMPLING = "SAMPLING"
    COSTING = "COSTING"
    PURCHASE_ORDER = "PURCHASE_ORDER"
    GENERAL = "GENERAL"
    UNKNOWN = "UNKNOWN"


class RecommendedAction(str, Enum):
    CREATE_SAMPLE_TASK = "CREATE_SAMPLE_TASK"
    CREATE_COSTING_TASK = "CREATE_COSTING_TASK"
    UPDATE_PO_WORKFLOW = "UPDATE_PO_WORKFLOW"
    NO_ACTION = "NO_ACTION"
    MANUAL_REVIEW = "MANUAL_REVIEW"


class PriorityLevel(str, Enum):
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"


class EmailInput(BaseModel):
    subject: str
    body: str
    thread_context: str


# Internal Chain 1 result
class Chain1Result(BaseModel):
    category: EmailCategory

    request_intent: str = Field(
        max_length=50,
        description="Short operational request type"
    )

    confidence: float = Field(
        ge=0.0,
        le=1.0,
        description="LLM confidence score"
    )

    extracted_ids: List[str]

class SummaryResult(BaseModel):
    summary: str = Field(
        max_length=200,
        description="Short operational summary"
    )

# Output of Chain 1
class ClassificationOutput(BaseModel):
    category: EmailCategory

    request_intent: str = Field(
        max_length=50,
        description="Short operational request type"
    )

    extracted_ids: List[str]

    confidence: float = Field(
        ge=0.0,
        le=1.0,
        description="Classification confidence score"
    )


# Output of Chain 2
class ActionOutput(BaseModel):
    recommended_action: RecommendedAction
    priority: PriorityLevel
    summary: str


# Final pipeline output
class FinalOutput(BaseModel):
    category: EmailCategory

    request_intent: str

    extracted_ids: List[str]

    confidence: float

    recommended_action: RecommendedAction

    priority: PriorityLevel

    summary: str