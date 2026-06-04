from fastapi import APIRouter

from app.models.schemas import (
    EmailInput,
    FinalOutput,
)

from app.services.email_pipeline import (
    EmailProcessingPipeline,
)

router = APIRouter()

pipeline = EmailProcessingPipeline()


@router.post(
    "/process-email",
    response_model=FinalOutput,
)
def process_email(
    email: EmailInput,
):

    return pipeline.invoke(email)