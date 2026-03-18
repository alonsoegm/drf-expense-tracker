"""
ViewSets for the Expense Tracker API

What are ViewSets?
- Class-based views that provide CRUD operations
- Combine logic for list, create, retrieve, update, destroy
- Work with DRF Router to auto-generate URLs

Compare to C#:
- ViewSet = API Controller
- ModelViewSet = Controller with all CRUD actions pre-built
- queryset = DbSet<T> in Entity Framework
- serializer_class = DTO mapping configuration

Why ViewSets?
- Less boilerplate code
- Automatic URL routing
- Built-in pagination, filtering, permissions
- RESTful by default
"""

# Third-party
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.request import Request
from rest_framework.response import Response

from .models import Category, Expense
from .serializers import (
    CategoryListSerializer,
    CategorySerializer,
    ExpenseListSerializer,
    ExpenseSerializer,
)


class CategoryViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Category CRUD operations

    This ViewSet automatically provides:
    - list()    → GET    /api/categories/
    - create()  → POST   /api/categories/
    - retrieve() → GET    /api/categories/{id}/
    - update()  → PUT    /api/categories/{id}/
    - partial_update() → PATCH /api/categories/{id}/
    - destroy() → DELETE /api/categories/{id}/

    Compare to C#:
    [ApiController]
    [Route("api/categories")]
    public class CategoriesController : ControllerBase {
        // You'd need to write each action manually
        // DRF does this automatically!
    }

    Attributes:
        queryset: All Category objects (like DbSet<Category>)
        serializer_class: Default serializer to use
    """

    queryset = Category.objects.all()
    # queryset: What data this ViewSet works with
    # Like: private readonly DbSet<Category> _categories;
    # Orders by name (defined in Category.Meta.ordering)

    serializer_class = CategorySerializer
    # Default serializer for all actions
    # Like: configuring AutoMapper profile

    def get_serializer_class(self):
        """
        Return different serializers based on action

        Why?
        - list() needs less data (CategoryListSerializer)
        - retrieve() needs full data (CategorySerializer)
        - Improves performance

        Compare to C#:
        public IActionResult GetAll() {
            return Ok(_mapper.Map<List<CategoryListDto>>(categories));
        }

        public IActionResult Get(int id) {
            return Ok(_mapper.Map<CategoryDetailDto>(category));
        }
        """
        if self.action == "list":
            # Use simplified serializer for list view
            return CategoryListSerializer
        return CategorySerializer

    def get_queryset(self):
        """
        Customize the queryset

        Why override this?
        - Add filtering
        - Add ordering
        - Optimize queries (select_related, prefetch_related)
        - Apply permissions

        Compare to C#:
        private IQueryable<Category> GetCategories() {
            return _context.Categories
                .Include(c => c.Expenses)
                .OrderBy(c => c.Name);
        }
        """
        queryset = Category.objects.all()

        # Optimize: Load expense count in single query
        # Similar to .Include() in Entity Framework
        # We'll add this optimization later

        return queryset

    def perform_create(self, serializer):
        """
        Customize object creation

        Called after validation but before saving

        Why override this?
        - Set additional fields (created_by, etc.)
        - Trigger side effects (send email, log, etc.)
        - Custom business logic

        Compare to C#:
        [HttpPost]
        public async Task<IActionResult> Create([FromBody] CategoryDto dto) {
            var category = _mapper.Map<Category>(dto);
            category.CreatedBy = User.Identity.Name;  // Like this!
            await _context.SaveChangesAsync();
            return CreatedAtAction(...);
        }

        Args:
            serializer: Validated serializer instance
        """
        # Save the category
        serializer.save()

        # Could add: logging, notifications, etc.
        # logger.info(f"Category created: {serializer.instance.name}")

    def perform_update(self, serializer):
        """
        Customize object update

        Similar to perform_create but for updates
        """
        serializer.save()
        # Could add: audit logging, cache invalidation, etc.

    def perform_destroy(self, instance):
        """
        Customize object deletion

        Why override this?
        - Soft delete instead of hard delete
        - Check if object can be deleted
        - Clean up related objects
        - Log deletion

        Compare to C#:
        [HttpDelete("{id}")]
        public async Task<IActionResult> Delete(int id) {
            var category = await _context.Categories
                .Include(c => c.Expenses)
                .FirstOrDefaultAsync(c => c.Id == id);

            if (category.Expenses.Any()) {
                return BadRequest("Cannot delete category with expenses");
            }

            _context.Remove(category);
            await _context.SaveChangesAsync();
            return NoContent();
        }

        Args:
            instance: The Category object to delete
        """
        # Check if category has expenses
        if instance.expenses.exists():
            # Can't delete category with expenses (PROTECT constraint)
            # This is already handled by Django's on_delete=models.PROTECT
            # But we could add custom error message here
            pass

        instance.delete()

    @action(detail=False, methods=["get"])
    def summary(self, request: Request) -> Response:
        """
        Custom endpoint: GET /api/categories/summary/

        @action decorator creates custom endpoints

        Args:
            detail=False: /api/categories/summary/ (list-level)
            detail=True:  /api/categories/{id}/summary/ (detail-level)
            methods: HTTP methods allowed

        Compare to C#:
        [HttpGet("summary")]
        public IActionResult GetSummary() {
            // Custom endpoint
        }

        Returns:
            Response with summary data
        """
        categories = self.get_queryset()

        summary_data = {
            "total_categories": categories.count(),
            "categories": [
                {"name": cat.name, "expense_count": cat.get_expense_count()}
                for cat in categories
            ],
        }

        return Response(summary_data)


class ExpenseViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Expense CRUD operations

    Provides all CRUD operations for expenses with automatic URL routing.

    Automatically provides:
    - GET    /api/expenses/         → list()
    - POST   /api/expenses/         → create()
    - GET    /api/expenses/{id}/    → retrieve()
    - PUT    /api/expenses/{id}/    → update()
    - PATCH  /api/expenses/{id}/    → partial_update()
    - DELETE /api/expenses/{id}/    → destroy()
    """

    queryset = Expense.objects.all()
    serializer_class = ExpenseSerializer

    def get_serializer_class(self):
        """
        Use simplified serializer for list view
        """
        if self.action == "list":
            return ExpenseListSerializer
        return ExpenseSerializer

    def get_queryset(self):
        """
        Optimize queryset with related data

        Why?
        - Reduce database queries (N+1 problem)
        - Load related Category and User in one query

        Compare to C#:
        return _context.Expenses
            .Include(e => e.Category)
            .Include(e => e.User)
            .OrderByDescending(e => e.Date);
        """
        queryset = Expense.objects.select_related("category", "user")
        # select_related: SQL JOIN for foreign keys
        # Like .Include() in Entity Framework
        # Loads Category and User in same query

        # Order by most recent first
        queryset = queryset.order_by("-date", "-created_at")

        return queryset

    def perform_create(self, serializer):
        """
        Set user automatically when creating expense

        The serializer expects user to be set, but we don't
        want the API consumer to provide it - we get it from
        the authenticated user.

        For now (no auth yet), we'll use the first user.
        Later we'll use: request.user

        Compare to C#:
        [HttpPost]
        public async Task<IActionResult> Create([FromBody] ExpenseDto dto) {
            var expense = _mapper.Map<Expense>(dto);
            expense.UserId = User.FindFirst(ClaimTypes.NameIdentifier).Value;
            // ...
        }
        """
        # TODO: Once we add authentication, change this to:
        # serializer.save(user=self.request.user)

        # For now, use first user
        # Third-party
        from django.contrib.auth.models import User

        user = User.objects.first()

        if not user:
            # No users exist, create one
            user = User.objects.create_user(
                username="admin", email="admin@example.com", password="admin123"
            )

        serializer.save(user=user)

    def perform_update(self, serializer):
        """
        Update expense

        Don't allow changing the user
        """
        # Save without changing user
        serializer.save()

    @action(detail=False, methods=["get"])
    def recent(self, request: Request) -> Response:
        """
        Custom endpoint: GET /api/expenses/recent/

        Returns expenses from last 7 days

        Compare to C#:
        [HttpGet("recent")]
        public IActionResult GetRecent() {
            var recent = _context.Expenses
                .Where(e => e.Date >= DateTime.Now.AddDays(-7))
                .ToList();
            return Ok(_mapper.Map<List<ExpenseDto>>(recent));
        }
        """
        # Standard Library
        from datetime import date, timedelta

        seven_days_ago = date.today() - timedelta(days=7)
        recent_expenses = self.get_queryset().filter(date__gte=seven_days_ago)

        serializer = self.get_serializer(recent_expenses, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=["get"])
    def statistics(self, request: Request) -> Response:
        """
        Custom endpoint: GET /api/expenses/statistics/

        Returns expense statistics
        """
        # Third-party
        from django.db.models import Avg, Count, Sum

        queryset = self.get_queryset()

        stats = queryset.aggregate(
            total_amount=Sum("amount"), count=Count("id"), average_amount=Avg("amount")
        )

        return Response(stats)


# ============================================================================
# VIEWSET COMPARISON SUMMARY
# ============================================================================
#
# DRF ViewSet:
# - One class for all CRUD operations
# - Automatic URL routing
# - Built-in pagination, filtering
# - Custom actions with @action decorator
#
# C# API Controller:
# - Need to write each action (Get, Post, Put, Delete)
# - Manual route configuration
# - Manual pagination implementation
# - Custom endpoints = custom action methods
#
# Both achieve the same goal, but ViewSets require less code!
