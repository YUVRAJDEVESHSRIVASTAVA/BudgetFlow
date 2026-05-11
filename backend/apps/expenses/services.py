from decimal import Decimal

from django.db.models import Avg, DecimalField, Sum, Value
from django.db.models.functions import Coalesce
from django.db.models import Q
from django.utils import timezone

from apps.expenses.models import Category, Expense


def apply_expense_filters(queryset, *, search=None, category_id=None, start_date=None, end_date=None):
    if search:
        queryset = queryset.filter(Q(title__icontains=search) | Q(description__icontains=search))
    if category_id:
        queryset = queryset.filter(category_id=category_id)
    if start_date:
        queryset = queryset.filter(spent_on__gte=start_date)
    if end_date:
        queryset = queryset.filter(spent_on__lte=end_date)
    return queryset


def build_dashboard_summary(*, user):
    today = timezone.localdate()
    month_start = today.replace(day=1)

    base_queryset = Expense.objects.filter(user=user).select_related("category")
    monthly_queryset = base_queryset.filter(spent_on__gte=month_start)

    total_spent = base_queryset.aggregate(
        total=Coalesce(Sum("amount"), Value(Decimal("0.00"), output_field=DecimalField(max_digits=12, decimal_places=2))),
    )["total"]
    monthly_total = monthly_queryset.aggregate(
        total=Coalesce(Sum("amount"), Value(Decimal("0.00"), output_field=DecimalField(max_digits=12, decimal_places=2))),
    )["total"]
    monthly_average = monthly_queryset.aggregate(
        average=Coalesce(Avg("amount"), Value(Decimal("0.00"), output_field=DecimalField(max_digits=12, decimal_places=2))),
    )["average"]

    budget_total = Category.objects.filter(user=user, budget_limit__isnull=False).aggregate(
        total=Coalesce(Sum("budget_limit"), Value(Decimal("0.00"), output_field=DecimalField(max_digits=12, decimal_places=2))),
    )["total"]

    category_breakdown = []
    for row in (
        monthly_queryset.values("category__id", "category__name", "category__color")
        .annotate(total=Coalesce(Sum("amount"), Value(Decimal("0.00"), output_field=DecimalField(max_digits=12, decimal_places=2))))
        .order_by("-total")
    ):
        category_breakdown.append(
            {
                "category_id": row["category__id"],
                "category_name": row["category__name"],
                "color": row["category__color"],
                "total": row["total"],
            }
        )

    budget_rows = list(
        monthly_queryset.filter(category__budget_limit__isnull=False)
        .values("category__name", "category__budget_limit")
        .annotate(
            total=Coalesce(Sum("amount"), Value(Decimal("0.00"), output_field=DecimalField(max_digits=12, decimal_places=2))),
        )
    )

    over_budget_rows = []
    for row in budget_rows:
        overage = row["total"] - row["category__budget_limit"]
        if overage > 0:
            over_budget_rows.append(
                {
                    "category_name": row["category__name"],
                    "need_to_pay": overage,
                }
            )

    if over_budget_rows:
        urgent_category = max(over_budget_rows, key=lambda item: item["need_to_pay"])
        need_to_pay_amount = urgent_category["need_to_pay"]
        need_to_pay_label = f"{urgent_category['category_name']} over budget"
    elif budget_total > 0:
        need_to_pay_amount = Decimal("0.00")
        need_to_pay_label = "Within budget"
    else:
        need_to_pay_amount = None
        need_to_pay_label = "No budget set"

    recent_expenses = base_queryset.order_by("-spent_on", "-created_at")[:5]

    return {
        "total_spent": total_spent,
        "monthly_total": monthly_total,
        "monthly_average": monthly_average,
        "expense_count": base_queryset.count(),
        "monthly_expense_count": monthly_queryset.count(),
        "budget_total": budget_total,
        "need_to_pay_amount": need_to_pay_amount,
        "need_to_pay_label": need_to_pay_label,
        "category_breakdown": category_breakdown,
        "recent_expenses": recent_expenses,
    }
