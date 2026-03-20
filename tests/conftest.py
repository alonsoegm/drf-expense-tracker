"""
Pytest fixtures and configuration
"""

# Third-party
import pytest
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken

# Local
from expenses.models import Category, Expense

# ============================================================================
# API CLIENT FIXTURE
# ============================================================================


@pytest.fixture
def api_client():
    """
    Fixture that provides DRF API client

    Note: This client is NOT authenticated by default
    Use authenticated_client for authenticated requests
    """
    return APIClient()


# ============================================================================
# USER FIXTURES
# ============================================================================


@pytest.fixture
def user(db):
    """
    Fixture that creates a test user

    Username: testuser
    Password: testpass123
    """
    return User.objects.create_user(
        username="testuser",
        email="test@example.com",
        password="testpass123",
        first_name="Test",
        last_name="User",
    )


@pytest.fixture
def user2(db):
    """
    Fixture that creates a second test user

    For testing user isolation

    Username: testuser2
    Password: testpass123
    """
    return User.objects.create_user(
        username="testuser2",
        email="test2@example.com",
        password="testpass123",
        first_name="Test2",
        last_name="User2",
    )


@pytest.fixture
def admin_user(db):
    """
    Fixture that creates an admin user
    """
    return User.objects.create_superuser(
        username="admin", email="admin@example.com", password="adminpass123"
    )


# ============================================================================
# AUTHENTICATION FIXTURES - NEW!
# ============================================================================


@pytest.fixture
def user_token(user):
    """
    Fixture that provides JWT token for user

    Returns access token string

    Usage:
    def test_something(api_client, user_token):
        response = api_client.get('/api/expenses/',
            HTTP_AUTHORIZATION=f'Bearer {user_token}')
    """
    refresh = RefreshToken.for_user(user)
    return str(refresh.access_token)


@pytest.fixture
def user2_token(user2):
    """
    Fixture that provides JWT token for user2

    For testing user isolation
    """
    refresh = RefreshToken.for_user(user2)
    return str(refresh.access_token)


@pytest.fixture
def authenticated_client(api_client, user_token):
    """
    Fixture that provides an authenticated API client

    Uses JWT Bearer token authentication

    Usage:
    def test_protected_endpoint(authenticated_client):
        response = authenticated_client.get('/api/expenses/')
        assert response.status_code == 200
    """
    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {user_token}")
    return api_client


@pytest.fixture
def authenticated_client2(api_client, user2_token):
    """
    Fixture that provides authenticated client for user2

    For testing user isolation
    """
    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {user2_token}")
    return api_client


# ============================================================================
# CATEGORY FIXTURES (unchanged)
# ============================================================================


@pytest.fixture
def category(db):
    """Fixture that creates a single category"""
    return Category.objects.create(name="Food", description="Food and groceries")


@pytest.fixture
def categories(db):
    """Fixture that creates multiple categories"""
    return [
        Category.objects.create(name="Food", description="Food and groceries"),
        Category.objects.create(name="Transport", description="Transportation costs"),
        Category.objects.create(name="Entertainment", description="Fun activities"),
    ]


# ============================================================================
# EXPENSE FIXTURES - UPDATED!
# ============================================================================


@pytest.fixture
def expense(db, category, user):
    """
    Fixture that creates a single expense

    UPDATED: Uses user fixture (authenticated user)
    """
    return Expense.objects.create(
        user=user,
        category=category,
        amount=50.00,
        description="Test expense",
        date="2024-03-19",
    )


@pytest.fixture
def expenses(db, categories, user):
    """
    Fixture that creates multiple expenses for user

    UPDATED: All expenses belong to user
    """
    return [
        Expense.objects.create(
            user=user,
            category=categories[0],  # Food
            amount=45.50,
            description="Grocery shopping",
            date="2024-03-19",
        ),
        Expense.objects.create(
            user=user,
            category=categories[0],  # Food
            amount=25.00,
            description="Restaurant lunch",
            date="2024-03-18",
        ),
        Expense.objects.create(
            user=user,
            category=categories[1],  # Transport
            amount=50.00,
            description="Gas",
            date="2024-03-17",
        ),
        Expense.objects.create(
            user=user,
            category=categories[2],  # Entertainment
            amount=30.00,
            description="Movie tickets",
            date="2024-03-16",
        ),
        Expense.objects.create(
            user=user,
            category=categories[2],  # Entertainment
            amount=15.00,
            description="Coffee shop",
            date="2024-03-15",
        ),
    ]


@pytest.fixture
def user2_expenses(db, categories, user2):
    """
    Fixture that creates expenses for user2

    For testing user isolation
    """
    return [
        Expense.objects.create(
            user=user2,
            category=categories[0],
            amount=100.00,
            description="User2 grocery",
            date="2024-03-19",
        ),
        Expense.objects.create(
            user=user2,
            category=categories[1],
            amount=75.00,
            description="User2 transport",
            date="2024-03-18",
        ),
    ]


# ============================================================================
# FIXTURE COMPARISON
# ============================================================================
#
# Before Authentication:
# - api_client: Plain client, worked because AllowAny permission
# - user: Created but not used for auth
# - expenses: Created with any user
#
# After Authentication:
# - api_client: Plain client (for unauthenticated tests)
# - authenticated_client: Client with JWT token (for protected endpoints)
# - user_token: JWT token for user
# - expenses: All belong to authenticated user
# - user2_expenses: For testing isolation
#
# Compare to C# xUnit:
# public class AuthenticatedTestBase : IClassFixture<WebApplicationFactory> {
#     protected readonly HttpClient _client;
#     protected readonly string _token;
#
#     public AuthenticatedTestBase() {
#         _token = GetJwtToken();
#         _client.DefaultRequestHeaders.Authorization =
#             new AuthenticationHeaderValue("Bearer", _token);
#     }
# }
