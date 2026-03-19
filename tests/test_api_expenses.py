"""
API Tests for Expense endpoints

IMPORTANT - camelCase vs snake_case:
------------------------------------
- Request data (what we send): camelCase (like frontend)
  Example: {'categoryId': 1, 'amount': 50.00}

- Response data (what we receive): camelCase (converted by djangorestframework-camel-case)
  Example: response.data['categoryName'], response.data['createdAt']

- Python code (models, variables): snake_case (Python convention)
  Example: expense.category_id, expense.created_at

Compare to C#:
public async Task TestCreateExpense() {
    var dto = new ExpenseDto { CategoryId = 1, Amount = 50 };
    var response = await _client.PostAsJsonAsync("/api/expenses", dto);
    Assert.Equal(HttpStatusCode.Created, response.StatusCode);
}
"""

# Standard Library
from datetime import date, timedelta
from decimal import Decimal

# Third-party
import pytest
from django.urls import reverse

# ============================================================================
# EXPENSE LIST TESTS (GET /api/expenses/)
# ============================================================================


@pytest.mark.django_db
class TestExpenseList:
    """Tests for GET /api/expenses/"""

    def test_list_expenses_empty(self, api_client):
        """Test listing expenses when none exist"""
        url = reverse("expenses:expense-list")
        response = api_client.get(url)

        assert response.status_code == 200
        assert response.data["count"] == 0
        assert response.data["results"] == []

    def test_list_expenses(self, api_client, expenses):
        """
        Test listing all expenses

        Should return paginated list with simplified serializer
        Response fields in camelCase
        """
        url = reverse("expenses:expense-list")
        response = api_client.get(url)

        assert response.status_code == 200
        assert response.data["count"] == 5
        assert len(response.data["results"]) == 5

        # Check structure (ExpenseListSerializer)
        first = response.data["results"][0]
        assert "id" in first
        assert "category_name" in first
        assert "amount" in first
        assert "description" in first
        assert "date" in first
        assert "username" in first
        # List serializer shouldn't have nested category_detail
        assert "category_detail" not in first

    def test_filter_by_category(self, api_client, expenses, categories):
        """
        Test filtering by category

        GET /api/expenses/?category=1
        """
        url = reverse("expenses:expense-list")
        response = api_client.get(url, {"category": categories[0].id})

        assert response.status_code == 200
        # Should have 2 Food expenses
        assert response.data["count"] == 2
        for expense in response.data["results"]:
            assert expense["category_name"] == "Food"

    def test_filter_by_amount_min(self, api_client, expenses):
        """
        Test filtering by minimum amount

        GET /api/expenses/?amount_min=40
        """
        url = reverse("expenses:expense-list")
        response = api_client.get(url, {"amount_min": 40})

        assert response.status_code == 200
        # Should have expenses >= 40 (45.50 and 50.00)
        assert response.data["count"] == 2
        for expense in response.data["results"]:
            assert Decimal(expense["amount"]) >= Decimal("40")

    def test_filter_by_amount_range(self, api_client, expenses):
        """
        Test filtering by amount range

        GET /api/expenses/?amount_min=20&amount_max=35
        """
        url = reverse("expenses:expense-list")
        response = api_client.get(url, {"amount_min": 20, "amount_max": 35})

        assert response.status_code == 200
        # Should have expenses between 20-35 (25.00 and 30.00)
        assert response.data["count"] == 2

    def test_filter_by_date_range(self, api_client, expenses):
        """
        Test filtering by date range

        GET /api/expenses/?date_from=2024-03-17&date_to=2024-03-19
        """
        url = reverse("expenses:expense-list")
        response = api_client.get(
            url, {"date_from": "2024-03-17", "date_to": "2024-03-19"}
        )

        assert response.status_code == 200
        # Should have expenses in that range
        assert response.data["count"] == 3

    def test_search_expenses(self, api_client, expenses):
        """
        Test search functionality

        GET /api/expenses/?search=grocery

        Should search in description field
        """
        url = reverse("expenses:expense-list")
        response = api_client.get(url, {"search": "grocery"})

        assert response.status_code == 200
        assert response.data["count"] >= 1
        # Should find "Grocery shopping"
        descriptions = [exp["description"] for exp in response.data["results"]]
        assert any("Grocery" in desc or "grocery" in desc for desc in descriptions)

    def test_ordering_by_amount(self, api_client, expenses):
        """
        Test ordering by amount ascending

        GET /api/expenses/?ordering=amount
        """
        url = reverse("expenses:expense-list")
        response = api_client.get(url, {"ordering": "amount"})

        assert response.status_code == 200
        amounts = [Decimal(exp["amount"]) for exp in response.data["results"]]

        # Should be sorted low to high
        assert amounts == sorted(amounts)

    def test_ordering_by_amount_descending(self, api_client, expenses):
        """
        Test ordering by amount descending

        GET /api/expenses/?ordering=-amount
        """
        url = reverse("expenses:expense-list")
        response = api_client.get(url, {"ordering": "-amount"})

        assert response.status_code == 200
        amounts = [Decimal(exp["amount"]) for exp in response.data["results"]]

        # Should be sorted high to low
        assert amounts == sorted(amounts, reverse=True)

    def test_ordering_by_date(self, api_client, expenses):
        """
        Test ordering by date descending (default)

        GET /api/expenses/?ordering=-date
        """
        url = reverse("expenses:expense-list")
        response = api_client.get(url, {"ordering": "-date"})

        assert response.status_code == 200
        dates = [exp["date"] for exp in response.data["results"]]

        # Should be newest first
        assert dates == sorted(dates, reverse=True)

    def test_complex_filter(self, api_client, expenses, categories):
        """
        Test combining multiple filters

        GET /api/expenses/?category=1&amount_min=30&ordering=-amount
        """
        url = reverse("expenses:expense-list")
        response = api_client.get(
            url,
            {
                "category": categories[0].id,  # Food
                "amount_min": 30,
                "ordering": "-amount",
            },
        )

        assert response.status_code == 200
        # Should have 1 Food expense >= 30 (45.50)
        assert response.data["count"] == 1
        assert response.data["results"][0]["category_name"] == "Food"


