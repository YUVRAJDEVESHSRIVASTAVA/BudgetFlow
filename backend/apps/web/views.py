from django.views.generic import TemplateView


class HomeView(TemplateView):
    template_name = "index.html"


class LoginPageView(TemplateView):
    template_name = "login.html"


class RegisterPageView(TemplateView):
    template_name = "register.html"


class DashboardPageView(TemplateView):
    template_name = "dashboard.html"
