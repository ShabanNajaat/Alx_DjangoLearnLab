from rest_framework import generics, status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from .models import Notification
from .serializers import NotificationSerializer, NotificationUpdateSerializer

class NotificationListView(generics.ListAPIView):
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return Notification.objects.filter(recipient=self.request.user).select_related('actor')

class NotificationDetailView(generics.RetrieveUpdateAPIView):
    serializer_class = NotificationUpdateSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return Notification.objects.filter(recipient=self.request.user)

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def notification_stats(request):
    total = Notification.objects.filter(recipient=request.user).count()
    unread = Notification.objects.filter(recipient=request.user, read=False).count()
    
    return Response({
        'total_notifications': total,
        'unread_notifications': unread
    })

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def mark_all_read(request):
    Notification.objects.filter(recipient=request.user, read=False).update(read=True)
    return Response({'message': 'All notifications marked as read'})
