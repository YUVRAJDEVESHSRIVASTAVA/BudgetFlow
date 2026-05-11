from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from django.db.models import Count, Max, Q
from django.template.response import TemplateResponse

from apps.accounts.models import AuthEvent, User


def traffic_dashboard_view(request):
    login_events = AuthEvent.objects.filter(event_type=AuthEvent.EventType.LOGIN)
    logout_events = AuthEvent.objects.filter(event_type=AuthEvent.EventType.LOGOUT)
    user_activity = (
        User.objects.annotate(
            login_count=Count("auth_events", filter=Q(auth_events__event_type=AuthEvent.EventType.LOGIN)),
            logout_count=Count("auth_events", filter=Q(auth_events__event_type=AuthEvent.EventType.LOGOUT)),
            last_login_event_at=Max(
                "auth_events__created_at",
                filter=Q(auth_events__event_type=AuthEvent.EventType.LOGIN),
            ),
            last_logout_event_at=Max(
                "auth_events__created_at",
                filter=Q(auth_events__event_type=AuthEvent.EventType.LOGOUT),
            ),
            last_activity_at=Max("auth_events__created_at"),
        )
        .order_by("-login_count", "-logout_count", "username")
    )

    context = {
        **admin.site.each_context(request),
        "title": "Traffic dashboard",
        "summary": {
            "total_users": User.objects.count(),
            "staff_users": User.objects.filter(is_staff=True).count(),
            "superusers": User.objects.filter(is_superuser=True).count(),
            "login_events": login_events.count(),
            "logout_events": logout_events.count(),
            "active_users": AuthEvent.objects.values("user_id").distinct().count(),
            "last_login": login_events.aggregate(latest=Max("created_at"))["latest"],
            "last_logout": logout_events.aggregate(latest=Max("created_at"))["latest"],
        },
        "recent_events": AuthEvent.objects.select_related("user").order_by("-created_at")[:25],
        "user_activity": user_activity,
    }
    return TemplateResponse(request, "admin/accounts/traffic_dashboard.html", context)


@admin.register(User)
class UserAdmin(DjangoUserAdmin):
    model = User
    list_display = ["username", "email", "first_name", "last_name", "is_staff", "last_login"]
    search_fields = ["username", "email", "first_name", "last_name"]
    ordering = ["username"]
    fieldsets = (
        (None, {"fields": ("username", "password")} ),
        ("Personal info", {"fields": ("first_name", "last_name", "email")} ),
        (
            "Permissions",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                )
            },
        ),
        ("Important dates", {"fields": ("last_login", "date_joined")} ),
    )


@admin.register(AuthEvent)
class AuthEventAdmin(admin.ModelAdmin):
    list_display = ["created_at", "event_type", "user", "identifier", "ip_address"]
    list_filter = ["event_type", "created_at"]
    search_fields = ["user__username", "user__email", "identifier", "ip_address", "user_agent"]
    ordering = ["-created_at"]
    readonly_fields = ["user", "event_type", "identifier", "ip_address", "user_agent", "created_at"]
