from django.db.models import Count, Sum, Value
from django.db.models.functions import Coalesce
from django.db.models import DecimalField
from django.utils import timezone
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.expenses.models import Category, Expense
from apps.expenses.serializers import CategorySerializer, ExpenseSerializer
from apps.expenses.services import apply_expense_filters, build_dashboard_summary


class CategoryViewSet(viewsets.ModelViewSet):
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated]
    pagination_class = None

    def get_queryset(self):
        return (
            Category.objects.filter(user=self.request.user)
            .annotate(
                expense_count=Count("expenses", distinct=True),
                total_spent=Coalesce(
                    Sum("expenses__amount"),
                    Value(0, output_field=DecimalField(max_digits=12, decimal_places=2)),
                ),
            )
            .order_by("name")
        )

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class ExpenseViewSet(viewsets.ModelViewSet):
    serializer_class = ExpenseSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = None

    def get_queryset(self):
        queryset = Expense.objects.filter(user=self.request.user).select_related("category")
        queryset = apply_expense_filters(
            queryset,
            search=self.request.query_params.get("search"),
            category_id=self.request.query_params.get("category"),
            start_date=self.request.query_params.get("start_date"),
            end_date=self.request.query_params.get("end_date"),
        )
        ordering = self.request.query_params.get("ordering", "-spent_on")
        allowed_ordering = {"spent_on", "-spent_on", "amount", "-amount", "created_at", "-created_at"}
        if ordering not in allowed_ordering:
            ordering = "-spent_on"
        return queryset.order_by(ordering, "-created_at")

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class DashboardSummaryAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        summary = build_dashboard_summary(user=request.user)
        recent_expenses = ExpenseSerializer(summary["recent_expenses"], many=True, context={"request": request}).data
        payload = {
            "total_spent": summary["total_spent"],
            "monthly_total": summary["monthly_total"],
            "monthly_average": summary["monthly_average"],
            "expense_count": summary["expense_count"],
            "monthly_expense_count": summary["monthly_expense_count"],
            "budget_total": summary["budget_total"],
            "need_to_pay_amount": summary["need_to_pay_amount"],
            "need_to_pay_label": summary["need_to_pay_label"],
            "category_breakdown": summary["category_breakdown"],
            "recent_expenses": recent_expenses,
        }
        return Response(payload)
