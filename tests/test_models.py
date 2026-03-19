"""
Model Tests for Category and Expense

What are we testing?
- Model creation
- String representations
- Model methods
- Field constraints
- Relationships

Compare to C#:
[Fact]
public void TestCategoryCreation() {
    var category = new Category { Name = "Food" };
    Assert.Equal("Food", category.Name);
}
"""

# Standard Library
from datetime import date, timedelta
from decimal import Decimal

# Third-party
import pytest
from django.db import IntegrityError

# Local
from expenses.models import Category, Expense

# ============================================================================
# CATEGORY MODEL TESTS
# ============================================================================


@pytest.mark.django_db
class TestCategoryModel:
    """
    Tests for the Category model

    @pytest.mark.django_db tells pytest to:
    - Create test database
    - Run migrations
    - Clean up after tests

    Compare to C#:
    [Collection("Database")]
    public class CategoryTests { }
    """

    def test_create_category(self):
        """
        Test creating a category with all fields

        Compare to C#:
        [Fact]
        public void TestCreateCategory() {
            var category = new Category {
                Name = "Food",
                Description = "Food and groceries"
            };
            Assert.Equal("Food", category.Name);
        }
        """
        category = Category.objects.create(
            name="Food", description="Food and groceries"
        )

        assert category.name == "Food"
        assert category.description == "Food and groceries"
        assert category.id is not None
        assert category.created_at is not None
        assert category.updated_at is not None

    def test_create_category_minimal(self):
        """Test creating category with only required fields"""
        category = Category.objects.create(name="Transport")

        assert category.name == "Transport"
        assert category.description == ""  # Default value

    def test_category_str_representation(self):
        """
        Test __str__ method

        This is what shows in Django admin and shell

        Compare to C#:
        [Fact]
        public void TestToString() {
            var category = new Category { Name = "Food" };
            Assert.Equal("Food", category.ToString());
        }
        """
        category = Category.objects.create(name="Entertainment")
        assert str(category) == "Entertainment"

    def test_category_name_unique(self):
        """
        Test that category names must be unique

        Should raise IntegrityError on duplicate
        """
        Category.objects.create(name="Food")

        with pytest.raises(IntegrityError):
            # Trying to create another "Food" category
            Category.objects.create(name="Food")

    def test_category_ordering(self):
        """
        Test default ordering (should be by name)

        Compare to C#:
        var categories = _context.Categories.OrderBy(c => c.Name).ToList();
        """
        Category.objects.create(name="Zebra")
        Category.objects.create(name="Apple")
        Category.objects.create(name="Mango")

        categories = list(Category.objects.all())

        assert categories[0].name == "Apple"
        assert categories[1].name == "Mango"
        assert categories[2].name == "Zebra"

    def test_get_expense_count_zero(self):
        """Test get_expense_count when no expenses exist"""
        category = Category.objects.create(name="Food")
        assert category.get_expense_count() == 0

    def test_get_expense_count_with_expenses(self, user):
        """
        Test get_expense_count with expenses

        Uses 'user' fixture from conftest.py
        """
        category = Category.objects.create(name="Food")

        # Create 3 expenses in this category
        Expense.objects.create(
            user=user, category=category, amount=10.00, date=date.today()
        )
        Expense.objects.create(
            user=user, category=category, amount=20.00, date=date.today()
        )
        Expense.objects.create(
            user=user, category=category, amount=30.00, date=date.today()
        )

        assert category.get_expense_count() == 3

    def test_category_timestamps_auto_set(self):
        """Test that timestamps are set automatically"""
        category = Category.objects.create(name="Food")

        assert category.created_at is not None
        assert category.updated_at is not None
        assert abs(category.created_at - category.updated_at) < timedelta(seconds=1)

    def test_category_timestamps_update(self):
        """Test that updated_at changes on save"""
        # Standard Library
        import time

        category = Category.objects.create(name="Food")
        original_updated = category.updated_at

        time.sleep(0.01)  # Small delay

        category.description = "Updated description"
        category.save()

        assert category.updated_at > original_updated


# ============================================================================
# EXPENSE MODEL TESTS
# ============================================================================


