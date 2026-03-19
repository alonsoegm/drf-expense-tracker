"""
Serializer Tests for Category and Expense

What are we testing?
- Serialization (model → JSON)
- Deserialization (JSON → model)
- Validation rules
- Custom validation methods
- Error messages

Compare to C#:
[Fact]
public void TestDtoValidation() {
    var dto = new CategoryDto { Name = "AB" };
    var validationResults = Validator.Validate(dto);
    Assert.False(validationResults.IsValid);
}
"""

# Standard Library
from datetime import date, timedelta
from decimal import Decimal

# Third-party
import pytest

# Local
from expenses.models import Expense
from expenses.serializers import (
    CategoryListSerializer,
    CategorySerializer,
    ExpenseListSerializer,
    ExpenseSerializer,
)

# ============================================================================
# CATEGORY SERIALIZER TESTS
# ============================================================================


@pytest.mark.django_db
class TestCategorySerializer:
    """Tests for CategorySerializer"""

    def test_serialize_category(self, category):
        """
        Test serializing a Category model to JSON

        Model → Serializer → JSON

        Compare to C#:
        var dto = _mapper.Map<CategoryDto>(category);
        """
        serializer = CategorySerializer(category)
        data = serializer.data

        assert data["id"] == category.id
        assert data["name"] == category.name
        assert data["description"] == category.description
        assert "expense_count" in data
        assert "created_at" in data
        assert "updated_at" in data

    def test_deserialize_valid_category(self):
        """
        Test deserializing valid JSON to Category

        JSON → Serializer → Model
        """
        data = {"name": "Food", "description": "Food and groceries"}

        serializer = CategorySerializer(data=data)
        assert serializer.is_valid()

        category = serializer.save()
        assert category.name == "Food"
        assert category.description == "Food and groceries"

    def test_deserialize_minimal_category(self):
        """Test deserializing with only required fields"""
        data = {"name": "Transport"}

        serializer = CategorySerializer(data=data)
        assert serializer.is_valid()

        category = serializer.save()
        assert category.name == "Transport"
        assert category.description == ""

    def test_validate_name_too_short(self):
        """
        Test custom validation: name must be at least 3 characters

        validate_name() should reject names < 3 chars
        """
        data = {"name": "AB"}  # Only 2 characters

        serializer = CategorySerializer(data=data)
        assert not serializer.is_valid()
        assert "name" in serializer.errors
        assert "at least 3 characters" in str(serializer.errors["name"])

    def test_validate_name_exactly_3_chars(self):
        """Test that 3 characters is valid (boundary test)"""
        data = {"name": "ABC"}

        serializer = CategorySerializer(data=data)
        assert serializer.is_valid()

    def test_validate_name_strips_whitespace(self):
        """
        Test that validate_name strips whitespace

        "  Food  " → "Food"
        """
        data = {"name": "  Food  "}

        serializer = CategorySerializer(data=data)
        assert serializer.is_valid()

        category = serializer.save()
        assert category.name == "Food"  # No whitespace

    def test_validate_name_title_case(self):
        """
        Test that validate_name converts to title case

        "food and drinks" → "Food And Drinks"
        """
        data = {"name": "food and drinks"}

        serializer = CategorySerializer(data=data)
        assert serializer.is_valid()

        category = serializer.save()
        assert category.name == "Food And Drinks"

    def test_validate_other_category_requires_description(self):
        """
        Test object-level validation

        validate() should require description for "Other" category
        """
        data = {"name": "Other"}  # No description

        serializer = CategorySerializer(data=data)
        assert not serializer.is_valid()
        assert "description" in serializer.errors

    def test_validate_other_category_with_description(self):
        """Test that "Other" category is valid with description"""
        data = {"name": "Other", "description": "Miscellaneous expenses"}

        serializer = CategorySerializer(data=data)
        assert serializer.is_valid()

    def test_expense_count_method_field(self, category, user):
        """
        Test SerializerMethodField: expenseCount

        Should return count of expenses in category
        """
        # Create 2 expenses in category
        Expense.objects.create(
            user=user, category=category, amount=10.00, date=date.today()
        )
        Expense.objects.create(
            user=user, category=category, amount=20.00, date=date.today()
        )

        serializer = CategorySerializer(category)
        assert serializer.data["expense_count"] == 2

    def test_update_category(self, category):
        """
        Test updating an existing category

        Compare to C#:
        _mapper.Map(dto, existingCategory);
        """
        data = {"name": "Updated Food", "description": "Updated description"}

        serializer = CategorySerializer(category, data=data)
        assert serializer.is_valid()

        updated = serializer.save()
        assert updated.id == category.id
        assert updated.name == "Updated Food"
        assert updated.description == "Updated description"


