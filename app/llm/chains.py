from app.llm.llm_factory import get_llm
from app.llm.prompts import CHAIN1_PROMPT

from app.models.schemas import (
    EmailInput,
    Chain1Result,
    ClassificationOutput
)

from app.validators.style_validator import (
    validate_style_ids
)

from app.llm.prompts import (
    CHAIN1_PROMPT,
    SUMMARY_PROMPT,
)

from app.services.action_mapper import (
    get_action_and_priority,
)

from app.models.schemas import (
    EmailInput,
    Chain1Result,
    ClassificationOutput,
    SummaryResult,
    ActionOutput,
)

class ClassificationExtractionChain:

    def __init__(self):

        self.llm = get_llm()

        self.chain = (
            CHAIN1_PROMPT
            | self.llm.with_structured_output(
                Chain1Result
            )
        )

    def invoke(
        self,
        email: EmailInput
    ) -> ClassificationOutput:

        result = self.chain.invoke(
            {
                "subject": email.subject,
                "body": email.body,
                "thread_context": email.thread_context
            }
        )

        source_text = "\n".join(
            [
                email.subject,
                email.body,
                email.thread_context
            ]
        )

        validated_ids = validate_style_ids(
            result.extracted_ids,
            source_text
        )

        return ClassificationOutput(
            category=result.category,
            request_intent=result.request_intent,
            extracted_ids=validated_ids,
            confidence=result.confidence
        )
    

class ActionRecommendationChain:

    def __init__(self):

        self.llm = get_llm()

        self.summary_chain = (
            SUMMARY_PROMPT
            | self.llm.with_structured_output(
                SummaryResult
            )
        )

    def invoke(
        self,
        classification: ClassificationOutput
    ) -> ActionOutput:

        action, priority = get_action_and_priority(
            classification.category
        )

        summary_result = self.summary_chain.invoke(
            {
                "category": classification.category.value,
                "request_intent": classification.request_intent,
                "extracted_ids": ", ".join(
                    classification.extracted_ids
                ),
                "recommended_action": action.value,
                "priority": priority.value,
            }
        )

        return ActionOutput(
            recommended_action=action,
            priority=priority,
            summary=summary_result.summary,
        )