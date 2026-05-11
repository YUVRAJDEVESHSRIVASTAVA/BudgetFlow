from django.urls import path

from apps.web.views import DashboardPageView, HomeView, LoginPageView, RegisterPageView

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("login/", LoginPageView.as_view(), name="login-page"),
    path("register/", RegisterPageView.as_view(), name="register-page"),
    path("dashboard/", DashboardPageView.as_view(), name="dashboard"),
]
