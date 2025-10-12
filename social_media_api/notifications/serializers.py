from rest_framework import serializers
from .models import Notification
from django.contrib.auth import get_user_model

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email')

class NotificationSerializer(serializers.ModelSerializer):
    actor = UserSerializer(read_only=True)
    
    class Meta:
        model = Notification
        fields = ('id', 'recipient', 'actor', 'verb', 'target_object_id', 'timestamp', 'read')
        read_only_fields = ('id', 'recipient', 'actor', 'verb', 'target_object_id', 'timestamp')

class NotificationUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ('read',)