@pytest.mark.django_db
class TestExpenseModel:
    """Tests for the Expense model"""

    def test_create_expense(self, user, category):
        """
        Test creating an expense with all fields

        Uses fixtures: user, category
        """
        expense = Expense.objects.create(
            user=user,
            category=category,
            amount=Decimal("45.50"),
            description="Grocery shopping",
            date=date(2024, 3, 19),
        )

        assert expense.user == user
        assert expense.category == category
        assert expense.amount == Decimal("45.50")
        assert expense.description == "Grocery shopping"
        assert expense.date == date(2024, 3, 19)
        assert expense.id is not None

    def test_create_expense_minimal(self, user, category):
        """Test creating expense with only required fields"""
        expense = Expense.objects.create(
            user=user, category=category, amount=100.00, date=date.today()
        )

        assert expense.description == ""  # Default value

    def test_expense_str_representation(self, user, category):
        """
        Test __str__ method

        Format: "Food - $45.50 on 2024-03-19"
        """
        expense = Expense.objects.create(
            user=user,
            category=category,
            amount=Decimal("45.50"),
            description="Test",
            date=date(2024, 3, 19),
        )

        expected = f"{category.name} - $45.50 on 2024-03-19"
        assert str(expense) == expected

    def test_expense_category_relationship(self, user, category):
        """
        Test ForeignKey relationship to Category

        Compare to C#:
        var expense = new Expense { CategoryId = category.Id };
        Assert.Equal(category.Name, expense.Category.Name);
        """
        expense = Expense.objects.create(
            user=user, category=category, amount=50.00, date=date.today()
        )

        # Can access category through relationship
        assert expense.category.name == category.name

    def test_expense_user_relationship(self, user, category):
        """Test ForeignKey relationship to User"""
        expense = Expense.objects.create(
            user=user, category=category, amount=50.00, date=date.today()
        )

        # Can access user through relationship
        assert expense.user.username == user.username

    def test_category_expenses_reverse_relationship(self, user, category):
        """
        Test reverse relationship from Category to Expenses

        category.expenses.all() should return all expenses in that category

        Compare to C#:
        var expenses = category.Expenses.ToList();
        """
        # Create 2 expenses in category
        Expense.objects.create(
            user=user, category=category, amount=10.00, date=date.today()
        )
        Expense.objects.create(
            user=user, category=category, amount=20.00, date=date.today()
        )

        # Access expenses through reverse relationship
        expenses = category.expenses.all()

        assert expenses.count() == 2

    def test_delete_category_with_expenses_protected(self, user, category):
        """
        Test that deleting a category with expenses is prevented

        on_delete=models.PROTECT should raise error

        Compare to C#:
        [Fact]
        public void TestCascadeDelete() {
            // EF Core: DeleteBehavior.Restrict
        }
        """
        Expense.objects.create(
            user=user, category=category, amount=50.00, date=date.today()
        )

        # Third-party
        from django.db.models import ProtectedError

        with pytest.raises(ProtectedError):
            category.delete()

    def test_delete_category_without_expenses_allowed(self, category):
        """Test that deleting a category without expenses works"""
        category_id = category.id
        category.delete()

        # Verify it's deleted
        assert not Category.objects.filter(id=category_id).exists()

    def test_delete_user_deletes_expenses(self, user, category):
        """
        Test that deleting a user deletes their expenses

        on_delete=models.CASCADE for user field
        """
        expense = Expense.objects.create(
            user=user, category=category, amount=50.00, date=date.today()
        )

        expense_id = expense.id
        user.delete()

        # Expense should be deleted too
        assert not Expense.objects.filter(id=expense_id).exists()

    def test_expense_amount_decimal_precision(self, user, category):
        """
        Test that amount is stored with correct precision

        DecimalField(max_digits=10, decimal_places=2)
        """
        expense = Expense.objects.create(
            user=user, category=category, amount=Decimal("123.45"), date=date.today()
        )

        # Fetch from DB
        expense.refresh_from_db()

        assert expense.amount == Decimal("123.45")
        assert isinstance(expense.amount, Decimal)

    def test_expense_ordering(self, user, category):
        """
        Test default ordering (should be by -date, -created_at)

        Most recent expenses first
        """
        expense1 = Expense.objects.create(
            user=user, category=category, amount=10.00, date=date(2024, 3, 15)
        )
        expense2 = Expense.objects.create(
            user=user, category=category, amount=20.00, date=date(2024, 3, 19)
        )
        expense3 = Expense.objects.create(
            user=user, category=category, amount=30.00, date=date(2024, 3, 17)
        )

        expenses = list(Expense.objects.all())

        # Should be ordered by date descending
        assert expenses[0].id == expense2.id  # 2024-03-19
        assert expenses[1].id == expense3.id  # 2024-03-17
        assert expenses[2].id == expense1.id  # 2024-03-15


# ============================================================================
# RUN THESE TESTS
# ============================================================================
#
# Run all tests:
# pytest
#
# Run only model tests:
# pytest tests/test_models.py
#
# Run specific test:
# pytest tests/test_models.py::TestCategoryModel::test_create_category
#
# Run with verbose output:
# pytest -v
#
# Run with print statements:
# pytest -s
