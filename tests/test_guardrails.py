from src.guardrails import CohortSpec, QAThresholds, build_cohort, evaluate_quality, summarise_for_stakeholders


def sample_records():
    return [
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


def test_build_cohort_filters_customer_policy_population():
    cohort = build_cohort(
        sample_records(),
        CohortSpec(product_type="home", min_tenure_months=12, policy_status="active", min_balance=1000.0),
    )

    assert len(cohort) == 2
    assert {row["customer_id"] for row in cohort} == {"C001", "C002"}


def test_evaluate_quality_blocks_nulls_and_duplicates():
    report = evaluate_quality(
        [
            {"customer_id": "C001", "policy_id": "P001", "policy_status": "active"},
            {"customer_id": "C001", "policy_id": "P001", "policy_status": "active"},
            {"customer_id": None, "policy_id": "P003", "policy_status": "active"},
        ],
        QAThresholds(min_records=2, max_null_ratio=0.10, max_duplicate_ratio=0.10),
    )

    assert report.status == "BLOCK"
    assert "High null ratio in customer/policy identifiers" in report.issues
    assert "Duplicate customer-policy pairs detected" in report.issues


def test_summary_mentions_progress_risks_and_opportunity():
    report = evaluate_quality(sample_records()[:2], QAThresholds())
    summary = summarise_for_stakeholders(report)

    assert "Progress: built cohort with 2 records." in summary
    assert "Risks:" in summary
    assert "Opportunity:" in summary
