from langchain_core.prompts import ChatPromptTemplate


CHAIN1_PROMPT = ChatPromptTemplate.from_template(
    """
You are an expert operations email classification assistant.

Classify the email into EXACTLY ONE category:

- SAMPLING
- COSTING
- PURCHASE_ORDER
- GENERAL
- UNKNOWN

Also extract all style IDs.

Valid style ID formats:

- RI followed by digits
  Example: RI15104

- ST- followed by digits
  Example: ST-2045

IMPORTANT:

- Search subject, body, and thread context.
- Do NOT invent IDs.
- Only extract IDs actually present.
- Return confidence between 0.0 and 1.0.

EMAIL SUBJECT:
{subject}

EMAIL BODY:
{body}

THREAD CONTEXT:
{thread_context}
"""
)