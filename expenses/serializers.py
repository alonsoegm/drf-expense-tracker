"""
Serializers for the Expense Tracker API

What are Serializers?
- Convert Django models to JSON (serialization)
- Convert JSON to Django models (deserialization)
- Validate incoming data
- Handle nested relationships

Compare to C#:
- Serializers = DTOs + AutoMapper + Data Annotations (validation)
- ModelSerializer = Automatic mapping like AutoMapper conventions
- Field declarations = DTO properties
- validate_* methods = Custom validation attributes

Why we need them:
- Models contain database-specific logic
- Serializers define what data the API exposes
- Allows different representations for different endpoints
"""

# Third-party
from rest_framework import serializers

from .models import Category, Expense


class CategorySerializer(serializers.ModelSerializer):
    """
    Serializer for Category model

    ModelSerializer automatically creates fields based on the model.
    Like using AutoMapper with default conventions in C#.

    Compare to C#:
    public class CategoryDto {
        public int Id { get; set; }
        public string Name { get; set; }
        public string Description { get; set; }
        public DateTime CreatedAt { get; set; }
        public DateTime UpdatedAt { get; set; }
    }

    What this does:
    - Defines which model fields to include in API responses
    - Handles validation automatically (based on model field definitions)
    - Provides create() and update() methods automatically
    """

    # Custom read-only field (computed property)
    expense_count = serializers.SerializerMethodField(
        help_text="Number of expenses in this category"
    )
    # SerializerMethodField = Custom computed property
    # Requires a get_<field_name> method below
    # Like a [NotMapped] computed property in C# Entity

    class Meta:
        """
        Meta class configuration

        This tells DRF:
        - Which model to serialize
        - Which fields to include
        - Read-only fields
        - Extra kwargs (like validation rules)
        """

        model = Category
        # The model this serializer is for

        fields = [
            "id",  # Primary key (auto-included)
            "name",  # From model
            "description",  # From model
            "expense_count",  # Custom field (SerializerMethodField)
            "created_at",  # Timestamp
            "updated_at",  # Timestamp
        ]
        # fields = '__all__'  # Alternative: include ALL model fields

        read_only_fields = ["id", "created_at", "updated_at"]
        # These fields cannot be modified via API
        # Like [Editable(false)] in C#

        extra_kwargs = {
            "name": {
                "required": True,
                "allow_blank": False,
                "max_length": 100,
            },
            "description": {
                "required": False,
                "allow_blank": True,
            },
        }
        # Additional validation rules
        # Like [Required], [MaxLength] attributes in C#

    def get_expense_count(self, obj):
        """
        Method for the SerializerMethodField 'expense_count'

        Args:
            obj: The Category instance being serialized

        Returns:
            int: Number of expenses in this category

        Why this exists:
        - Provides computed/calculated data in API responses
        - Can access related objects (obj.expenses)
        - Useful for summary information

        Compare to C#:
        public int ExpenseCount => Expenses?.Count ?? 0;
        """
        return obj.get_expense_count()
        # Calls the model method we created in models.py

    def validate_name(self, value):
        """
        Custom validation for the 'name' field

        Method naming: validate_<field_name>

        Args:
            value: The value to validate

        Returns:
            The validated value (possibly modified)

        Raises:
            serializers.ValidationError: If validation fails

        Compare to C#:
        [CustomValidation(typeof(CategoryValidator), "ValidateName")]
        public string Name { get; set; }

        Why this exists:
        - Add custom business logic validation
        - Goes beyond model field constraints
        """
        if len(value.strip()) < 3:
            raise serializers.ValidationError(
                "Category name must be at least 3 characters long."
            )
        return value.strip().title()  # Return cleaned value (Title Case)

    def validate(self, attrs):
        """
        Object-level validation (validates multiple fields together)

        Args:
            attrs: Dictionary of all field values

        Returns:
            The validated attributes dictionary

        Compare to C#:
        public IEnumerable<ValidationResult> Validate(ValidationContext context) {
            // Multi-field validation
        }

        Why this exists:
        - Validate relationships between fields
        - Business logic that involves multiple fields
        """
        # Example: Ensure description is provided if name is generic
        if attrs.get("name", "").lower() == "other" and not attrs.get("description"):
            raise serializers.ValidationError(
                {"description": "Description is required for 'Other' category"}
            )

        return attrs


class CategoryListSerializer(serializers.ModelSerializer):
    """
    Simplified serializer for listing categories (less data)

    Why multiple serializers?
    - List views often need less data than detail views
    - Improves performance (less data transferred)
    - Different endpoints can use different serializers

    Compare to C#:
    public class CategoryListDto {  // Simpler than CategoryDto
        public int Id { get; set; }
        public string Name { get; set; }
    }
    """

    class Meta:
        model = Category
        fields = ["id", "name"]  # Only essential fields for list view
        read_only_fields = ["id"]


