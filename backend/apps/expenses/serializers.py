from decimal import Decimal

from rest_framework import serializers

from apps.expenses.models import Category, Expense


class CategorySerializer(serializers.ModelSerializer):
    expense_count = serializers.IntegerField(read_only=True)
    total_spent = serializers.DecimalField(max_digits=12, decimal_places=2, read_only=True)

    class Meta:
        model = Category
        fields = [
            "id",
            "name",
            "color",
            "budget_limit",
            "expense_count",
            "total_spent",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "expense_count", "total_spent", "created_at", "updated_at"]


class ExpenseSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source="category.name", read_only=True)
    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.none(), allow_null=True, required=False)

    class Meta:
        model = Expense
        fields = [
            "id",
            "category",
            "category_name",
            "title",
            "amount",
            "spent_on",
            "description",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "category_name", "created_at", "updated_at"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        request = self.context.get("request")
        if request and request.user and request.user.is_authenticated:
            self.fields["category"].queryset = Category.objects.filter(user=request.user)

    def validate_amount(self, value: Decimal) -> Decimal:
        if value <= 0:
            raise serializers.ValidationError("Amount must be greater than zero.")
        return value
