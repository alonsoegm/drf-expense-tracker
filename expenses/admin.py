"""
Django Admin configuration

Why this exists:
- Provides a web UI to manage data (CRUD operations)
- Useful for testing and manual data entry
- Like a built-in database management tool

Compare to C#:
- No direct equivalent
- Similar to scaffolded CRUD pages in ASP.NET
"""

from django.contrib import admin
from .models import Category, Expense


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """
    Admin configuration for Category model
    
    What you can do here:
    - Customize how categories appear in admin panel
    - Add search, filters, custom actions
    """
    list_display = ['name', 'description', 'created_at']
    # Columns to show in the list view
    
    search_fields = ['name', 'description']
    # Fields to search by
    
    list_filter = ['created_at']
    # Add filter sidebar for these fields
    
    readonly_fields = ['created_at', 'updated_at']
    # Fields that can't be edited


@admin.register(Expense)
class ExpenseAdmin(admin.ModelAdmin):
    """
    Admin configuration for Expense model
    """
    list_display = ['description', 'category', 'amount', 'date', 'user', 'created_at']
    # Show these columns in list
    
    search_fields = ['description']
    # Search by description
    
    list_filter = ['category', 'date', 'user']
    # Filter by category, date, user
    
    readonly_fields = ['created_at', 'updated_at']
    
    date_hierarchy = 'date'
    # Add date-based navigation at top
    
    # Organize fields in the edit form
    fieldsets = (
        ('Expense Details', {
            'fields': ('user', 'category', 'amount', 'description', 'date')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)  # Collapsible section
        }),
    )