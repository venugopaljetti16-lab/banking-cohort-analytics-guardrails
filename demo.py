from src.guardrails import CohortSpec, QAThresholds, build_cohort, evaluate_quality, summarise_for_stakeholders


records = [
    {
        "customer_id": "C001",
        "policy_id": "P001",
        "product_type": "home",
        "tenure_months": 18,
        "policy_status": "active",
        "balance": 2400.0,
    },
    {
        "customer_id": "C002",
        "policy_id": "P002",
        "product_type": "home",
        "tenure_months": 14,
        "policy_status": "active",
        "balance": 1800.0,
    },
    {
        "customer_id": "C003",
        "policy_id": "P003",
        "product_type": "motor",
        "tenure_months": 8,
        "policy_status": "lapsed",
        "balance": 600.0,
    },
]

spec = CohortSpec(product_type="home", min_tenure_months=12, policy_status="active", min_balance=1000.0)
cohort = build_cohort(records, spec)
report = evaluate_quality(cohort, QAThresholds())
print(summarise_for_stakeholders(report))