@pytest.mark.django_db
class TestCategoryListSerializer:
    """Tests for CategoryListSerializer (simplified)"""

    def test_serialize_category_list(self, categories):
        """
        Test serializing multiple categories

        Should only include id and name (simplified)
        """
        serializer = CategoryListSerializer(categories, many=True)
        data = serializer.data

        assert len(data) == 3
        assert "id" in data[0]
        assert "name" in data[0]
        # Should NOT have description, expense_count, etc.
        assert "description" not in data[0]
        assert "expense_count" not in data[0]


# ============================================================================
# EXPENSE SERIALIZER TESTS
# ============================================================================


@pytest.mark.django_db
class TestExpenseSerializer:
    """Tests for ExpenseSerializer"""

    def test_serialize_expense(self, expense):
        """
        Test serializing an Expense model to JSON
        """
        serializer = ExpenseSerializer(expense)
        data = serializer.data

        assert data["id"] == expense.id
        assert Decimal(data["amount"]) == expense.amount
        assert data["description"] == expense.description
        assert data["date"] == str(expense.date)
        assert "category_detail" in data
        assert "category_name" in data
        assert "username" in data

    def test_deserialize_valid_expense(self, category, user):
        """
        Test deserializing valid JSON to Expense
        """
        data = {
            "category_id": category.id,
            "amount": 45.50,
            "description": "Grocery shopping",
            "date": "2024-03-19",
        }

        serializer = ExpenseSerializer(
            data=data, context={"request": type("Request", (), {"user": user})()}
        )
        assert serializer.is_valid(), serializer.errors

        # Need to pass user in save (since it's not in data)
        expense = serializer.save(user=user)
        assert expense.category == category
        assert expense.amount == Decimal("45.50")
        assert expense.description == "Grocery shopping"

    def test_validate_amount_positive(self, category):
        """
        Test that amount must be greater than zero

        validate_amount() should reject negative/zero amounts
        """
        data = {
            "category_id": category.id,
            "amount": 0,  # Zero not allowed
            "date": "2024-03-19",
        }

        serializer = ExpenseSerializer(data=data)
        assert not serializer.is_valid()
        assert "amount" in serializer.errors
        assert "greater than or equal to 0.01" in str(serializer.errors["amount"])

    def test_validate_amount_negative(self, category):
        """Test that negative amounts are rejected"""
        data = {"category_id": category.id, "amount": -10.00, "date": "2024-03-19"}

        serializer = ExpenseSerializer(data=data)
        assert not serializer.is_valid()
        assert "amount" in serializer.errors

    def test_validate_amount_too_large(self, category):
        """
        Test that amounts over 1,000,000 are rejected
        """
        data = {
            "category_id": category.id,
            "amount": 1_000_001,  # Over limit
            "date": "2024-03-19",
        }

        serializer = ExpenseSerializer(data=data)
        assert not serializer.is_valid()
        assert "amount" in serializer.errors
        assert "1,000,000" in str(serializer.errors["amount"])

    def test_validate_amount_exactly_limit(self, category, user):
        """Test that exactly 1,000,000 is valid (boundary test)"""
        data = {
            "category_id": category.id,
            "amount": 1_000_000,
            "description": "Test expense",
            "date": "2024-03-19",
        }

        serializer = ExpenseSerializer(
            data=data, context={"request": type("Request", (), {"user": user})()}
        )
        assert serializer.is_valid()

    def test_validate_date_future(self, category):
        """
        Test that future dates are rejected

        validate_date() should reject dates in the future
        """
        future_date = date.today() + timedelta(days=1)

        data = {"category_id": category.id, "amount": 50.00, "date": str(future_date)}

        serializer = ExpenseSerializer(data=data)
        assert not serializer.is_valid()
        assert "date" in serializer.errors
        assert "future" in str(serializer.errors["date"]).lower()

    def test_validate_date_today(self, category, user):
        """Test that today's date is valid"""
        data = {
            "category_id": category.id,
            "amount": 50.00,
            "description": "Test expense",
            "date": str(date.today()),
        }

        serializer = ExpenseSerializer(
            data=data, context={"request": type("Request", (), {"user": user})()}
        )
        assert serializer.is_valid()

    def test_validate_date_past(self, category, user):
        """Test that past dates are valid"""
        past_date = date.today() - timedelta(days=30)

        data = {
            "category_id": category.id,
            "amount": 50.00,
            "description": "Test expense",
            "date": str(past_date),
        }

        serializer = ExpenseSerializer(
            data=data, context={"request": type("Request", (), {"user": user})()}
        )
        assert serializer.is_valid()

    def test_validate_duplicate_expense(self, category, user):
        """
        Test duplicate detection

        validate() should prevent creating identical expenses
        (same category, amount, date)
        """
        # Create first expense
        Expense.objects.create(
            user=user,
            category=category,
            amount=50.00,
            description="Original",
            date=date.today(),
        )

        # Try to create duplicate (same category, amount, date)
        data = {
            "category_id": category.id,
            "amount": 50.00,
            "description": "Duplicate",  # Different description OK
            "date": str(date.today()),
        }

        serializer = ExpenseSerializer(
            data=data, context={"request": type("Request", (), {"user": user})()}
        )
        assert not serializer.is_valid()
        assert "non_field_errors" in serializer.errors
        assert "similar expense" in str(serializer.errors["non_field_errors"]).lower()

    def test_different_amount_not_duplicate(self, category, user):
        """Test that different amounts are not considered duplicates"""
        Expense.objects.create(
            user=user, category=category, amount=50.00, date=date.today()
        )

        # Different amount - should be valid
        data = {
            "category_id": category.id,
            "amount": 51.00,  # Different!
            "description": "Test expense",
            "date": str(date.today()),
        }

        serializer = ExpenseSerializer(
            data=data, context={"request": type("Request", (), {"user": user})()}
        )
        assert serializer.is_valid()

    def test_nested_category_detail(self, expense):
        """
        Test nested serializer: categoryDetail

        Should include full category object
        """
        serializer = ExpenseSerializer(expense)
        data = serializer.data

        assert "category_detail" in data
        assert data["category_detail"]["id"] == expense.category.id
        assert data["category_detail"]["name"] == expense.category.name

    def test_category_name_field(self, expense):
        """
        Test convenience field: category_name

        Should return category name directly
        """
        serializer = ExpenseSerializer(expense)
        assert serializer.data["category_name"] == expense.category.name

    def test_username_field(self, expense):
        """
        Test convenience field: username

        Should return user's username
        """
        serializer = ExpenseSerializer(expense)
        assert serializer.data["username"] == expense.user.username


@pytest.mark.django_db
class TestExpenseListSerializer:
    """Tests for ExpenseListSerializer (simplified)"""

    def test_serialize_expense_list(self, expenses):
        """
        Test serializing multiple expenses

        Should use simplified fields (no nested objects)
        """
        serializer = ExpenseListSerializer(expenses, many=True)
        data = serializer.data

        assert len(data) == 5
        assert "id" in data[0]
        assert "category_name" in data[0]
        assert "amount" in data[0]
        # Should NOT have category_detail (nested)
        assert "category_detail" not in data[0]


# ============================================================================
# RUN THESE TESTS
# ============================================================================
#
# Run all serializer tests:
# pytest tests/test_serializers.py -v
#
# Run specific test class:
# pytest tests/test_serializers.py::TestCategorySerializer -v
#
# Run specific test:
# pytest tests/test_serializers.py::TestExpenseSerializer::test_validate_amount_positive -v
