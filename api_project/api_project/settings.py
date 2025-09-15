# Add to INSTALLED_APPS
INSTALLED_APPS = [
    # ... other apps ...
    'rest_framework',
    'rest_framework.authtoken',  # Add this for token authentication
    'api',
]

# Django REST Framework settings
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',  # Token authentication
        'rest_framework.authentication.SessionAuthentication',  # Session authentication for browsable API
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',  # Default: require authentication
    ],
}
