from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token

User = get_user_model()

class UserProfileSerializer(serializers.ModelSerializer):
    following_count = serializers.SerializerMethodField()
    followers_count = serializers.SerializerMethodField()
    is_following = serializers.SerializerMethodField()
    
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'bio', 'profile_picture', 
                 'following_count', 'followers_count', 'is_following')
        read_only_fields = ('id', 'following_count', 'followers_count', 'is_following')
    
    def get_following_count(self, obj):
        return obj.get_following_count()
    
    def get_followers_count(self, obj):
        return obj.get_followers_count()
    
    def get_is_following(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return request.user.is_following(obj)
        return False

# Keep your existing serializers and add these:
class FollowSerializer(serializers.Serializer):
    user_id = serializers.IntegerField()

class UserSearchSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'bio', 'profile_picture')
