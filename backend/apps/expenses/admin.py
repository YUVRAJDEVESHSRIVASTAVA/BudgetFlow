from django.contrib import admin

from apps.expenses.models import Category, Expense


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ["name", "user", "budget_limit", "created_at"]
    list_filter = ["created_at"]
    search_fields = ["name", "user__username", "user__email"]


@admin.register(Expense)
class ExpenseAdmin(admin.ModelAdmin):
    list_display = ["title", "user", "category", "amount", "spent_on"]
    list_filter = ["spent_on", "category"]
    search_fields = ["title", "description", "user__username", "user__email"]
    ordering = ["-spent_on"]
