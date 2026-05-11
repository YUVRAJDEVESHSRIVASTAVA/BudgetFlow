from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken

from apps.accounts.models import User


class AuthApiTests(APITestCase):
    def test_register_creates_user_and_returns_tokens(self):
        response = self.client.post(
            "/api/auth/register/",
            {
                "username": "alice",
                "email": "alice@example.com",
                "first_name": "Alice",
                "last_name": "Johnson",
                "password": "StrongPass123",
                "confirm_password": "StrongPass123",
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["user"]["username"], "alice")
        self.assertIn("access", response.data["tokens"])
        self.assertTrue(User.objects.filter(username="alice", email="alice@example.com").exists())

    def test_login_and_me_return_authenticated_profile(self):
        user = User.objects.create_user(
            username="brenda",
            email="brenda@example.com",
            password="StrongPass123",
            first_name="Brenda",
            last_name="Rivera",
        )

        login_response = self.client.post(
            "/api/auth/login/",
            {"identifier": "brenda@example.com", "password": "StrongPass123"},
            format="json",
        )

        self.assertEqual(login_response.status_code, status.HTTP_200_OK)
        self.assertEqual(login_response.data["user"]["email"], "brenda@example.com")
        self.assertIn("refresh", login_response.data["tokens"])

        access_token = login_response.data["tokens"]["access"]
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {access_token}")

        me_response = self.client.get("/api/auth/me/")
        self.assertEqual(me_response.status_code, status.HTTP_200_OK)
        self.assertEqual(me_response.data["username"], user.username)
        self.assertEqual(me_response.data["email"], user.email)

    def test_login_rejects_invalid_password(self):
        User.objects.create_user(username="carol", email="carol@example.com", password="StrongPass123")

        response = self.client.post(
            "/api/auth/login/",
            {"identifier": "carol", "password": "wrong-password"},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("Invalid credentials", str(response.data))
