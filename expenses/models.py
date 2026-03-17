"""
Models for the Expense Tracker API

In Django, models are Python classes that represent database tables.
Each model class becomes a table, and each attribute becomes a column.

Compare to C#:
- Django Model = Entity class in Entity Framework
- Field types = Data annotations / Fluent API configuration
- models.Model = inheriting from a base entity class
"""

# Third-party
from django.contrib.auth.models import User
from django.db import models


class Category(models.Model):
    """
    Category model - Represents expense categories (Food, Transport, etc.)
    Why this exists:
    - Organizes expenses into logical groups
    - Allows filtering expenses by category
    - Makes reporting easier (total spent per category)

    Compare to C#:
    public class Category {
        public int Id { get; set; }              // Auto-created in Django
        public string Name { get; set; }
        public string Description { get; set; }
        public DateTime CreatedAt { get; set; }
    }
    """

    # Fields (these become database columns)

    name = models.CharField(
        max_length=100,
        unique=True,  # No duplicate category names
        help_text="Category name (e.g., Food, Transport, Entertainment)",
    )
    # CharField = VARCHAR in SQL, like string in C#
    # max_length is required for CharField
    # unique=True creates a UNIQUE constraint in database

    description = models.TextField(
        blank=True,  # Optional field (can be empty in forms)
        default="",
        help_text="Optional description of the category",
    )
    # TextField = TEXT in SQL, for longer text
    # blank=True: validation allows empty values
    # null=True: database allows NULL

    created_at = models.DateTimeField(
        auto_now_add=True, help_text="Timestamp when category was created"
    )
    # auto_now_add=True: automatically sets to NOW when created
    # Like [DatabaseGenerated(DatabaseGeneratedOption.Identity)] in C#

    updated_at = models.DateTimeField(
        auto_now=True, help_text="Timestamp when category was last updated"
    )
    # auto_now=True: automatically updates to NOW on every save

    # Meta class - additional configuration
    class Meta:
        """
        Meta options for the model

        Compare to C# Entity Framework Fluent API:
        modelBuilder.Entity<Category>()
            .ToTable("categories")
            .HasIndex(c => c.Name);
        """

        verbose_name = "Category"  # Singular name for admin
        verbose_name_plural = "Categories"  # Plural name for admin
        ordering = ["name"]  # Default ordering (alphabetically by name)
        db_table = "categories"  # Explicit table name (optional)

    # String representation
    def __str__(self):
        """
        String representation of the model

        Compare to C#:
        public override string ToString() {
            return Name;
        }

        Why this exists:
        - Used in Django admin panel
        - Used in shell/debugging
        - Makes objects readable in logs
        """
        return self.name

    # Custom methods (you can add business logic here)
    def get_expense_count(self):
        """
        Returns the number of expenses in this category

        Why this exists:
        - Business logic method (like a method in C# entity)
        - Can be used in serializers or views
        """
        return self.expenses.count()


class Expense(models.Model):
    """
    Expense model - Represents individual expense records

    Why this exists:
    - Core model of our API
    - Stores all expense transactions
    - Links to Category and User

    Compare to C#:
    public class Expense {
        public int Id { get; set; }
        public int CategoryId { get; set; }
        public Category Category { get; set; }  // Navigation property
        public decimal Amount { get; set; }
        public string Description { get; set; }
        public DateTime Date { get; set; }
    }
    """

    # Foreign Key to User (who owns this expense)
    user = models.ForeignKey(
        User,  # Django's built-in User model
        on_delete=models.CASCADE,  # If user is deleted, delete their expenses
        related_name="expenses",  # Access user's expenses via user.expenses.all()
        help_text="User who created this expense",
    )
    # ForeignKey = Foreign Key in SQL
    # Compare to C#: public int UserId { get; set; }
    # on_delete=models.CASCADE: like ON DELETE CASCADE in SQL
    # related_name: like [InverseProperty("Expenses")] in C#

    # Foreign Key to Category
    category = models.ForeignKey(
        Category,
        on_delete=models.PROTECT,  # Cannot delete category if it has expenses
        related_name="expenses",  # Access category's expenses via category.expenses.all()
        help_text="Category of this expense",
    )
    # on_delete=models.PROTECT: prevents deletion if related objects exist
    # Like adding a constraint that prevents deletion

    amount = models.DecimalField(
        max_digits=10,  # Total digits (including decimals)
        decimal_places=2,  # Digits after decimal point
        help_text="Expense amount (e.g., 45.50)",
    )
    # DecimalField = DECIMAL in SQL
    # max_digits=10, decimal_places=2 means: 99999999.99 max
    # Like decimal(10,2) in SQL or decimal in C#

    description = models.TextField(help_text="Description of the expense")
    # TextField for longer descriptions

    date = models.DateField(help_text="Date when expense occurred")
    # DateField = DATE in SQL (date only, no time)
    # Like DateTime in C# but stores only date part

    created_at = models.DateTimeField(
        auto_now_add=True, help_text="Timestamp when expense was created"
    )

    updated_at = models.DateTimeField(
        auto_now=True, help_text="Timestamp when expense was last updated"
    )

    # Meta configuration
    class Meta:
        verbose_name = "Expense"
        verbose_name_plural = "Expenses"
        ordering = ["-date", "-created_at"]  # Most recent first (- means descending)
        db_table = "expenses"

        # Indexes for better query performance
        indexes = [
            models.Index(fields=["date"]),  # Index on date for faster filtering
            models.Index(fields=["category", "date"]),  # Composite index
        ]
        # Compare to C#: [Index(nameof(Date))]

    def __str__(self):
        """
        String representation

        Returns: "Food - $45.50 on 2024-03-10"
        """
        return f"{self.category.name} - ${self.amount} on {self.date}"

    # Custom properties (like computed properties in C#)
    @property
    def is_recent(self):
        """
        Check if expense is from last 7 days

        Compare to C#:
        public bool IsRecent => Date >= DateTime.Now.AddDays(-7);

        Why use @property:
        - Makes it accessible like expense.is_recent (no parentheses)
        - Can be used in serializers
        """
        # Standard Library
        from datetime import date, timedelta

        return self.date >= date.today() - timedelta(days=7)
