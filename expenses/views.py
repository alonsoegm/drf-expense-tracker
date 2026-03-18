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
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import OpenApiExample, OpenApiParameter, extend_schema
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
    """

    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    @extend_schema(
        summary="List all categories",
        description="Returns a paginated list of all expense categories.",
        responses={200: CategoryListSerializer(many=True)},
        tags=["Categories"],
    )
    def list(self, request, *args, **kwargs):
        """Get all categories"""
        return super().list(request, *args, **kwargs)

    @extend_schema(
        summary="Create a new category",
        description="Create a new expense category. Category names must be unique and at least 3 characters long.",
        request=CategorySerializer,
        responses={
            201: CategorySerializer,
            400: OpenApiTypes.OBJECT,
        },
        examples=[
            OpenApiExample(
                "Create Food Category",
                value={"name": "Food", "description": "Food and groceries"},
                request_only=True,
            ),
            OpenApiExample(
                "Create Transport Category",
                value={"name": "Transport", "description": "Public transport and gas"},
                request_only=True,
            ),
        ],
        tags=["Categories"],
    )
    def create(self, request, *args, **kwargs):
        """Create a new category"""
        return super().create(request, *args, **kwargs)

    @extend_schema(
        summary="Get category details",
        description="Retrieve detailed information about a specific category including expense count.",
        responses={
            200: CategorySerializer,
            404: OpenApiTypes.OBJECT,
        },
        tags=["Categories"],
    )
    def retrieve(self, request, *args, **kwargs):
        """Get a single category by ID"""
        return super().retrieve(request, *args, **kwargs)

    @extend_schema(
        summary="Update a category",
        description="Update all fields of an existing category. Requires all fields to be provided.",
        request=CategorySerializer,
        responses={
            200: CategorySerializer,
            400: OpenApiTypes.OBJECT,
            404: OpenApiTypes.OBJECT,
        },
        tags=["Categories"],
    )
    def update(self, request, *args, **kwargs):
        """Update a category (full update)"""
        return super().update(request, *args, **kwargs)

    @extend_schema(
        summary="Partially update a category",
        description="Update specific fields of a category. Only provided fields will be updated.",
        request=CategorySerializer,
        responses={
            200: CategorySerializer,
            400: OpenApiTypes.OBJECT,
            404: OpenApiTypes.OBJECT,
        },
        tags=["Categories"],
    )
    def partial_update(self, request, *args, **kwargs):
        """Partially update a category"""
        return super().partial_update(request, *args, **kwargs)

    @extend_schema(
        summary="Delete a category",
        description="Delete a category. Cannot delete if category has associated expenses.",
        responses={
            204: None,
            400: OpenApiTypes.OBJECT,
            404: OpenApiTypes.OBJECT,
        },
        tags=["Categories"],
    )
    def destroy(self, request, *args, **kwargs):
        """Delete a category"""
        return super().destroy(request, *args, **kwargs)


class ExpenseViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Expense CRUD operations
    """

    queryset = Expense.objects.all()
    serializer_class = ExpenseSerializer

    def get_serializer_class(self):
        """Use simplified serializer for list view"""
        if self.action == "list":
            return ExpenseListSerializer
        return ExpenseSerializer

    def get_queryset(self):
        """
        Optimize queryset with related data
        """
        queryset = Expense.objects.select_related("category", "user")
        queryset = queryset.order_by("-date", "-created_at")
        return queryset

    @extend_schema(
        summary="List all expenses",
        description="Returns a paginated list of all expenses ordered by date (most recent first).",
        responses={200: ExpenseListSerializer(many=True)},
        parameters=[
            OpenApiParameter(
                name="page",
                type=OpenApiTypes.INT,
                location=OpenApiParameter.QUERY,
                description="Page number for pagination",
            ),
        ],
        tags=["Expenses"],
    )
    def list(self, request, *args, **kwargs):
        """Get all expenses"""
        return super().list(request, *args, **kwargs)

    @extend_schema(
        summary="Create a new expense",
        description=" Create a new expense record.",
        request=ExpenseSerializer,
        responses={
            201: ExpenseSerializer,
            400: OpenApiTypes.OBJECT,
        },
        examples=[
            OpenApiExample(
                "Grocery Shopping",
                value={
                    "categoryId": 1,
                    "amount": 85.50,
                    "description": "Weekly grocery shopping at Whole Foods",
                    "date": "2024-03-19",
                },
                request_only=True,
            ),
            OpenApiExample(
                "Gas Station",
                value={
                    "categoryId": 2,
                    "amount": 45.00,
                    "description": "Gas fill-up",
                    "date": "2024-03-18",
                },
                request_only=True,
            ),
            OpenApiExample(
                "Restaurant",
                value={
                    "categoryId": 1,
                    "amount": 32.75,
                    "description": "Dinner at Italian restaurant",
                    "date": "2024-03-17",
                },
                request_only=True,
            ),
        ],
        tags=["Expenses"],
    )
    def create(self, request, *args, **kwargs):
        """Create a new expense"""
        return super().create(request, *args, **kwargs)

    @extend_schema(
        summary="Get expense details",
        description="Retrieve detailed information about a specific expense.",
        responses={
            200: ExpenseSerializer,
            404: OpenApiTypes.OBJECT,
        },
        tags=["Expenses"],
    )
    def retrieve(self, request, *args, **kwargs):
        """Get a single expense by ID"""
        return super().retrieve(request, *args, **kwargs)

    @extend_schema(
        summary="Update an expense",
        description="Update all fields of an existing expense.",
        request=ExpenseSerializer,
        responses={
            200: ExpenseSerializer,
            400: OpenApiTypes.OBJECT,
            404: OpenApiTypes.OBJECT,
        },
        examples=[
            OpenApiExample(
                "Update Expense",
                value={
                    "categoryId": 1,
                    "amount": 95.00,
                    "description": "Updated: Weekly grocery shopping",
                    "date": "2024-03-19",
                },
                request_only=True,
            ),
        ],
        tags=["Expenses"],
    )
    def update(self, request, *args, **kwargs):
        """Update an expense (full update)"""
        return super().update(request, *args, **kwargs)

    @extend_schema(
        summary="Partially update an expense",
        description="Update specific fields of an expense without providing all fields.",
        request=ExpenseSerializer,
        responses={
            200: ExpenseSerializer,
            400: OpenApiTypes.OBJECT,
            404: OpenApiTypes.OBJECT,
        },
        examples=[
            OpenApiExample(
                "Update Amount Only",
                value={"amount": 99.99},
                request_only=True,
            ),
            OpenApiExample(
                "Update Description and Category",
                value={
                    "categoryId": 3,
                    "description": "Corrected: Entertainment expense",
                },
                request_only=True,
            ),
            OpenApiExample(
                "Update Date",
                value={"date": "2024-03-18"},
                request_only=True,
            ),
        ],
        tags=["Expenses"],
    )
    def partial_update(self, request, *args, **kwargs):
        """Partially update an expense"""
        return super().partial_update(request, *args, **kwargs)

    @extend_schema(
        summary="Delete an expense",
        description="Permanently delete an expense record.",
        responses={
            204: None,
            404: OpenApiTypes.OBJECT,
        },
        tags=["Expenses"],
    )
    def destroy(self, request, *args, **kwargs):
        """Delete an expense"""
        return super().destroy(request, *args, **kwargs)

    @extend_schema(
        summary="Get recent expenses",
        description="Returns expenses from the last 7 days.",
        responses={200: ExpenseListSerializer(many=True)},
        tags=["Expenses"],
    )
    @action(detail=False, methods=["get"])
    def recent(self, request: Request) -> Response:
        """
        Custom endpoint: GET /api/expenses/recent/

        Returns expenses from last 7 days
        """
        # Standard Library
        from datetime import date, timedelta

        seven_days_ago = date.today() - timedelta(days=7)
        recent_expenses = self.get_queryset().filter(date__gte=seven_days_ago)

        serializer = self.get_serializer(recent_expenses, many=True)
        return Response(serializer.data)

    @extend_schema(
        summary="Get expense statistics",
        description="Returns aggregated statistics about all expenses.",
        responses={
            200: {
                "type": "object",
                "properties": {
                    "totalAmount": {
                        "type": "number",
                        "description": "Sum of all expense amounts",
                        "example": 1234.56,
                    },
                    "count": {
                        "type": "integer",
                        "description": "Total number of expenses",
                        "example": 42,
                    },
                    "averageAmount": {
                        "type": "number",
                        "description": "Average expense amount",
                        "example": 29.39,
                    },
                },
            }
        },
        examples=[
            OpenApiExample(
                "Statistics Response",
                value={"totalAmount": 1234.56, "count": 42, "averageAmount": 29.39},
                response_only=True,
            ),
        ],
        tags=["Expenses"],
    )
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

    def perform_create(self, serializer):
        """
        Set user automatically when creating expense
        """
        # Third-party
        from django.contrib.auth.models import User

        user = User.objects.first()

        if not user:
            user = User.objects.create_user(
                username="admin", email="admin@example.com", password="admin123"
            )

        serializer.save(user=user)

    def perform_update(self, serializer):
        """Update expense without changing user"""
        serializer.save()


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
