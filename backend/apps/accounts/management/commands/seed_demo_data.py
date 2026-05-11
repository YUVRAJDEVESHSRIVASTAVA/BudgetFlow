from decimal import Decimal
from datetime import timedelta

from django.core.management.base import BaseCommand
from django.utils import timezone

from apps.accounts.models import AuthEvent, User
from apps.expenses.models import Category, Expense


class Command(BaseCommand):
    help = "Seed demo users, categories, expenses, and auth activity for testing."

    def handle(self, *args, **options):
        now = timezone.now()
        admin_username = "trafficadmin"
        admin_email = "trafficadmin@example.com"
        admin_password = "TrafficAdmin@1234"
        demo_password = "DemoUser@1234"

        demo_users = [
            {
                "username": "asha_patel",
                "email": "asha.patel@example.com",
                "first_name": "Asha",
                "last_name": "Patel",
                "login_offset_days": 5,
                "session_hours": 4,
                "categories": [
                    {"name": "Groceries", "color": "#2563EB", "budget_limit": "12000.00"},
                    {"name": "Transport", "color": "#F97316", "budget_limit": "5000.00"},
                ],
                "expenses": [
                    {"title": "Monthly groceries", "amount": "4250.00", "category": "Groceries", "days_ago": 1, "description": "Food and kitchen supplies"},
                    {"title": "Metro pass", "amount": "780.00", "category": "Transport", "days_ago": 3, "description": "Commute to work"},
                    {"title": "Dinner out", "amount": "1350.00", "category": "Groceries", "days_ago": 5, "description": "Weekend dinner"},
                ],
            },
            {
                "username": "imran_khan",
                "email": "imran.khan@example.com",
                "first_name": "Imran",
                "last_name": "Khan",
                "login_offset_days": 4,
                "session_hours": 3,
                "categories": [
                    {"name": "Bills", "color": "#14B8A6", "budget_limit": "15000.00"},
                    {"name": "Entertainment", "color": "#8B5CF6", "budget_limit": "4000.00"},
                ],
                "expenses": [
                    {"title": "Electricity bill", "amount": "2450.00", "category": "Bills", "days_ago": 2, "description": "Monthly utility payment"},
                    {"title": "Movie night", "amount": "780.00", "category": "Entertainment", "days_ago": 4, "description": "Tickets and snacks"},
                    {"title": "Internet recharge", "amount": "1199.00", "category": "Bills", "days_ago": 6, "description": "Broadband renewal"},
                ],
            },
            {
                "username": "meera_rao",
                "email": "meera.rao@example.com",
                "first_name": "Meera",
                "last_name": "Rao",
                "login_offset_days": 3,
                "session_hours": 5,
                "categories": [
                    {"name": "Health", "color": "#DC2626", "budget_limit": "8000.00"},
                    {"name": "Food", "color": "#059669", "budget_limit": "10000.00"},
                ],
                "expenses": [
                    {"title": "Pharmacy visit", "amount": "640.00", "category": "Health", "days_ago": 1, "description": "Medicines and vitamins"},
                    {"title": "Lunch break", "amount": "320.00", "category": "Food", "days_ago": 2, "description": "Office lunch"},
                    {"title": "Streaming subscription", "amount": "499.00", "category": "Health", "days_ago": 7, "description": "Monthly subscription"},
                ],
            },
            {
                "username": "daniel_joseph",
                "email": "daniel.joseph@example.com",
                "first_name": "Daniel",
                "last_name": "Joseph",
                "login_offset_days": 2,
                "session_hours": 6,
                "categories": [
                    {"name": "Travel", "color": "#0EA5E9", "budget_limit": "9000.00"},
                    {"name": "Office", "color": "#64748B", "budget_limit": "3000.00"},
                ],
                "expenses": [
                    {"title": "Cab ride", "amount": "510.00", "category": "Travel", "days_ago": 1, "description": "Airport pickup"},
                    {"title": "Lunch with team", "amount": "280.00", "category": "Office", "days_ago": 3, "description": "Team meeting lunch"},
                    {"title": "Stationery", "amount": "690.00", "category": "Office", "days_ago": 6, "description": "Notebooks and pens"},
                ],
            },
            {
                "username": "priya_nair",
                "email": "priya.nair@example.com",
                "first_name": "Priya",
                "last_name": "Nair",
                "login_offset_days": 1,
                "session_hours": 2,
                "categories": [
                    {"name": "Shopping", "color": "#EC4899", "budget_limit": "11000.00"},
                    {"name": "Savings", "color": "#22C55E", "budget_limit": "20000.00"},
                ],
                "expenses": [
                    {"title": "Clothes purchase", "amount": "1950.00", "category": "Shopping", "days_ago": 2, "description": "Work clothes"},
                    {"title": "Coffee catch-up", "amount": "180.00", "category": "Shopping", "days_ago": 4, "description": "Quick meetup"},
                    {"title": "Snacks", "amount": "140.00", "category": "Shopping", "days_ago": 5, "description": "Evening snacks"},
                ],
            },
        ]

        cleanup_usernames = [spec["username"] for spec in demo_users] + [admin_username]
        User.objects.filter(username__in=cleanup_usernames).delete()

        admin_user = User.objects.create_superuser(
            username=admin_username,
            email=admin_email,
            password=admin_password,
        )
        admin_user.first_name = "Traffic"
        admin_user.last_name = "Admin"
        admin_user.save(update_fields=["first_name", "last_name"])
        self._create_auth_event(admin_user, AuthEvent.EventType.LOGIN, now - timedelta(minutes=15))
        User.objects.filter(pk=admin_user.pk).update(last_login=now - timedelta(minutes=15))

        for index, spec in enumerate(demo_users):
            user = User.objects.create_user(
                username=spec["username"],
                email=spec["email"],
                password=demo_password,
                first_name=spec["first_name"],
                last_name=spec["last_name"],
            )

            category_lookup = {}
            for category_spec in spec["categories"]:
                category = Category.objects.create(
                    user=user,
                    name=category_spec["name"],
                    color=category_spec["color"],
                    budget_limit=Decimal(category_spec["budget_limit"]),
                )
                category_lookup[category.name] = category

            for expense_spec in spec["expenses"]:
                Expense.objects.create(
                    user=user,
                    category=category_lookup[expense_spec["category"]],
                    title=expense_spec["title"],
                    amount=Decimal(expense_spec["amount"]),
                    spent_on=(now - timedelta(days=expense_spec["days_ago"])).date(),
                    description=expense_spec["description"],
                )

            login_at = now - timedelta(days=spec["login_offset_days"], hours=2)
            logout_at = login_at + timedelta(hours=spec["session_hours"])
            self._create_auth_event(user, AuthEvent.EventType.LOGIN, login_at)
            self._create_auth_event(user, AuthEvent.EventType.LOGOUT, logout_at)
            User.objects.filter(pk=user.pk).update(last_login=login_at)

        self.stdout.write(self.style.SUCCESS("Seeded 5 demo users, 1 admin user, categories, expenses, and auth events."))
        self.stdout.write(self.style.SUCCESS(f"Admin login: {admin_username} / {admin_password}"))
        self.stdout.write(self.style.SUCCESS(f"Demo user password: {demo_password}"))

    def _create_auth_event(self, user, event_type, created_at):
        event = AuthEvent.objects.create(
            user=user,
            event_type=event_type,
            identifier=user.username,
            ip_address="127.0.0.1",
            user_agent="seed-demo-data",
        )
        AuthEvent.objects.filter(pk=event.pk).update(created_at=created_at)
        return event