# ============================================================================
# EXPENSE CREATE TESTS (POST /api/expenses/)
# ============================================================================


@pytest.mark.django_db
class TestExpenseCreate:
    """Tests for POST /api/expenses/"""

    def test_create_expense(self, api_client, category, user):
        """
        Test creating a valid expense

        Request body in camelCase (like frontend would send)
        Response in camelCase
        """
        url = reverse("expenses:expense-list")
        data = {
            "categoryId": category.id,  # camelCase!
            "amount": 75.50,
            "description": "Test expense",
            "date": "2024-03-19",
        }

        response = api_client.post(url, data, format="json")

        assert response.status_code == 201
        assert Decimal(response.data["amount"]) == Decimal("75.50")
        assert response.data["description"] == "Test expense"
        assert response.data["date"] == "2024-03-19"

        # Response fields
        assert "category_detail" in response.data
        assert "category_name" in response.data
        assert "created_at" in response.data
        assert "updated_at" in response.data
        assert response.data["category_name"] == category.name

    def test_create_expense_minimal(self, api_client, category, user):
        """Test creating expense with only required fields"""
        url = reverse("expenses:expense-list")
        data = {
            "categoryId": category.id,  # camelCase!
            "amount": 100.00,
            "description": "Minimal expense",
            "date": "2024-03-19",
        }

        response = api_client.post(url, data, format="json")

        assert response.status_code == 201
        assert response.data["description"] == "Minimal expense"

    def test_create_expense_amount_zero(self, api_client, category):
        """
        Test validation: amount must be > 0

        Should return 400 Bad Request
        """
        url = reverse("expenses:expense-list")
        data = {
            "categoryId": category.id,  # camelCase!
            "amount": 0,
            "date": "2024-03-19",
        }

        response = api_client.post(url, data, format="json")

        assert response.status_code == 400
        assert "amount" in response.data

    def test_create_expense_amount_negative(self, api_client, category):
        """Test validation: negative amounts not allowed"""
        url = reverse("expenses:expense-list")
        data = {
            "categoryId": category.id,  # camelCase!
            "amount": -50.00,
            "date": "2024-03-19",
        }

        response = api_client.post(url, data, format="json")

        assert response.status_code == 400
        assert "amount" in response.data

    def test_create_expense_amount_too_large(self, api_client, category):
        """Test validation: amount cannot exceed 1,000,000"""
        url = reverse("expenses:expense-list")
        data = {
            "categoryId": category.id,  # camelCase!
            "amount": 1_000_001,
            "date": "2024-03-19",
        }

        response = api_client.post(url, data, format="json")

        assert response.status_code == 400
        assert "amount" in response.data

    def test_create_expense_future_date(self, api_client, category):
        """
        Test validation: date cannot be in the future
        """
        url = reverse("expenses:expense-list")
        future_date = date.today() + timedelta(days=1)

        data = {
            "categoryId": category.id,  # camelCase!
            "amount": 50.00,
            "date": str(future_date),
        }

        response = api_client.post(url, data, format="json")

        assert response.status_code == 400
        assert "date" in response.data

    def test_create_expense_invalid_category(self, api_client):
        """Test validation: category must exist"""
        url = reverse("expenses:expense-list")
        data = {
            "categoryId": 9999,  # camelCase! Non-existent
            "amount": 50.00,
            "date": "2024-03-19",
        }

        response = api_client.post(url, data, format="json")

        assert response.status_code == 400
        assert "category_id" in response.data or "category" in response.data


