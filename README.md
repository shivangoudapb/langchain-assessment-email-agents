# LangChain Email Classification & Action Recommendation Pipeline

## Overview

This project implements a composable LangChain-based email processing pipeline for operational emails in a manufacturing supply chain.

The system classifies emails, extracts key identifiers, recommends operational actions, and generates concise summaries for operations teams.

The solution is built using two connected LangChain chains:

```text
Raw Email
    ↓
Chain 1: Classification + Extraction
    ↓
ClassificationOutput
    ↓
Chain 2: Action Recommendation
    ↓
ActionOutput
    ↓
FinalOutput
```

A FastAPI endpoint is included for integration into larger systems.

---

## Features

### Chain 1 – Classification & Extraction

Responsibilities:

* Classify emails into:

  * `SAMPLING`
  * `COSTING`
  * `PURCHASE_ORDER`
  * `GENERAL`
  * `UNKNOWN`
* Extract style identifiers such as:

  * `RI15104`
  * `ST-2045`
* Generate a short operational intent
* Return a confidence score
* Validate outputs using Pydantic
* Prevent hallucinated style IDs

Example output:

```json
{
  "category": "SAMPLING",
  "request_intent": "mockup sample",
  "extracted_ids": ["RI15104"],
  "confidence": 1.0
}
```

---

### Chain 2 – Action Recommendation

Responsibilities:

* Consume Chain 1 output
* Recommend the next operational action
* Assign priority
* Generate an operational summary

Example output:

```json
{
  "recommended_action": "CREATE_SAMPLE_TASK",
  "priority": "HIGH",
  "summary": "The sender requested a mockup sample for style ID RI15104."
}
```

---

## Final Pipeline Output

```json
{
  "category": "SAMPLING",
  "request_intent": "mockup sample",
  "extracted_ids": ["RI15104"],
  "confidence": 1.0,
  "recommended_action": "CREATE_SAMPLE_TASK",
  "priority": "HIGH",
  "summary": "The sender requested a mockup sample for style ID RI15104."
}
```

---

# Architecture

## Why Two Chains Instead of One?

The system is intentionally split into two chains.

### Chain 1

Responsible for language understanding:

* Classification
* Style ID extraction
* Intent identification

### Chain 2

Responsible for workflow decisions:

* Action recommendation
* Prioritization
* Summary generation

### Benefits

* Better modularity
* Easier testing
* Easier prompt maintenance
* Independent evolution of business logic
* Reusable intermediate outputs

This design allows future chains to be added without changing existing components.

---

# Hallucination Prevention

A common failure mode of LLMs is hallucinating identifiers that do not exist in the source email.

To mitigate this:

1. Style IDs must match approved patterns:

```text
RI15104
ST-2045
```

2. Every extracted ID is validated against the original email text.

3. IDs not present in the email are discarded.

Example:

```python
validate_style_ids(
    ["RI15104", "FAKE123"],
    source_email
)
```

Output:

```python
["RI15104"]
```

This validation layer ensures downstream workflows never receive fabricated identifiers.

---

# Extending the System

To add a new category such as:

```text
INSPECTION_REQUEST
```

Only four changes are required:

1. Add enum value in `schemas.py`
2. Update Chain 1 prompt instructions
3. Add mapping in `action_mapper.py`
4. Add tests

No pipeline changes are required.

This keeps the architecture open for future workflow expansion.

---

# Testing Strategy

The project uses deterministic unit tests for validation and business logic.

### Style Validator Tests

* ID extraction
* Duplicate removal
* Pattern validation
* Hallucination prevention

### Action Mapper Tests

* Category → Action mapping
* Category → Priority mapping

### Schema Validation Tests

* Confidence bounds
* Pydantic validation rules

### Test Results

```bash
pytest tests -v
```

Result:

```text
11 passed
```

---

# Fixture Evaluation

An evaluation script is provided:

```bash
python evaluation/evaluate_fixtures.py
```

The script runs the pipeline against the provided fixture emails and records results for manual inspection.

This evaluation is intentionally separate from unit tests to avoid dependence on external LLM API availability.

---

# FastAPI Integration

Run:

```bash
uvicorn app.main:app --reload
```

Swagger UI:

```text
http://127.0.0.1:8000/docs
```

Endpoint:

```http
POST /process-email
```

Example Request:

```json
{
  "subject": "Need mockup sample for RI15104",
  "body": "Please arrange mockup sample for RI15104.",
  "thread_context": "First order from this buyer."
}
```

Example Response:

```json
{
  "category": "SAMPLING",
  "request_intent": "mockup sample",
  "extracted_ids": ["RI15104"],
  "confidence": 1.0,
  "recommended_action": "CREATE_SAMPLE_TASK",
  "priority": "HIGH",
  "summary": "The sender requested a mockup sample for style ID RI15104."
}
```

---

# Shared Order-State Design (Future Multi-Agent System)

If multiple agents interact with the same order, a shared order-state model should be maintained.

## Proposed Minimal Schema

```json
{
  "order_id": "",
  "style_ids": [],
  "buyer": "",
  "vendor": "",
  "status": "",
  "owner": "",
  "last_updated": "",
  "history": []
}
```

## Update Rules

* Agents never overwrite existing history
* Every update appends a new event
* Current state is derived from event history
* Ownership changes are recorded as events
* Timestamps are stored for all modifications

This event-driven approach prevents agents from accidentally overwriting each other's work.

---

# Important Future Fields

Future integrations with techpacks and client documents should persist:

* Style references
* Buyer information
* Vendor information
* PO numbers
* Costing revisions
* Shipment milestones
* CRD dates
* Approval checkpoints
* Ownership assignments
* Audit history

These fields enable future workflow automation beyond email processing.

---

# Project Structure

```text
app/
├── api/
│   └── routes.py
├── llm/
│   ├── chains.py
│   ├── prompts.py
│   └── llm_factory.py
├── models/
│   └── schemas.py
├── services/
│   ├── action_mapper.py
│   └── email_pipeline.py
├── validators/
│   └── style_validator.py
└── main.py

tests/
├── test_action_mapper.py
├── test_schemas.py
└── test_style_validator.py

evaluation/
└── evaluate_fixtures.py
```

---

# Setup

## Create Virtual Environment

```bash
python -m venv venv
```

Activate:

```bash
venv\Scripts\activate
```

## Install Dependencies

```bash
pip install -r requirements.txt
```

## Configure Environment

Create a `.env` file:

```text
GOOGLE_API_KEY=your_api_key_here
```

## Run API

```bash
uvicorn app.main:app --reload
```

---

# Technologies Used

* Python 3.11
* LangChain
* Gemini 2.5 Flash
* FastAPI
* Pydantic
* Pytest
* python-dotenv
