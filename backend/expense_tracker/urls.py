from django.contrib import admin
from django.urls import include, path

from apps.accounts.admin import traffic_dashboard_view

urlpatterns = [
    path("admin/traffic/", admin.site.admin_view(traffic_dashboard_view), name="admin-traffic-dashboard"),
    path("admin/", admin.site.urls),
    path("", include("apps.web.urls")),
    path("api/auth/", include("apps.accounts.urls")),
    path("api/", include("apps.expenses.urls")),
]
