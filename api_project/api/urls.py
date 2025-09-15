from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken.views import obtain_auth_token
from .views import BookList, BookViewSet
from .auth_views import register_user

router = DefaultRouter()
router.register(r'books_all', BookViewSet, basename='book_all')

urlpatterns = [
    path('books/', BookList.as_view(), name='book-list'),
    path('auth-token/', obtain_auth_token, name='api_token_auth'),
    path('register/', register_user, name='api_register'),  # User registration
    path('', include(router.urls)),
]
