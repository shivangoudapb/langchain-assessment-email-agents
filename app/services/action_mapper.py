from app.models.schemas import (
    EmailCategory,
    RecommendedAction,
    PriorityLevel,
)


ACTION_MAPPING = {
    EmailCategory.SAMPLING: (
        RecommendedAction.CREATE_SAMPLE_TASK,
        PriorityLevel.HIGH,
    ),
    EmailCategory.COSTING: (
        RecommendedAction.CREATE_COSTING_TASK,
        PriorityLevel.HIGH,
    ),
    EmailCategory.PURCHASE_ORDER: (
        RecommendedAction.UPDATE_PO_WORKFLOW,
        PriorityLevel.MEDIUM,
    ),
    EmailCategory.GENERAL: (
        RecommendedAction.NO_ACTION,
        PriorityLevel.LOW,
    ),
    EmailCategory.UNKNOWN: (
        RecommendedAction.MANUAL_REVIEW,
        PriorityLevel.MEDIUM,
    ),
}


def get_action_and_priority(category: EmailCategory):
    return ACTION_MAPPING[category]