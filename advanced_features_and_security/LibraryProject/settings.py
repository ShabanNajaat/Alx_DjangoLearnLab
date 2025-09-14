# Add to your settings.py
AUTH_USER_MODEL = 'bookshelf.CustomUser'

# Also add media settings for profile photos
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
