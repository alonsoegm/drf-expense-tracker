"""
API Tests for Authentication endpoints

Tests:
- User registration
- User login
- Token refresh
- Get current user
- Update current user
- Change password
- Logout
"""

# Third-party
import pytest
from django.urls import reverse


@pytest.mark.django_db
class TestRegister:
    """Tests for POST /api/auth/register/"""

    def test_register_success(self, api_client):
        """Test successful user registration"""
        url = reverse("authentication:register")
        data = {
            "username": "newuser",
            "email": "newuser@example.com",
            "password": "SecurePass123!",
            "passwordConfirm": "SecurePass123!",
            "firstName": "New",
            "lastName": "User",
        }

        response = api_client.post(url, data, format="json")

        assert response.status_code == 201
        assert "user" in response.data
        assert "access" in response.data
        assert "refresh" in response.data
        assert response.data["user"]["username"] == "newuser"

    def test_register_password_mismatch(self, api_client):
        """Test registration with mismatched passwords"""
        url = reverse("authentication:register")
        data = {
            "username": "newuser",
            "email": "newuser@example.com",
            "password": "SecurePass123!",
            "passwordConfirm": "DifferentPass123!",
        }

        response = api_client.post(url, data, format="json")

        assert response.status_code == 400
        assert "password" in response.data or "passwordConfirm" in response.data

    def test_register_duplicate_username(self, api_client, user):
        """Test registration with existing username"""
        url = reverse("authentication:register")
        data = {
            "username": "testuser",  # Already exists
            "email": "different@example.com",
            "password": "SecurePass123!",
            "passwordConfirm": "SecurePass123!",
        }

        response = api_client.post(url, data, format="json")

        assert response.status_code == 400
        assert "username" in response.data


@pytest.mark.django_db
class TestLogin:
    """Tests for POST /api/auth/login/"""

    def test_login_success(self, api_client, user):
        """Test successful login"""
        url = reverse("authentication:login")
        data = {"username": "testuser", "password": "testpass123"}

        response = api_client.post(url, data, format="json")

        assert response.status_code == 200
        assert "access" in response.data
        assert "refresh" in response.data

    def test_login_wrong_password(self, api_client, user):
        """Test login with wrong password"""
        url = reverse("authentication:login")
        data = {"username": "testuser", "password": "wrongpassword"}

        response = api_client.post(url, data, format="json")

        assert response.status_code == 401

    def test_login_nonexistent_user(self, api_client):
        """Test login with non-existent user"""
        url = reverse("authentication:login")
        data = {"username": "doesnotexist", "password": "somepassword"}

        response = api_client.post(url, data, format="json")

        assert response.status_code == 401


@pytest.mark.django_db
class TestCurrentUser:
    """Tests for GET/PATCH /api/auth/me/"""

    def test_get_current_user_unauthenticated(self, api_client):
        """Test getting current user without authentication"""
        url = reverse("authentication:current_user")
        response = api_client.get(url)

        assert response.status_code == 401

    def test_get_current_user(self, authenticated_client, user):
        """Test getting current user info"""
        url = reverse("authentication:current_user")
        response = authenticated_client.get(url)

        assert response.status_code == 200
        assert response.data["username"] == "testuser"
        assert response.data["email"] == "test@example.com"
        assert "first_name" in response.data
        assert "last_name" in response.data

    def test_update_current_user(self, authenticated_client):
        """Test updating current user"""
        url = reverse("authentication:current_user")
        data = {"firstName": "Updated", "lastName": "Name"}

        response = authenticated_client.patch(url, data, format="json")

        assert response.status_code == 200
        assert response.data["first_name"] == "Updated"
        assert response.data["last_name"] == "Name"


@pytest.mark.django_db
class TestChangePassword:
    """Tests for POST /api/auth/change-password/"""

    def test_change_password_success(self, authenticated_client, user):
        """Test successful password change"""
        url = reverse("authentication:change_password")
        data = {
            "oldPassword": "testpass123",
            "newPassword": "NewSecurePass123!",
            "newPasswordConfirm": "NewSecurePass123!",
        }

        response = authenticated_client.put(url, data, format="json")

        assert response.status_code == 200

        # Verify password was changed
        user.refresh_from_db()
        assert user.check_password("NewSecurePass123!")

    def test_change_password_wrong_old_password(self, authenticated_client):
        """Test password change with wrong old password"""
        url = reverse("authentication:change_password")
        data = {
            "oldPassword": "wrongpassword",
            "newPassword": "NewSecurePass123!",
            "newPasswordConfirm": "NewSecurePass123!",
        }

        response = authenticated_client.put(url, data, format="json")

        assert response.status_code == 400
        assert "old_password" in response.data

    def test_change_password_mismatch(self, authenticated_client):
        """Test password change with mismatched new passwords"""
        url = reverse("authentication:change_password")
        data = {
            "oldPassword": "testpass123",
            "newPassword": "NewSecurePass123!",
            "newPasswordConfirm": "DifferentPass123!",
        }

        response = authenticated_client.put(url, data, format="json")

        assert response.status_code == 400
