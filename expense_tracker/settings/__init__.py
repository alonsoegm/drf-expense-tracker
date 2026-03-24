"""
Settings package for expense_tracker project.

Automatically loads the correct settings module based on DJANGO_ENV:
- development: Local development settings
- production: Production settings
- testing: Test settings

Similar to environment-based configuration in ASP.NET Core.
"""

# Third-party
from decouple import config

# Determine which settings to use
# Priority: DJANGO_SETTINGS_MODULE > DJANGO_ENV > default to development
ENVIRONMENT = config("DJANGO_ENV", default="development")

if ENVIRONMENT == "production":
    from .production import *  # noqa: F401, F403
elif ENVIRONMENT == "testing":
    from .testing import *  # noqa: F401, F403
else:
    # Default to development
    from .development import *  # noqa: F401, F403

print(f"Loaded settings for: {ENVIRONMENT.upper()} environment")
