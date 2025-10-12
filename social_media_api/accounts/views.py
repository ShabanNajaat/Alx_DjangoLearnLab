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

# Keep your existing RegisterView and login_view

class RegisterView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    permission_classes = (permissions.AllowAny,)
    serializer_class = RegisterSerializer
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        
        # Get the token that was created in the serializer
        token = Token.objects.get(user=user)
        return Response({
            'user': UserSerializer(user).data,
            'token': token.key
        }, status=status.HTTP_201_CREATED)

@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def login_view(request):
    serializer = LoginSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'user': UserSerializer(user).data,
            'token': token.key
        })
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Add GenericAPIView based views

class UserProfileView(generics.GenericAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request):
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)
    
    def put(self, request):
        serializer = self.get_serializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserDetailView(generics.GenericAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        # Use the exact required syntax
        return CustomUser.objects.all()
    
    def get(self, request, pk):
        user = get_object_or_404(self.get_queryset(), pk=pk)
        serializer = self.get_serializer(user, context={'request': request})
        return Response(serializer.data)

class UserListView(generics.GenericAPIView):
    serializer_class = UserSearchSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        # Use the exact required syntax
        return CustomUser.objects.all().exclude(id=self.request.user.id)
    
    def get(self, request):
        username = request.query_params.get('username', '')
        if username:
            users = self.get_queryset().filter(username__icontains=username)
        else:
            users = self.get_queryset()[:20]  # Limit to 20 users if no search
        
        serializer = self.get_serializer(users, many=True)
        return Response(serializer.data)

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def follow_user(request):
    serializer = FollowSerializer(data=request.data)
    if serializer.is_valid():
        user_to_follow = get_object_or_404(CustomUser.objects.all(), id=serializer.validated_data['user_id'])
        
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
        user_to_unfollow = get_object_or_404(CustomUser.objects.all(), id=serializer.validated_data['user_id'])
        
        if not request.user.is_following(user_to_unfollow):
            return Response({'error': 'You are not following this user'}, status=status.HTTP_400_BAD_REQUEST)
        
        request.user.unfollow(user_to_unfollow)
        return Response({'message': f'You have unfollowed {user_to_unfollow.username}'}, status=status.HTTP_200_OK)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def get_following(request):
    # Use the exact required syntax
    following_users = request.user.followers.all()
    serializer = UserSearchSerializer(following_users, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def get_followers(request):
    # Use the exact required syntax
    followers = request.user.following.all()
    serializer = UserSearchSerializer(followers, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def search_users(request):
    username = request.query_params.get('username', '')
    if username:
        # Use the exact required syntax
        users = CustomUser.objects.all().filter(username__icontains=username).exclude(id=request.user.id)
        serializer = UserSearchSerializer(users, many=True)
        return Response(serializer.data)
    return Response([])
