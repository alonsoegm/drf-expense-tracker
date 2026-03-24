"""
Testing settings for expense_tracker project.
These settings are used when running tests with pytest.
Optimized for speed and isolation.
"""

from .base import *  # noqa: F403

# ==============================================================================
# DEBUG SETTINGS
# ==============================================================================

DEBUG = False

# ==============================================================================
# DATABASE
# ==============================================================================
# Use in-memory SQLite for faster tests
# Similar to InMemory database in Entity Framework for testing

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": ":memory:",  # In-memory database (very fast!)
    }
}

# ==============================================================================
# PASSWORD HASHERS
# ==============================================================================
# Use faster password hasher for tests (security doesn't matter in tests)

PASSWORD_HASHERS = [
    "django.contrib.auth.hashers.MD5PasswordHasher",
]

# ==============================================================================
# EMAIL BACKEND
# ==============================================================================
# Use in-memory email backend (don't actually send emails)

EMAIL_BACKEND = "django.core.mail.backends.locmem.EmailBackend"

# ==============================================================================
# LOGGING
# ==============================================================================
# Minimal logging during tests (only show errors)

LOGGING["loggers"]["django"]["level"] = "ERROR"  # type: ignore[index]  # noqa: F405
LOGGING["loggers"]["expenses"]["level"] = "ERROR"  # type: ignore[index]  # noqa: F405

# ==============================================================================
# CACHES
# ==============================================================================
# Use dummy cache (no caching in tests)

CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.dummy.DummyCache",
    }
}

# ==============================================================================
# MIDDLEWARE
# ==============================================================================
# Remove unnecessary middleware for faster tests
# Keep only essential ones

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
]

# ==============================================================================
# STATIC FILES
# ==============================================================================
# Simplified static files for testing

STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },
    "staticfiles": {
        "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage",
    },
}
