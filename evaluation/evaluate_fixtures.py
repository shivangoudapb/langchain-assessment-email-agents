import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

import json
import time

from dotenv import load_dotenv

from app.models.schemas import EmailInput
from app.services.email_pipeline import EmailProcessingPipeline


FIXTURE_PATH = (
    PROJECT_ROOT
    / "fixtures"
    / "sample_emails.json"
)

OUTPUT_PATH = (
    PROJECT_ROOT
    / "evaluation"
    / "evaluation_results.json"
)


def serialize_result(result):

    return {
        "category": result.category.value,
        "request_intent": result.request_intent,
        "extracted_ids": result.extracted_ids,
        "confidence": result.confidence,
        "recommended_action":
            result.recommended_action.value,
        "priority":
            result.priority.value,
        "summary":
            result.summary,
    }


def save_results(results):

    with open(
        OUTPUT_PATH,
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            results,
            f,
            indent=2,
        )


def main():

    load_dotenv()

    pipeline = EmailProcessingPipeline()

    with open(
        FIXTURE_PATH,
        "r",
        encoding="utf-8"
    ) as f:

        data = json.load(f)

    emails = data["emails"]

    results = []

    print()
    print("=" * 80)
    print(
        f"Evaluating {len(emails)} fixture emails"
    )
    print("=" * 80)

    for index, email_data in enumerate(
        emails,
        start=1
    ):

        print()
        print("-" * 80)
        print(
            f"[{index}/{len(emails)}] "
            f"{email_data['id']}"
        )

        email = EmailInput(
            subject=email_data["subject"],
            body=email_data["body"],
            thread_context=email_data[
                "thread_context"
            ]
        )

        try:

            result = pipeline.invoke(email)

            serialized = serialize_result(
                result
            )

            results.append(
                {
                    "fixture_id":
                        email_data["id"],
                    "result":
                        serialized,
                }
            )

            save_results(results)

            print(
                json.dumps(
                    serialized,
                    indent=2
                )
            )

        except Exception as e:

            print(
                f"ERROR: {e}"
            )

            results.append(
                {
                    "fixture_id":
                        email_data["id"],
                    "error":
                        str(e),
                }
            )

            save_results(results)

        # stay under free-tier limits
        time.sleep(30)

    print()
    print("=" * 80)
    print(
        f"Results saved to:"
    )
    print(
        OUTPUT_PATH
    )
    print("=" * 80)


if __name__ == "__main__":
    main()