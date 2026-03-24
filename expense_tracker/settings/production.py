"""
Production settings for expense_tracker project.
These settings are used in production environment (Azure, AWS, etc.)
Similar to appsettings.Production.json in ASP.NET Core
"""

# Third-party
from decouple import Csv, config  # For parsing comma-separated environment variables

from .base import *  # noqa: F403

# ==============================================================================
# SECURITY SETTINGS
# ==============================================================================

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

# SECURITY WARNING: keep the secret key used in production secret!
# Must be set via environment variable
SECRET_KEY = config("SECRET_KEY")

# Allowed hosts must be configured via environment variable
# Example: yourapp.azurewebsites.net,yourdomain.com
ALLOWED_HOSTS = config("ALLOWED_HOSTS", cast=Csv())

# ==============================================================================
# HTTPS/SSL SETTINGS
# ==============================================================================

# Redirect all HTTP requests to HTTPS
SECURE_SSL_REDIRECT = True

# Use secure cookies
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

# HSTS (HTTP Strict Transport Security)
# Force browsers to use HTTPS for 1 year
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True

# X-Content-Type-Options: nosniff
SECURE_CONTENT_TYPE_NOSNIFF = True

# X-Frame-Options: DENY
X_FRAME_OPTIONS = "DENY"

# ==============================================================================
# CORS SETTINGS
# ==============================================================================

# Strict CORS in production - must be configured via environment variable
CORS_ALLOWED_ORIGINS = config("CORS_ALLOWED_ORIGINS", cast=Csv())
CORS_ALLOW_ALL_ORIGINS = False

# ==============================================================================
# DATABASE
# ==============================================================================

# Database must be configured via DATABASE_URL environment variable
# Example for Azure SQL:
# postgresql://user:pass@server.postgres.database.azure.com:5432/dbname?sslmode=require

# Database is already configured in base.py using dj_database_url
# In production, make sure DATABASE_URL is set!

# ==============================================================================
# STATIC FILES
# ==============================================================================

# WhiteNoise will serve static files (already configured in base.py)
# Make sure to run: python manage.py collectstatic --noinput

# ==============================================================================
# LOGGING
# ==============================================================================

# Production logging - less verbose, focus on errors
LOGGING["loggers"]["django"]["level"] = "WARNING"  # type: ignore[index]  # noqa: F405
LOGGING["loggers"]["expenses"]["level"] = "INFO"  # type: ignore[index]  # noqa: F405

# ==============================================================================
# EMAIL BACKEND
# ==============================================================================

# Use real email backend in production
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = config("EMAIL_HOST", default="smtp.gmail.com")
EMAIL_PORT = config("EMAIL_PORT", default=587, cast=int)
EMAIL_USE_TLS = config("EMAIL_USE_TLS", default=True, cast=bool)
EMAIL_HOST_USER = config("EMAIL_HOST_USER", default="")
EMAIL_HOST_PASSWORD = config("EMAIL_HOST_PASSWORD", default="")

# ==============================================================================
# ADMINS
# ==============================================================================

# Configure admins to receive error emails
ADMINS = [
    ("Admin", config("ADMIN_EMAIL", default="admin@example.com")),
]

MANAGERS = ADMINS

# ==============================================================================
# CACHES (Optional - configure if needed)
# ==============================================================================

# Example Redis cache configuration
# CACHES = {
#     'default': {
#         'BACKEND': 'django.core.cache.backends.redis.RedisCache',
#         'LOCATION': config('REDIS_URL', default='redis://127.0.0.1:6379/1'),
#     }
# }
