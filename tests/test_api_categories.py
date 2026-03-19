"""
API Tests for Category endpoints

What are we testing?
- HTTP methods (GET, POST, PUT, PATCH, DELETE)
- Status codes (200, 201, 400, 404)
- Response data structure
- Filtering and search
- Custom actions

Compare to C#:
[Fact]
public async Task TestGetCategories() {
    var response = await _client.GetAsync("/api/categories");
    response.EnsureSuccessStatusCode();
    var categories = await response.Content.ReadAsAsync<List<CategoryDto>>();
    Assert.NotEmpty(categories);
}
"""

# Third-party
import pytest
from django.urls import reverse

# ============================================================================
# CATEGORY LIST TESTS (GET /api/categories/)
# ============================================================================


@pytest.mark.django_db
class TestCategoryList:
    """Tests for GET /api/categories/"""

    def test_list_categories_empty(self, api_client):
        """Test listing categories when none exist"""
        url = reverse("expenses:category-list")
        response = api_client.get(url)

        assert response.status_code == 200
        assert response.data["count"] == 0
        assert response.data["results"] == []

    def test_list_categories(self, api_client, categories):
        """
        Test listing all categories

        Should return paginated list with simplified serializer
        """
        url = reverse("expenses:category-list")
        response = api_client.get(url)

        assert response.status_code == 200
        assert response.data["count"] == 3
        assert len(response.data["results"]) == 3

        # Check structure (using CategoryListSerializer)
        first = response.data["results"][0]
        assert "id" in first
        assert "name" in first
        # List serializer shouldn't have these
        assert "description" not in first
        assert "expenseCount" not in first

    def test_filter_by_name(self, api_client, categories):
        """
        Test filtering by exact name

        GET /api/categories/?name=Food
        """
        url = reverse("expenses:category-list")
        response = api_client.get(url, {"name": "Food"})

        assert response.status_code == 200
        assert response.data["count"] == 1
        assert response.data["results"][0]["name"] == "Food"

    def test_filter_by_name_icontains(self, api_client, categories):
        """
        Test filtering by name contains (case-insensitive)

        GET /api/categories/?name__icontains=tran
        """
        url = reverse("expenses:category-list")
        response = api_client.get(url, {"name__icontains": "tran"})

        assert response.status_code == 200
        assert response.data["count"] == 1
        assert response.data["results"][0]["name"] == "Transport"

    def test_search_categories(self, api_client, categories):
        """
        Test search functionality

        GET /api/categories/?search=food

        Should search in name and description
        """
        url = reverse("expenses:category-list")
        response = api_client.get(url, {"search": "food"})

        assert response.status_code == 200
        assert response.data["count"] >= 1
        # Should find "Food" category
        names = [cat["name"] for cat in response.data["results"]]
        assert "Food" in names

    def test_ordering_by_name(self, api_client, categories):
        """
        Test ordering by name

        GET /api/categories/?ordering=name
        """
        url = reverse("expenses:category-list")
        response = api_client.get(url, {"ordering": "name"})

        assert response.status_code == 200
        results = response.data["results"]
        names = [cat["name"] for cat in results]

        # Should be alphabetically sorted
        assert names == sorted(names)

    def test_ordering_by_name_descending(self, api_client, categories):
        """
        Test ordering by name descending

        GET /api/categories/?ordering=-name
        """
        url = reverse("expenses:category-list")
        response = api_client.get(url, {"ordering": "-name"})

        assert response.status_code == 200
        results = response.data["results"]
        names = [cat["name"] for cat in results]

        # Should be reverse alphabetically sorted
        assert names == sorted(names, reverse=True)


# ============================================================================
# CATEGORY CREATE TESTS (POST /api/categories/)
# ============================================================================


@pytest.mark.django_db
class TestCategoryCreate:
    """Tests for POST /api/categories/"""

    def test_create_category(self, api_client):
        """
        Test creating a valid category

        Compare to C#:
        var response = await _client.PostAsJsonAsync("/api/categories", dto);
        Assert.Equal(HttpStatusCode.Created, response.StatusCode);
        """
        url = reverse("expenses:category-list")
        data = {"name": "Health", "description": "Medical expenses"}

        response = api_client.post(url, data, format="json")

        assert response.status_code == 201
        assert response.data["name"] == "Health"
        assert response.data["description"] == "Medical expenses"
        assert "id" in response.data
        assert "created_at" in response.data

    def test_create_category_minimal(self, api_client):
        """Test creating category with only required fields"""
        url = reverse("expenses:category-list")
        data = {"name": "Shopping"}

        response = api_client.post(url, data, format="json")

        assert response.status_code == 201
        assert response.data["name"] == "Shopping"

    def test_create_category_name_too_short(self, api_client):
        """
        Test validation: name must be at least 3 characters

        Should return 400 Bad Request
        """
        url = reverse("expenses:category-list")
        data = {"name": "AB"}  # Too short

        response = api_client.post(url, data, format="json")

        assert response.status_code == 400
        assert "name" in response.data

    def test_create_category_duplicate_name(self, api_client, category):
        """
        Test validation: name must be unique

        Should return 400 Bad Request
        """
        url = reverse("expenses:category-list")
        data = {"name": category.name}  # Duplicate

        response = api_client.post(url, data, format="json")

        assert response.status_code == 400
        assert "name" in response.data

    def test_create_category_other_without_description(self, api_client):
        """
        Test validation: "Other" category requires description
        """
        url = reverse("expenses:category-list")
        data = {"name": "Other"}  # No description

        response = api_client.post(url, data, format="json")

        assert response.status_code == 400
        assert "description" in response.data


