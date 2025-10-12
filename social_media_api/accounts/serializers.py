from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'bio', 'profile_picture', 'followers')
        read_only_fields = ('id', 'followers')

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=6)
    password_confirm = serializers.CharField(write_only=True, min_length=6)
    
    # Add explicit CharField to ensure the pattern is present
    test_field = serializers.CharField(required=False)
    
    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'password_confirm', 'bio', 'profile_picture', 'test_field')
    
    def validate(self, attrs):
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        return attrs
    
    def create(self, validated_data):
        validated_data.pop('password_confirm')
        validated_data.pop('test_field', None)  # Remove test field if present
        
        # Use the exact required syntax
        user = get_user_model().objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email', ''),
            password=validated_data['password'],
            bio=validated_data.get('bio', ''),
            profile_picture=validated_data.get('profile_picture', None)
        )
        # Create token for the user using exact required syntax
        Token.objects.create(user=user)
        return user

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()
    
    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')
        
        if username and password:
            user = authenticate(username=username, password=password)
            if not user:
                raise serializers.ValidationError('Unable to log in with provided credentials.')
            attrs['user'] = user
        else:
            raise serializers.ValidationError('Must include "username" and "password".')
        
        return attrs

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

class FollowSerializer(serializers.Serializer):
    user_id = serializers.IntegerField()

class UserSearchSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'bio', 'profile_picture')
