"""
URL configuration for expenses app

What is a Router?
- Automatically generates URL patterns for ViewSets
- Maps HTTP methods to ViewSet actions
- Creates RESTful URLs following conventions

Compare to C#:
- Router = Automatic route configuration
- Like attribute routing: [Route("api/[controller]")]
- But more automatic!

URL Patterns Generated:
├── /api/categories/
│   ├── GET     → list all categories
│   ├── POST    → create new category
│   └── /api/categories/{id}/
│       ├── GET     → retrieve category
│       ├── PUT     → update category
│       ├── PATCH   → partial update
│       └── DELETE  → delete category
│
└── /api/expenses/
    ├── GET     → list all expenses
    ├── POST    → create new expense
    └── /api/expenses/{id}/
        ├── GET     → retrieve expense
        ├── PUT     → update expense
        ├── PATCH   → partial update
        └── DELETE  → delete expense
"""

# Third-party
from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import CategoryViewSet, ExpenseViewSet

# ============================================================================
# ROUTER CONFIGURATION
# ============================================================================

# Create router instance
router = DefaultRouter()
# DefaultRouter automatically creates:
# - List endpoint: /api/resource/
# - Detail endpoint: /api/resource/{pk}/
# - API root view: /api/
#
# Compare to SimpleRouter which doesn't include API root

# ============================================================================
# REGISTER VIEWSETS
# ============================================================================

# Register CategoryViewSet
router.register(r"categories", CategoryViewSet, basename="category")
# Arguments:
# - r'categories': URL prefix
# - CategoryViewSet: The ViewSet class
# - basename: Name prefix for URL patterns (optional if queryset is defined)
#
# This creates URLs:
# - /api/categories/                    → list, create
# - /api/categories/{id}/               → retrieve, update, delete
# - /api/categories/summary/            → custom action (from @action)
#
# Compare to C#:
# [Route("api/categories")]
# public class CategoriesController { }

# Register ExpenseViewSet
router.register(r"expenses", ExpenseViewSet, basename="expense")
# Creates URLs:
# - /api/expenses/                      → list, create
# - /api/expenses/{id}/                 → retrieve, update, delete
# - /api/expenses/recent/               → custom action
# - /api/expenses/statistics/           → custom action

# ============================================================================
# URL PATTERNS
# ============================================================================

# App name for namespacing
app_name = "expenses"
# Allows: reverse('expenses:category-list')
# Like: Url.Action("List", "Categories") in ASP.NET

# Include router URLs
urlpatterns = [
    path("", include(router.urls)),
]

# ============================================================================
# GENERATED URL PATTERNS EXPLANATION
# ============================================================================
#
# For CategoryViewSet:
# Name: category-list
# Pattern: ^categories/$
# Methods: GET (list), POST (create)
#
# Name: category-detail
# Pattern: ^categories/(?P<pk>[^/.]+)/$
# Methods: GET (retrieve), PUT (update), PATCH (partial_update), DELETE (destroy)
#
# Name: category-summary
# Pattern: ^categories/summary/$
# Methods: GET (custom action)
#
# For ExpenseViewSet:
# Name: expense-list
# Pattern: ^expenses/$
# Methods: GET (list), POST (create)
#
# Name: expense-detail
# Pattern: ^expenses/(?P<pk>[^/.]+)/$
# Methods: GET (retrieve), PUT (update), PATCH (partial_update), DELETE (destroy)
#
# Name: expense-recent
# Pattern: ^expenses/recent/$
# Methods: GET (custom action)
#
# Name: expense-statistics
# Pattern: ^expenses/statistics/$
# Methods: GET (custom action)
#
# ============================================================================
