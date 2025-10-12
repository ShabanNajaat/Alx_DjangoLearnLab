from django.urls import path
from .views import NotificationListView, NotificationDetailView, notification_stats, mark_all_read

urlpatterns = [
    path('', NotificationListView.as_view(), name='notification-list'),
    path('stats/', notification_stats, name='notification-stats'),
    path('mark-all-read/', mark_all_read, name='mark-all-read'),
    path('<int:pk>/', NotificationDetailView.as_view(), name='notification-detail'),
]