# ============================================================================
# EXPENSE RETRIEVE TESTS (GET /api/expenses/{id}/)
# ============================================================================


@pytest.mark.django_db
class TestExpenseRetrieve:
    """Tests for GET /api/expenses/{id}/"""

    def test_retrieve_expense(self, api_client, expense):
        """
        Test retrieving a single expense

        Should return full ExpenseSerializer with nested data
        All fields in camelCase
        """
        url = reverse("expenses:expense-detail", kwargs={"pk": expense.id})
        response = api_client.get(url)

        assert response.status_code == 200
        assert response.data["id"] == expense.id
        assert Decimal(response.data["amount"]) == expense.amount

        # Detail serializer includes nested category
        assert "category_detail" in response.data
        assert response.data["category_detail"]["id"] == expense.category.id
        assert response.data["category_detail"]["name"] == expense.category.name

        # Convenience fields
        assert "category_name" in response.data
        assert "username" in response.data
        assert "created_at" in response.data
        assert "updated_at" in response.data

    def test_retrieve_expense_not_found(self, api_client):
        """
        Test retrieving non-existent expense

        Should return 404 Not Found
        """
        url = reverse("expenses:expense-detail", kwargs={"pk": 9999})
        response = api_client.get(url)

        assert response.status_code == 404


# ============================================================================
# EXPENSE UPDATE TESTS (PUT/PATCH /api/expenses/{id}/)
# ============================================================================


@pytest.mark.django_db
class TestExpenseUpdate:
    """Tests for PUT and PATCH /api/expenses/{id}/"""

    def test_update_expense_put(self, api_client, expense, category):
        """
        Test full update (PUT)

        Request in camelCase, response in camelCase
        """
        url = reverse("expenses:expense-detail", kwargs={"pk": expense.id})
        data = {
            "categoryId": category.id,  # camelCase!
            "amount": 99.99,
            "description": "Updated expense",
            "date": "2024-03-18",
        }

        response = api_client.put(url, data, format="json")

        assert response.status_code == 200
        assert Decimal(response.data["amount"]) == Decimal("99.99")
        assert response.data["description"] == "Updated expense"
        assert response.data["date"] == "2024-03-18"

    def test_update_expense_patch(self, api_client, expense):
        """
        Test partial update (PATCH)

        Only update specific fields
        """
        url = reverse("expenses:expense-detail", kwargs={"pk": expense.id})
        original_amount = expense.amount

        data = {"description": "Partially updated"}

        response = api_client.patch(url, data, format="json")

        assert response.status_code == 200
        assert Decimal(response.data["amount"]) == original_amount  # Unchanged
        assert response.data["description"] == "Partially updated"

    def test_update_expense_amount_only(self, api_client, expense):
        """Test updating only amount"""
        url = reverse("expenses:expense-detail", kwargs={"pk": expense.id})
        data = {"amount": 123.45}

        response = api_client.patch(url, data, format="json")

        assert response.status_code == 200
        assert Decimal(response.data["amount"]) == Decimal("123.45")

    def test_update_expense_not_found(self, api_client):
        """Test updating non-existent expense"""
        url = reverse("expenses:expense-detail", kwargs={"pk": 9999})
        data = {"amount": 50.00}

        response = api_client.patch(url, data, format="json")

        assert response.status_code == 404


