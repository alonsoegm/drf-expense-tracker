"""
Authentication URLs

Endpoints:
- POST /api/auth/register/ - User registration
- POST /api/auth/login/ - User login
- POST /api/auth/token/refresh/ - Refresh access token
- POST /api/auth/logout/ - Logout (blacklist token)
- GET /api/auth/me/ - Get current user
- PATCH /api/auth/me/ - Update current user
- POST /api/auth/change-password/ - Change password
"""

# Third-party
from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from .views import (
    ChangePasswordView,
    CurrentUserView,
    LoginView,
    LogoutView,
    RegisterView,
)

app_name = "authentication"

urlpatterns = [
    # Registration
    path("register/", RegisterView.as_view(), name="register"),
    # Login (get tokens)
    path("login/", LoginView.as_view(), name="login"),
    # Token refresh
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    # Logout (blacklist refresh token)
    path("logout/", LogoutView.as_view(), name="logout"),
    # Current user
    path("me/", CurrentUserView.as_view(), name="current_user"),
    # Change password
    path("change-password/", ChangePasswordView.as_view(), name="change_password"),
]
