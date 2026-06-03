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

Also extract a request_intent.

request_intent rules:

- Capture the primary operational request.
- Use 2 to 5 words.
- Use terminology from the email whenever possible.
- Do not include style IDs.
- Do not include buyer names.
- Do not write full sentences.
- Do not mention urgency.
- Focus on what the sender is asking for.

Good examples:

- mockup sample
- fit sample
- proto sample
- yardage request
- revised costing
- booking confirmation
- po update
- follow up

Bad examples:

- Buyer requested mockup sample
- Need mockup sample for RI15104
- RI15104 sample request
- Please urgently arrange mockup sample

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

SUMMARY_PROMPT = ChatPromptTemplate.from_template(
    """
You are an operations assistant.

Generate a short summary of the sender's request.

Rules:

- One sentence only.
- Focus on what the sender requested.
- Mention style IDs when available.
- Do not mention priority.
- Do not mention recommended actions.
- Do not mention internal workflows.
- Do not invent information.

CATEGORY:
{category}

REQUEST INTENT:
{request_intent}

STYLE IDS:
{extracted_ids}
"""
)