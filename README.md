# Banking Cohort Analytics Guardrails

Small Python POC for a banking data analyst / data engineer workflow focused on cohort creation, QA validation, and stakeholder-ready reporting.

## Why this fits the role

The recruiter brief emphasizes:
- cohort creation across customer and policy data
- analytical insight generation for programme decision-making
- QA of analyst outputs
- stakeholder progress, risk, and opportunity reporting
- SQL, Snowflake, AWS, and GitLab-aligned delivery habits

This POC mirrors those patterns in a lightweight, testable package.

## What it demonstrates

### 1. Cohort construction
- Filters customer and policy records into a target cohort using reusable rules
- Supports product, tenure, balance, and policy-status driven cohort logic
- Models the kind of cohorting workflow often implemented in Snowflake-backed analytics stacks

### 2. QA guardrails
- Checks for null customer or policy identifiers
- Detects duplicate customer-policy joins
- Flags low record volume and low active-policy coverage
- Produces a clear PASS / WARN / BLOCK decision before analysts circulate outputs

### 3. Stakeholder reporting
- Generates a concise summary covering:
  - progress
  - risks
  - opportunities
- Keeps the output readable for programme managers and analytics leads, not just engineers

## Project structure

```text
banking-cohort-analytics-guardrails/
├── README.md
├── requirements.txt
├── demo.py
├── src/
│   ├── __init__.py
│   └── guardrails.py
└── tests/
    └── test_guardrails.py
```

## Local run

```bash
pip install -r requirements.txt
pytest -q
python demo.py
```

## Role alignment

- **SQL / warehouse thinking:** the cohort rules and data-quality checks are structured like pre-insight warehouse validation
- **Snowflake / AWS fit:** the logic is platform-neutral but shaped around cloud analytics delivery patterns
- **Git / GitLab fit:** the project is version-controlled, testable, and easy to extend in CI
- **QA fit:** issues are surfaced before stakeholder-facing reports go out
- **Stakeholder management fit:** the summary output is framed in the language of progress, risks, and opportunities