# ============================================================================
# EXPENSE DELETE TESTS (DELETE /api/expenses/{id}/)
# ============================================================================


@pytest.mark.django_db
class TestExpenseDelete:
    """Tests for DELETE /api/expenses/{id}/"""

    def test_delete_expense(self, api_client, expense):
        """
        Test deleting an expense

        Should return 204 No Content
        """
        url = reverse("expenses:expense-detail", kwargs={"pk": expense.id})
        response = api_client.delete(url)

        assert response.status_code == 204

        # Verify it's deleted
        response = api_client.get(url)
        assert response.status_code == 404

    def test_delete_expense_not_found(self, api_client):
        """Test deleting non-existent expense"""
        url = reverse("expenses:expense-detail", kwargs={"pk": 9999})
        response = api_client.delete(url)

        assert response.status_code == 404


# ============================================================================
# EXPENSE CUSTOM ACTIONS TESTS
# ============================================================================


@pytest.mark.django_db
class TestExpenseCustomActions:
    """Tests for custom actions on expenses"""

    def test_recent_expenses(self, api_client, user, category):
        """
        Test GET /api/expenses/recent/

        Should return expenses from last 7 days
        """
        # Local
        from expenses.models import Expense

        # Create expenses at different dates
        today = date.today()

        # Recent (within 7 days)
        Expense.objects.create(user=user, category=category, amount=10.00, date=today)
        Expense.objects.create(
            user=user, category=category, amount=20.00, date=today - timedelta(days=5)
        )

        # Old (more than 7 days ago)
        Expense.objects.create(
            user=user, category=category, amount=30.00, date=today - timedelta(days=10)
        )

        url = reverse("expenses:expense-recent")
        response = api_client.get(url)

        assert response.status_code == 200
        # Should only return recent expenses
        assert len(response.data) == 2

    def test_expense_statistics(self, api_client, expenses):
        """
        Test GET /api/expenses/statistics/

        Should return aggregated statistics
        Response fields in camelCase
        """
        url = reverse("expenses:expense-statistics")
        response = api_client.get(url)

        assert response.status_code == 200

        # Check fields exist (in camelCase!)
        assert "totalAmount" in response.data or "total_amount" in response.data
        assert "count" in response.data
        assert "averageAmount" in response.data or "average_amount" in response.data

        # Check values
        total = Decimal(
            str(response.data.get("totalAmount") or response.data.get("total_amount"))
        )
        count = response.data["count"]

        assert count == 5
        assert total > 0

    def test_statistics_empty(self, api_client):
        """Test statistics when no expenses exist"""
        url = reverse("expenses:expense-statistics")
        response = api_client.get(url)

        assert response.status_code == 200
        # Should handle null/empty gracefully
        count = response.data["count"]
        assert count == 0


# ============================================================================
# RUN THESE TESTS
# ============================================================================
#
# Run all expense API tests:
# pytest tests/test_api_expenses.py -v
#
# Run specific test class:
# pytest tests/test_api_expenses.py::TestExpenseCreate -v
#
# Run with output:
# pytest tests/test_api_expenses.py -v -s
#
# Run only filtering tests:
# pytest tests/test_api_expenses.py::TestExpenseList -v
