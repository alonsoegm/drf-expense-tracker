"""
FilterSets for the Expense Tracker API

What are FilterSets?
- Classes that define which fields can be filtered
- Define how filtering works (exact, range, contains, etc.)
- Automatically generate query parameters

Compare to C#:
- Like defining [FromQuery] parameters in controller
- But more declarative and automatic
- DRF handles all the query string parsing

Filter Types:
- CharFilter: Text fields (exact, contains, icontains)
- NumberFilter: Numeric fields (exact, lt, lte, gt, gte)
- DateFilter: Date fields (exact, lt, lte, gt, gte)
- BooleanFilter: Boolean fields (true/false)
- ChoiceFilter: Enumerated choices
"""

# Third-party
import django_filters

from .models import Category, Expense


class CategoryFilter(django_filters.FilterSet):
    """
    FilterSet for Category model

    Available filters:
    - name: Filter by exact name
    - name__icontains: Search in name (case-insensitive)

    Examples:
    GET /api/categories/?name=Food
    GET /api/categories/?name__icontains=foo

    Compare to C#:
    [HttpGet]
    public IActionResult GetCategories([FromQuery] string? name) {
        var query = _context.Categories.AsQueryable();
        if (!string.IsNullOrEmpty(name))
            query = query.Where(c => c.Name.Contains(name,
                StringComparison.OrdinalIgnoreCase));
        return Ok(query.ToList());
    }
    """

    # Custom filter: Search in name (case-insensitive)
    name = django_filters.CharFilter(
        field_name="name",
        lookup_expr="icontains",
        # lookup_expr options:
        # - 'exact': Exact match (default)
        # - 'iexact': Case-insensitive exact match
        # - 'contains': Case-sensitive contains
        # - 'icontains': Case-insensitive contains
        # - 'startswith': Starts with
        # - 'istartswith': Case-insensitive starts with
        # - 'endswith': Ends with
        # - 'iendswith': Case-insensitive ends with
    )

    class Meta:
        model = Category
        fields = {
            "name": ["exact", "icontains"],  # /api/categories/?name=Food
            # This generates two filters:
            # - name (exact match)
            # - name__icontains (contains, case-insensitive)
        }

        # Alternative syntax (more explicit):
        # fields = ['name']  # Only exact match


