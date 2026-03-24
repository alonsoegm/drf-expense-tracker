"""
Development settings for expense_tracker project.
These settings are used for local development.
Similar to appsettings.Development.json in ASP.NET Core
"""

from .base import *  # noqa: F403

# ==============================================================================
# DEBUG SETTINGS
# ==============================================================================

DEBUG = True

# ==============================================================================
# ALLOWED HOSTS
# ==============================================================================

ALLOWED_HOSTS = ["localhost", "127.0.0.1", "[::1]"]

# ==============================================================================
# DATABASE
# ==============================================================================
# In development, we use SQLite by default
# You can override with DATABASE_URL in .env if you want to test with PostgreSQL

# Database is already configured in base.py using dj_database_url
# It will use DATABASE_URL from .env or default to SQLite

# ==============================================================================
# CORS SETTINGS
# ==============================================================================
# More permissive CORS for development

CORS_ALLOW_ALL_ORIGINS = False  # Still use specific origins from .env
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",  # React default
    "http://localhost:5173",  # Vite default
    "http://localhost:8080",  # Vue default
    "http://localhost:4200",  # Angular default
]

# ==============================================================================
# LOGGING
# ==============================================================================
# More verbose logging in development

LOGGING["loggers"]["django"]["level"] = "DEBUG"  # type: ignore[index]  # noqa: F405
LOGGING["loggers"]["expenses"]["level"] = "DEBUG"  # type: ignore[index]  # noqa: F405

# ==============================================================================
# EMAIL BACKEND
# ==============================================================================
# Print emails to console in development (not send them)

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

# ==============================================================================
# DEVELOPMENT TOOLS
# ==============================================================================

# Show detailed error pages
DEBUG_PROPAGATE_EXCEPTIONS = False

# Django Debug Toolbar (if you want to add it later)
# INSTALLED_APPS += ['debug_toolbar']
# MIDDLEWARE += ['debug_toolbar.middleware.DebugToolbarMiddleware']
# INTERNAL_IPS = ['127.0.0.1']