class ExpenseSerializer(serializers.ModelSerializer):
    """
    Serializer for Expense model

    This serializer includes:
    - All expense fields
    - Nested category data (read-only)
    - Custom validation
    - User association

    Compare to C#:
    public class ExpenseDto {
        public int Id { get; set; }
        public CategoryDto Category { get; set; }  // Nested object
        public decimal Amount { get; set; }
        public string Description { get; set; }
        public DateTime Date { get; set; }
        public string Username { get; set; }
    }
    """

    # Nested serializer - shows full category object in response
    category_detail = CategoryListSerializer(
        source="category",  # The model field to serialize
        read_only=True,  # Only for responses, not for input
    )
    # source='category': Maps to the category ForeignKey in model
    # read_only=True: Cannot set this via API (use category_id instead)

    # Show category name directly (alternative to nested object)
    category_name = serializers.CharField(source="category.name", read_only=True)
    # Accesses related object field: expense.category.name
    # Like Include() in Entity Framework

    # Show username instead of user ID
    username = serializers.CharField(source="user.username", read_only=True)

    # Write-only field for creating/updating
    category_id: serializers.PrimaryKeyRelatedField = serializers.PrimaryKeyRelatedField(  # type: ignore[type-arg]
        queryset=Category.objects.all(),
        source="category",
        write_only=True,  # Only for input (POST/PUT), not in response
    )
    # PrimaryKeyRelatedField: Accepts category ID in requests
    # queryset: Validates that the ID exists in database
    # write_only=True: Won't appear in GET responses

    class Meta:
        model = Expense
        fields = [
            "id",
            "user",  # Will be set automatically from request.user
            "username",  # Read-only, shows user's name
            "category_id",  # Write-only, for creating/updating
            "category_detail",  # Read-only, nested category object
            "category_name",  # Read-only, just the name
            "amount",
            "description",
            "date",
            "created_at",
            "updated_at",
        ]

        examples = {
            "create_expense": {
                "summary": "Create a new expense",
                "value": {
                    "category_id": 1,
                    "amount": 45.50,
                    "description": "Lunch at restaurant",
                    "date": "2024-03-19",
                },
            }
        }

        read_only_fields = ["id", "user", "username", "created_at", "updated_at"]

        extra_kwargs = {
            "amount": {
                "required": True,
                "min_value": 0.01,  # Must be positive
                "max_digits": 10,
                "decimal_places": 2,
            },
            "description": {
                "required": True,
                "allow_blank": False,
                "max_length": 500,
            },
            "date": {
                "required": True,
            },
        }

    def validate_amount(self, value):
        """
        Validate expense amount

        Compare to C#:
        [Range(0.01, double.MaxValue, ErrorMessage = "Amount must be positive")]
        public decimal Amount { get; set; }
        """
        if value <= 0:
            raise serializers.ValidationError("Amount must be greater than zero.")

        if value > 1000000:  # Example business rule
            raise serializers.ValidationError("Amount cannot exceed 1,000,000.")

        return value

    def validate_date(self, value):
        """
        Validate expense date

        Business rule: Cannot create expenses in the future
        """
        # Standard Library
        from datetime import date

        if value > date.today():
            raise serializers.ValidationError(
                "Cannot create expenses for future dates."
            )

        return value

    def validate(self, attrs):
        """
        Object-level validation

        Example: Check for duplicate expenses
        """
        # Check if similar expense exists (same user, category, amount, date)
        request = self.context.get("request")
        user = getattr(request, "user", None) if request else None
        category = attrs.get("category")
        amount = attrs.get("amount")
        date = attrs.get("date")

        # Only check for duplicates on creation (not updates)
        if not self.instance and user and user.is_authenticated:
            similar_expense = Expense.objects.filter(
                user=user, category=category, amount=amount, date=date
            ).exists()

            if similar_expense:
                raise serializers.ValidationError(
                    "A similar expense already exists for this date."
                )

        return attrs

    def create(self, validated_data):
        """
        Create a new expense

        This method is called when POST request is made.

        Args:
            validated_data: Dictionary of validated field values

        Returns:
            Expense instance

        Compare to C#:
        public async Task<Expense> CreateExpenseAsync(ExpenseDto dto) {
            var expense = _mapper.Map<Expense>(dto);
            expense.UserId = _currentUser.Id;
            await _context.Expenses.AddAsync(expense);
            await _context.SaveChangesAsync();
            return expense;
        }

        Why override this?
        - Set user automatically from request
        - Custom creation logic
        - Trigger side effects (send email, log, etc.)
        """
        # Get current user from request context (if not already set by perform_create)
        if "user" not in validated_data:
            request = self.context.get("request")
            if request and hasattr(request, "user") and request.user.is_authenticated:
                validated_data["user"] = request.user

        # Create and return the expense
        expense = Expense.objects.create(**validated_data)

        # Could add: Send notification, log activity, etc.

        return expense

    def update(self, instance, validated_data):
        """
        Update an existing expense

        Args:
            instance: The existing Expense object
            validated_data: Dictionary of validated new values

        Returns:
            Updated Expense instance

        Why override this?
        - Custom update logic
        - Prevent updating certain fields
        - Track changes
        """
        # Update fields
        instance.category = validated_data.get("category", instance.category)
        instance.amount = validated_data.get("amount", instance.amount)
        instance.description = validated_data.get("description", instance.description)
        instance.date = validated_data.get("date", instance.date)

        # Save to database
        instance.save()

        return instance


class ExpenseListSerializer(serializers.ModelSerializer):
    """
    Simplified serializer for listing expenses

    Used in list views where we don't need all details.

    Why this exists:
    - Faster API responses (less data)
    - Better user experience
    - Reduced bandwidth usage
    """

    category_name = serializers.CharField(source="category.name", read_only=True)
    username = serializers.CharField(source="user.username", read_only=True)

    class Meta:
        model = Expense
        fields = [
            "id",
            "category_name",
            "amount",
            "description",
            "date",
            "username",
        ]
        read_only_fields = fields  # All fields read-only for list view