class ExpenseFilter(django_filters.FilterSet):
    """
    FilterSet for Expense model

    Available filters:
    - category: Filter by category ID
    - amount_min: Minimum amount (amount >= value)
    - amount_max: Maximum amount (amount <= value)
    - date_from: Start date (date >= value)
    - date_to: End date (date <= value)
    - description: Search in description (case-insensitive)
    - user: Filter by user ID

    Examples:
    GET /api/expenses/?category=1
    GET /api/expenses/?amount_min=50&amount_max=100
    GET /api/expenses/?date_from=2024-01-01&date_to=2024-12-31
    GET /api/expenses/?description=grocery
    GET /api/expenses/?category=1&date_from=2024-03-01&ordering=-amount

    Compare to C#:
    public class ExpenseQueryParams {
        public int? CategoryId { get; set; }
        public decimal? AmountMin { get; set; }
        public decimal? AmountMax { get; set; }
        public DateTime? DateFrom { get; set; }
        public DateTime? DateTo { get; set; }
        public string? Description { get; set; }
    }

    [HttpGet]
    public IActionResult GetExpenses([FromQuery] ExpenseQueryParams params) {
        var query = _context.Expenses.AsQueryable();

        if (params.CategoryId.HasValue)
            query = query.Where(e => e.CategoryId == params.CategoryId);

        if (params.AmountMin.HasValue)
            query = query.Where(e => e.Amount >= params.AmountMin);

        if (params.AmountMax.HasValue)
            query = query.Where(e => e.Amount <= params.AmountMax);

        if (params.DateFrom.HasValue)
            query = query.Where(e => e.Date >= params.DateFrom);

        if (params.DateTo.HasValue)
            query = query.Where(e => e.Date <= params.DateTo);

        if (!string.IsNullOrEmpty(params.Description))
            query = query.Where(e => e.Description.Contains(params.Description));

        return Ok(query.ToList());
    }
    """

    # Category filter (exact match)
    category = django_filters.NumberFilter(
        field_name="category",
        # Filters by category ID
        # GET /api/expenses/?category=1
    )

    # Amount range filters
    amount_min = django_filters.NumberFilter(
        field_name="amount",
        lookup_expr="gte",  # Greater than or equal (>=)
        # GET /api/expenses/?amount_min=50
    )

    amount_max = django_filters.NumberFilter(
        field_name="amount",
        lookup_expr="lte",  # Less than or equal (<=)
        # GET /api/expenses/?amount_max=100
    )

    # Date range filters
    date_from = django_filters.DateFilter(
        field_name="date",
        lookup_expr="gte",  # Greater than or equal
        # GET /api/expenses/?date_from=2024-01-01
    )

    date_to = django_filters.DateFilter(
        field_name="date",
        lookup_expr="lte",  # Less than or equal
        # GET /api/expenses/?date_to=2024-12-31
    )

    # Description search (case-insensitive contains)
    description = django_filters.CharFilter(
        field_name="description",
        lookup_expr="icontains",
        # GET /api/expenses/?description=grocery
        # Finds: "Grocery shopping", "GROCERY", "grocery store", etc.
    )

    # User filter
    user = django_filters.NumberFilter(
        field_name="user",
        # GET /api/expenses/?user=1
    )

    class Meta:
        model = Expense
        fields = {
            # Simple filters (exact match)
            "category": ["exact"],
            "user": ["exact"],
            # Amount with range
            "amount": ["exact", "gte", "lte", "gt", "lt"],
            # Generates:
            # - amount (exact)
            # - amount__gte (greater than or equal)
            # - amount__lte (less than or equal)
            # - amount__gt (greater than)
            # - amount__lt (less than)
            # Date with range
            "date": ["exact", "gte", "lte", "gt", "lt", "year", "month"],
            # Generates:
            # - date (exact)
            # - date__gte (from date)
            # - date__lte (to date)
            # - date__year (filter by year: ?date__year=2024)
            # - date__month (filter by month: ?date__month=3)
            # Description search
            "description": ["icontains"],
            # Generates:
            # - description__icontains (case-insensitive search)
        }


# ============================================================================
# FILTER COMPARISON SUMMARY
# ============================================================================
#
# django-filter FilterSet:
# - Declarative configuration
# - Automatic query parameter parsing
# - Built-in validation
# - Works with DRF seamlessly
# - Generates OpenAPI schema automatically
#
# C# Manual Filtering:
# - Imperative code in controller
# - Manual parameter binding
# - Manual validation
# - More boilerplate code
# - Need to document API separately
#
# Both achieve the same result, but FilterSets require less code!
#
# ============================================================================
# LOOKUP EXPRESSIONS REFERENCE
# ============================================================================
#
# Text fields (CharField, TextField):
# - exact: Exact match
# - iexact: Case-insensitive exact match
# - contains: Contains (case-sensitive)
# - icontains: Contains (case-insensitive) ← Most common for search
# - startswith: Starts with
# - istartswith: Case-insensitive starts with
# - endswith: Ends with
# - iendswith: Case-insensitive ends with
#
# Numeric fields (IntegerField, DecimalField):
# - exact: Exact match
# - gt: Greater than (>)
# - gte: Greater than or equal (>=) ← Common for "from" filters
# - lt: Less than (<)
# - lte: Less than or equal (<=) ← Common for "to" filters
# - range: Between two values
#
# Date/DateTime fields:
# - exact: Exact date
# - gt, gte, lt, lte: Date comparisons
# - year: Filter by year
# - month: Filter by month
# - day: Filter by day
# - week_day: Filter by day of week
# - range: Date range
#
# Boolean fields:
# - exact: true/false
#
# ForeignKey fields:
# - All lookups work on the FK ID
# - Use __ to filter on related fields:
#   category__name__icontains (filter expenses by category name)
