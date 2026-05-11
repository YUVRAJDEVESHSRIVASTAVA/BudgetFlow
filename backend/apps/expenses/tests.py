from decimal import Decimal

from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken

from apps.accounts.models import User
from apps.expenses.models import Category, Expense


class ExpenseApiTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="dylan",
            email="dylan@example.com",
            password="StrongPass123",
            first_name="Dylan",
        )
        self.access_token = str(RefreshToken.for_user(self.user).access_token)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.access_token}")

    def test_category_and_expense_summary_flow(self):
        category_response = self.client.post(
            "/api/categories/",
            {
                "name": "Groceries",
                "color": "#14B8A6",
                "budget_limit": "500.00",
            },
            format="json",
        )

        self.assertEqual(category_response.status_code, status.HTTP_201_CREATED)
        category_id = category_response.data["id"]
        self.assertTrue(Category.objects.filter(user=self.user, name="Groceries").exists())

        expense_response = self.client.post(
            "/api/expenses/",
            {
                "title": "Weekly grocery run",
                "amount": "125.50",
                "spent_on": "2026-05-10",
                "category": category_id,
                "description": "Fresh produce and pantry staples",
            },
            format="json",
        )

        self.assertEqual(expense_response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Expense.objects.filter(user=self.user, title="Weekly grocery run").exists())

        summary_response = self.client.get("/api/summary/")
        self.assertEqual(summary_response.status_code, status.HTTP_200_OK)
        self.assertEqual(summary_response.data["expense_count"], 1)
        self.assertEqual(summary_response.data["monthly_expense_count"], 1)
        self.assertEqual(summary_response.data["total_spent"], Decimal("125.50"))
        self.assertEqual(summary_response.data["monthly_total"], Decimal("125.50"))
        self.assertEqual(summary_response.data["monthly_average"], Decimal("125.50"))
        self.assertEqual(summary_response.data["need_to_pay_amount"], Decimal("0.00"))
        self.assertEqual(summary_response.data["need_to_pay_label"], "Within budget")
        self.assertEqual(summary_response.data["category_breakdown"][0]["category_name"], "Groceries")

    def test_over_budget_category_is_reported_as_amount_due(self):
        category_response = self.client.post(
            "/api/categories/",
            {
                "name": "Utilities",
                "color": "#F59E0B",
                "budget_limit": "100.00",
            },
            format="json",
        )

        category_id = category_response.data["id"]
        expense_response = self.client.post(
            "/api/expenses/",
            {
                "title": "Electric bill",
                "amount": "175.00",
                "spent_on": "2026-05-10",
                "category": category_id,
                "description": "Monthly power bill",
            },
            format="json",
        )

        self.assertEqual(expense_response.status_code, status.HTTP_201_CREATED)

        summary_response = self.client.get("/api/summary/")
        self.assertEqual(summary_response.status_code, status.HTTP_200_OK)
        self.assertEqual(summary_response.data["monthly_average"], Decimal("175.00"))
        self.assertEqual(summary_response.data["need_to_pay_amount"], Decimal("75.00"))
        self.assertEqual(summary_response.data["need_to_pay_label"], "Utilities over budget")

    def test_category_list_is_scoped_to_authenticated_user(self):
        Category.objects.create(user=self.user, name="Rent", color="#0F766E")
        other_user = User.objects.create_user(username="maya", email="maya@example.com", password="StrongPass123")
        Category.objects.create(user=other_user, name="Travel", color="#F59E0B")

        response = self.client.get("/api/categories/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["name"], "Rent")
