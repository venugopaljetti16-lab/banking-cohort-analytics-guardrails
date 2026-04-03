from dataclasses import dataclass
from typing import Any, Optional


@dataclass(frozen=True)
class CohortSpec:
    product_type: Optional[str] = None
    min_tenure_months: int = 0
    policy_status: Optional[str] = None
    min_balance: float = 0.0


@dataclass(frozen=True)
class QAThresholds:
    min_records: int = 2
    max_null_ratio: float = 0.10
    max_duplicate_ratio: float = 0.05
    min_active_policy_ratio: float = 0.60


@dataclass(frozen=True)
class QAReport:
    record_count: int
    null_ratio: float
    duplicate_ratio: float
    active_policy_ratio: float
    status: str
    issues: tuple[str, ...]


def build_cohort(records: list[dict[str, Any]], spec: CohortSpec) -> list[dict[str, Any]]:
    cohort: list[dict[str, Any]] = []
    for row in records:
        if spec.product_type and row.get("product_type") != spec.product_type:
            continue
        if row.get("tenure_months", 0) < spec.min_tenure_months:
            continue
        if spec.policy_status and row.get("policy_status") != spec.policy_status:
            continue
        if row.get("balance", 0.0) < spec.min_balance:
            continue
        cohort.append(row)
    return cohort


def evaluate_quality(records: list[dict[str, Any]], thresholds: QAThresholds) -> QAReport:
    record_count = len(records)
    if record_count == 0:
        return QAReport(0, 1.0, 0.0, 0.0, "BLOCK", ("Empty cohort",))

    null_rows = 0
    duplicate_keys: set[tuple[Any, Any]] = set()
    duplicate_count = 0
    active_count = 0

    for row in records:
        customer_id = row.get("customer_id")
        policy_id = row.get("policy_id")
        if customer_id in (None, "") or policy_id in (None, ""):
            null_rows += 1

        key = (customer_id, policy_id)
        if key in duplicate_keys:
            duplicate_count += 1
        else:
            duplicate_keys.add(key)

        if row.get("policy_status") == "active":
            active_count += 1

    null_ratio = null_rows / record_count
    duplicate_ratio = duplicate_count / record_count
    active_policy_ratio = active_count / record_count

    issues: list[str] = []
    status = "PASS"

    if record_count < thresholds.min_records:
        issues.append("Low cohort volume")
        status = "WARN"
    if null_ratio > thresholds.max_null_ratio:
        issues.append("High null ratio in customer/policy identifiers")
        status = "BLOCK"
    if duplicate_ratio > thresholds.max_duplicate_ratio:
        issues.append("Duplicate customer-policy pairs detected")
        status = "BLOCK"
    if active_policy_ratio < thresholds.min_active_policy_ratio and status != "BLOCK":
        issues.append("Active policy coverage below target")
        status = "WARN"

    return QAReport(
        record_count=record_count,
        null_ratio=round(null_ratio, 4),
        duplicate_ratio=round(duplicate_ratio, 4),
        active_policy_ratio=round(active_policy_ratio, 4),
        status=status,
        issues=tuple(issues),
    )


def summarise_for_stakeholders(report: QAReport) -> str:
    risk_line = "Risks: none material." if not report.issues else f"Risks: {'; '.join(report.issues)}."
    if report.status == "PASS":
        opportunity = "Opportunity: cohort is ready for downstream insight generation and programme reporting."
    elif report.status == "WARN":
        opportunity = "Opportunity: proceed with caution and prioritise analyst review before stakeholder circulation."
    else:
        opportunity = "Opportunity: fix cohort quality issues before using the output for strategic decision-making."

    return (
        f"Progress: built cohort with {report.record_count} records. "
        f"Null ratio={report.null_ratio:.2%}, duplicate ratio={report.duplicate_ratio:.2%}, "
        f"active policy coverage={report.active_policy_ratio:.2%}. "
        f"{risk_line} {opportunity}"
    )
