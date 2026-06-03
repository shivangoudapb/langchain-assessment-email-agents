from app.llm.chains import (
    ClassificationExtractionChain,
    ActionRecommendationChain,
)

from app.models.schemas import (
    EmailInput,
    FinalOutput,
)


class EmailProcessingPipeline:

    def __init__(self):

        self.classification_chain = (
            ClassificationExtractionChain()
        )

        self.action_chain = (
            ActionRecommendationChain()
        )

    def invoke(
        self,
        email: EmailInput,
    ) -> FinalOutput:

        classification_result = (
            self.classification_chain.invoke(email)
        )

        action_result = (
            self.action_chain.invoke(
                classification_result
            )
        )

        return FinalOutput(
            category=classification_result.category,
            request_intent=classification_result.request_intent,
            extracted_ids=classification_result.extracted_ids,
            confidence=classification_result.confidence,

            recommended_action=action_result.recommended_action,
            priority=action_result.priority,
            summary=action_result.summary,
        )