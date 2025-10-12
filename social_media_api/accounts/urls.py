from django.urls import path
from .views import (RegisterView, login_view, UserProfileView, 
                   follow_user, unfollow_user, get_following, 
                   get_followers, search_users, UserDetailView)

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', login_view, name='login'),
    path('profile/', UserProfileView.as_view(), name='profile'),
    path('users/<int:pk>/', UserDetailView.as_view(), name='user-detail'),
    path('follow/<int:user_id>/', follow_user, name='follow-user'),
    path('unfollow/<int:user_id>/', unfollow_user, name='unfollow-user'),
    path('following/', get_following, name='get-following'),
    path('followers/', get_followers, name='get-followers'),
    path('search/', search_users, name='search-users'),
]