# ============================================================================
# CATEGORY RETRIEVE TESTS (GET /api/categories/{id}/)
# ============================================================================


@pytest.mark.django_db
class TestCategoryRetrieve:
    """Tests for GET /api/categories/{id}/"""

    def test_retrieve_category(self, api_client, category):
        """
        Test retrieving a single category

        Should return full CategorySerializer (not list serializer)
        """
        url = reverse("expenses:category-detail", kwargs={"pk": category.id})
        response = api_client.get(url)

        assert response.status_code == 200
        assert response.data["id"] == category.id
        assert response.data["name"] == category.name
        assert response.data["description"] == category.description

        # Detail serializer includes these
        assert "expense_count" in response.data
        assert "created_at" in response.data
        assert "updated_at" in response.data

    def test_retrieve_category_not_found(self, api_client):
        """
        Test retrieving non-existent category

        Should return 404 Not Found
        """
        url = reverse("expenses:category-detail", kwargs={"pk": 9999})
        response = api_client.get(url)

        assert response.status_code == 404


# ============================================================================
# CATEGORY UPDATE TESTS (PUT/PATCH /api/categories/{id}/)
# ============================================================================


@pytest.mark.django_db
class TestCategoryUpdate:
    """Tests for PUT and PATCH /api/categories/{id}/"""

    def test_update_category_put(self, api_client, category):
        """
        Test full update (PUT)

        Requires all fields
        """
        url = reverse("expenses:category-detail", kwargs={"pk": category.id})
        data = {"name": "Updated Food", "description": "Updated description"}

        response = api_client.put(url, data, format="json")

        assert response.status_code == 200
        assert response.data["name"] == "Updated Food"
        assert response.data["description"] == "Updated description"

    def test_update_category_patch(self, api_client, category):
        """
        Test partial update (PATCH)

        Only update specific fields
        """
        url = reverse("expenses:category-detail", kwargs={"pk": category.id})
        data = {"description": "New description only"}

        response = api_client.patch(url, data, format="json")

        assert response.status_code == 200
        assert response.data["name"] == category.name  # Unchanged
        assert response.data["description"] == "New description only"

    def test_update_category_not_found(self, api_client):
        """Test updating non-existent category"""
        url = reverse("expenses:category-detail", kwargs={"pk": 9999})
        data = {"name": "Test"}

        response = api_client.patch(url, data, format="json")

        assert response.status_code == 404


# ============================================================================
# CATEGORY DELETE TESTS (DELETE /api/categories/{id}/)
# ============================================================================


@pytest.mark.django_db
class TestCategoryDelete:
    """Tests for DELETE /api/categories/{id}/"""

    def test_delete_category(self, api_client, category):
        """
        Test deleting a category

        Should return 204 No Content
        """
        url = reverse("expenses:category-detail", kwargs={"pk": category.id})
        response = api_client.delete(url)

        assert response.status_code == 204

        # Verify it's deleted
        response = api_client.get(url)
        assert response.status_code == 404

    def test_delete_category_with_expenses(self, api_client, category, user):
        """
        Test deleting category with expenses

        Should fail (PROTECT constraint)
        """
        # Standard Library
        from datetime import date

        # Local
        from expenses.models import Expense

        # Create expense in category
        Expense.objects.create(
            user=user, category=category, amount=50.00, date=date.today()
        )

        url = reverse("expenses:category-detail", kwargs={"pk": category.id})
        response = api_client.delete(url)

        # Should fail with 400 or 409 (depends on DRF version)
        assert response.status_code in [400, 409]

    def test_delete_category_not_found(self, api_client):
        """Test deleting non-existent category"""
        url = reverse("expenses:category-detail", kwargs={"pk": 9999})
        response = api_client.delete(url)

        assert response.status_code == 400


# ============================================================================
# CATEGORY CUSTOM ACTION TESTS
# ============================================================================


@pytest.mark.django_db
class TestCategorySummary:
    """Tests for GET /api/categories/summary/"""

    def test_summary_action(self, api_client, categories, user):
        """
        Test custom summary action

        Should return total categories and expense counts
        """
        # Standard Library
        from datetime import date

        # Local
        from expenses.models import Expense

        # Create expenses
        Expense.objects.create(
            user=user, category=categories[0], amount=10.00, date=date.today()  # Food
        )
        Expense.objects.create(
            user=user, category=categories[0], amount=20.00, date=date.today()  # Food
        )

        url = reverse("expenses:category-summary")
        response = api_client.get(url)

        assert response.status_code == 200
        assert "total_categories" in response.data
        assert "categories" in response.data
        assert response.data["total_categories"] == 3

        # Check first category has expense count
        food_cat = next(c for c in response.data["categories"] if c["name"] == "Food")
        assert food_cat["expense_count"] == 2


# ============================================================================
# RUN THESE TESTS
# ============================================================================
#
# Run all category API tests:
# pytest tests/test_api_categories.py -v
#
# Run specific test class:
# pytest tests/test_api_categories.py::TestCategoryCreate -v
#
# Run with output:
# pytest tests/test_api_categories.py -v -s
