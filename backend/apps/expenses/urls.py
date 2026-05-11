from django.urls import include, path
from rest_framework.routers import DefaultRouter

from apps.expenses.views import CategoryViewSet, DashboardSummaryAPIView, ExpenseViewSet

router = DefaultRouter()
router.register(r"categories", CategoryViewSet, basename="category")
router.register(r"expenses", ExpenseViewSet, basename="expense")

urlpatterns = [
    path("summary/", DashboardSummaryAPIView.as_view(), name="summary"),
    path("", include(router.urls)),
]
