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
            extracted_ids=validated_ids,
            confidence=result.confidence
        )