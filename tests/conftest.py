"""
Pytest fixtures and configuration

What are fixtures?
- Reusable test data and setup code
- Like [SetUp] methods in xUnit, but more powerful
- Can be shared across all tests
- Dependency injection for tests

Compare to C#:
public class TestFixture : IDisposable {
    public User TestUser { get; set; }

    public TestFixture() {
        // Setup
        TestUser = new User { Username = "testuser" };
    }

    public void Dispose() {
        // Cleanup
    }
}

[Fact]
public void TestSomething(TestFixture fixture) {
    var user = fixture.TestUser;
    // Use user in test
}
"""

# Third-party
import pytest
from django.contrib.auth.models import User
from rest_framework.test import APIClient

# Local
from expenses.models import Category, Expense

# ============================================================================
# API CLIENT FIXTURE
# ============================================================================


@pytest.fixture
def api_client():
    """
    Fixture that provides DRF API client

    Usage:
    def test_something(api_client):
        response = api_client.get('/api/categories/')
        assert response.status_code == 200

    Compare to C#:
    private readonly HttpClient _client;

    public TestClass() {
        _client = new HttpClient();
    }
    """
    return APIClient()


# ============================================================================
# USER FIXTURES
# ============================================================================


@pytest.fixture
def user(db):
    """
    Fixture that creates a test user

    The 'db' parameter is a pytest-django fixture that:
    - Sets up test database
    - Rolls back after test
    - Like [DatabaseFixture] in xUnit

    Usage:
    def test_something(user):
        assert user.username == "testuser"
    """
    return User.objects.create_user(
        username="testuser", email="test@example.com", password="testpass123"
    )


@pytest.fixture
def admin_user(db):
    """
    Fixture that creates an admin user

    Usage:
    def test_admin_action(admin_user):
        assert admin_user.is_staff
    """
    return User.objects.create_superuser(
        username="admin", email="admin@example.com", password="adminpass123"
    )


# ============================================================================
# CATEGORY FIXTURES
# ============================================================================


@pytest.fixture
def category(db):
    """
    Fixture that creates a single category

    Usage:
    def test_category(category):
        assert category.name == "Food"
    """
    return Category.objects.create(name="Food", description="Food and groceries")


@pytest.fixture
def categories(db):
    """
    Fixture that creates multiple categories

    Returns a list of categories

    Usage:
    def test_multiple_categories(categories):
        assert len(categories) == 3
        assert categories[0].name == "Food"
    """
    return [
        Category.objects.create(name="Food", description="Food and groceries"),
        Category.objects.create(name="Transport", description="Transportation costs"),
        Category.objects.create(name="Entertainment", description="Fun activities"),
    ]


# ============================================================================
# EXPENSE FIXTURES
# ============================================================================


@pytest.fixture
def expense(db, category, user):
    """
    Fixture that creates a single expense

    Depends on 'category' and 'user' fixtures
    pytest automatically resolves dependencies!

    Usage:
    def test_expense(expense):
        assert expense.amount == 50.00
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
    Fixture that creates multiple expenses

    Returns a list of expenses across different categories

    Usage:
    def test_multiple_expenses(expenses):
        assert len(expenses) == 5
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


# ============================================================================
# AUTHENTICATED CLIENT FIXTURE
# ============================================================================


@pytest.fixture
def authenticated_client(api_client, user):
    """
    Fixture that provides an authenticated API client

    For now uses session auth (for browsable API)
    Later we'll add JWT token support

    Usage:
    def test_protected_endpoint(authenticated_client):
        response = authenticated_client.get('/api/expenses/')
        assert response.status_code == 200
    """
    api_client.force_authenticate(user=user)
    return api_client


# ============================================================================
# FIXTURE SCOPES
# ============================================================================
#
# Fixtures can have different scopes:
#
# @pytest.fixture(scope='function')  # Default - new instance per test
# @pytest.fixture(scope='class')     # Shared within test class
# @pytest.fixture(scope='module')    # Shared within test file
# @pytest.fixture(scope='session')   # Shared across all tests
#
# Example:
# @pytest.fixture(scope='session')
# def django_db_setup():
#     # Expensive setup once per test session
#     pass
#
# ============================================================================
# FIXTURE COMPARISON
# ============================================================================
#
# pytest fixtures vs C# xUnit:
#
# pytest:
# @pytest.fixture
# def user(db):
#     return User.objects.create(...)
#
# def test_something(user):  # Injected automatically
#     assert user.username == "testuser"
#
# C# xUnit:
# public class UserFixture : IDisposable {
#     public User User { get; set; }
#     public UserFixture() {
#         User = new User { Username = "testuser" };
#     }
# }
#
# public class TestClass : IClassFixture<UserFixture> {
#     private readonly UserFixture _fixture;
#
#     public TestClass(UserFixture fixture) {
#         _fixture = fixture;
#     }
#
#     [Fact]
#     public void TestSomething() {
#         Assert.Equal("testuser", _fixture.User.Username);
#     }
# }
#
# pytest is more concise!
