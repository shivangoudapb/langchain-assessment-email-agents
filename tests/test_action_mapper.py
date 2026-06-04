from app.services.action_mapper import (
    get_action_and_priority,
)

from app.models.schemas import (
    EmailCategory,
    RecommendedAction,
    PriorityLevel,
)


def test_sampling_mapping():

    action, priority = (
        get_action_and_priority(
            EmailCategory.SAMPLING
        )
    )

    assert (
        action
        ==
        RecommendedAction.CREATE_SAMPLE_TASK
    )

    assert (
        priority
        ==
        PriorityLevel.HIGH
    )


def test_costing_mapping():

    action, priority = (
        get_action_and_priority(
            EmailCategory.COSTING
        )
    )

    assert (
        action
        ==
        RecommendedAction.CREATE_COSTING_TASK
    )

    assert (
        priority
        ==
        PriorityLevel.HIGH
    )


def test_purchase_order_mapping():

    action, priority = (
        get_action_and_priority(
            EmailCategory.PURCHASE_ORDER
        )
    )

    assert (
        action
        ==
        RecommendedAction.UPDATE_PO_WORKFLOW
    )

    assert (
        priority
        ==
        PriorityLevel.MEDIUM
    )


def test_general_mapping():

    action, priority = (
        get_action_and_priority(
            EmailCategory.GENERAL
        )
    )

    assert (
        action
        ==
        RecommendedAction.NO_ACTION
    )

    assert (
        priority
        ==
        PriorityLevel.LOW
    )