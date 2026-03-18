"""
Main URL configuration for expense_tracker project

This is the root URL configuration that includes all app URLs.

Compare to C#:
- This is like Program.cs or Startup.cs where you configure routing
- app.MapControllers() vs including app URLs

URL Structure:
/admin/                 → Django admin panel
/api/                   → All API endpoints (from expenses app)
"""

# Third-party
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    # Django Admin
    path("admin/", admin.site.urls),
    # Admin panel at: http://localhost:8000/admin/
    # Like: /Admin in ASP.NET MVC
    # API endpoints
    path("api/", include("expenses.urls")),
    # Includes all URLs from expenses/urls.py
    # All API endpoints will be under /api/
    #
    # Like in C#:
    # app.MapControllerRoute(
    #     name: "api",
    #     pattern: "api/{controller}/{action}/{id?}"
    # );
]

# ============================================================================
# FINAL URL STRUCTURE
# ============================================================================
#
# Admin:
# http://localhost:8000/admin/
#
# API Root:
# http://localhost:8000/api/
#
# Categories:
# http://localhost:8000/api/categories/
# http://localhost:8000/api/categories/1/
# http://localhost:8000/api/categories/summary/
#
# Expenses:
# http://localhost:8000/api/expenses/
# http://localhost:8000/api/expenses/1/
# http://localhost:8000/api/expenses/recent/
# http://localhost:8000/api/expenses/statistics/
