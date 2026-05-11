from django.contrib.auth import authenticate
from django.utils import timezone
from rest_framework_simplejwt.tokens import RefreshToken

from apps.accounts.models import AuthEvent, User


def create_user(*, username: str, email: str, password: str, first_name: str = "", last_name: str = "") -> User:
    return User.objects.create_user(
        username=username,
        email=email,
        password=password,
        first_name=first_name,
        last_name=last_name,
    )


def authenticate_user(*, identifier: str, password: str) -> User | None:
    if "@" in identifier:
        user = User.objects.filter(email__iexact=identifier).first()
        if not user:
            return None
        return authenticate(username=user.username, password=password)
    return authenticate(username=identifier, password=password)


def get_client_ip(request) -> str | None:
    forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR", "")
    if forwarded_for:
        return forwarded_for.split(",")[0].strip()
    return request.META.get("REMOTE_ADDR")


def record_login(*, user: User, request, identifier: str = "") -> AuthEvent:
    user.last_login = timezone.now()
    user.save(update_fields=["last_login"])
    return AuthEvent.objects.create(
        user=user,
        event_type=AuthEvent.EventType.LOGIN,
        identifier=identifier or user.username,
        ip_address=get_client_ip(request),
        user_agent=request.META.get("HTTP_USER_AGENT", ""),
    )


def record_logout(*, user: User, request, identifier: str = "") -> AuthEvent:
    return AuthEvent.objects.create(
        user=user,
        event_type=AuthEvent.EventType.LOGOUT,
        identifier=identifier or user.username,
        ip_address=get_client_ip(request),
        user_agent=request.META.get("HTTP_USER_AGENT", ""),
    )


def build_token_pair(user: User) -> dict[str, str]:
    refresh = RefreshToken.for_user(user)
    return {"refresh": str(refresh), "access": str(refresh.access_token)}
