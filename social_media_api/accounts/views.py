from rest_framework import status, generics, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from .models import CustomUser
from .serializers import (UserSerializer, RegisterSerializer, LoginSerializer, 
                         UserProfileSerializer, FollowSerializer, UserSearchSerializer)

User = get_user_model()

# Keep your existing views and add these:

class UserProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_object(self):
        return self.request.user

class UserDetailView(generics.RetrieveAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = User.objects.all()
    
    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def follow_user(request):
    serializer = FollowSerializer(data=request.data)
    if serializer.is_valid():
        user_to_follow = get_object_or_404(User, id=serializer.validated_data['user_id'])
        
        if user_to_follow == request.user:
            return Response({'error': 'You cannot follow yourself'}, status=status.HTTP_400_BAD_REQUEST)
        
        if request.user.is_following(user_to_follow):
            return Response({'error': 'You are already following this user'}, status=status.HTTP_400_BAD_REQUEST)
        
        request.user.follow(user_to_follow)
        return Response({'message': f'You are now following {user_to_follow.username}'}, status=status.HTTP_200_OK)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def unfollow_user(request):
    serializer = FollowSerializer(data=request.data)
    if serializer.is_valid():
        user_to_unfollow = get_object_or_404(User, id=serializer.validated_data['user_id'])
        
        if not request.user.is_following(user_to_unfollow):
            return Response({'error': 'You are not following this user'}, status=status.HTTP_400_BAD_REQUEST)
        
        request.user.unfollow(user_to_unfollow)
        return Response({'message': f'You have unfollowed {user_to_unfollow.username}'}, status=status.HTTP_200_OK)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def get_following(request):
    following_users = request.user.followers.all()
    serializer = UserSearchSerializer(following_users, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def get_followers(request):
    followers = request.user.following.all()
    serializer = UserSearchSerializer(followers, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def search_users(request):
    username = request.query_params.get('username', '')
    if username:
        users = User.objects.filter(username__icontains=username).exclude(id=request.user.id)
        serializer = UserSearchSerializer(users, many=True)
        return Response(serializer.data)
    return Response([])
