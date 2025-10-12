from rest_framework import viewsets, status, filters, generics
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.decorators import api_view, permission_classes
from rest_framework import permissions
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404
from .models import Post, Comment, Like
from .serializers import (
    PostSerializer, PostCreateSerializer, 
    CommentSerializer, CommentCreateSerializer,
    LikeSerializer
)
from .permissions import IsAuthorOrReadOnly
from notifications.models import Notification

class PostViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'content']
    filterset_fields = ['author']
    ordering_fields = ['created_at', 'updated_at']
    ordering = ['-created_at']
    
    def get_queryset(self):
        return Post.objects.all().select_related('author').prefetch_related('comments__author', 'likes__user')
    
    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return PostCreateSerializer
        return PostSerializer
    
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
    
    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticatedOrReadOnly])
    def add_comment(self, request, pk=None):
        post = self.get_object()
        serializer = CommentCreateSerializer(data=request.data)
        
        if serializer.is_valid():
            comment = serializer.save(post=post, author=request.user)
            
            # Create notification for post author (if not commenting on own post)
            if post.author != request.user:
                Notification.objects.create(
                    recipient=post.author,
                    actor=request.user,
                    verb='comment',
                    target=post
                )
            
            return Response(CommentSerializer(comment).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def like(self, request, pk=None):
        post = generics.get_object_or_404(Post, pk=pk)
        
        if post.is_liked_by(request.user):
            return Response({'error': 'You have already liked this post'}, status=status.HTTP_400_BAD_REQUEST)
        
        like, created = Like.objects.get_or_create(user=request.user, post=post)
        
        # Create notification for post author (if not liking own post)
        if post.author != request.user:
            Notification.objects.create(
                recipient=post.author,
                actor=request.user,
                verb='like',
                target=post
            )
        
        return Response(LikeSerializer(like).data, status=status.HTTP_201_CREATED)
    
    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def unlike(self, request, pk=None):
        post = generics.get_object_or_404(Post, pk=pk)
        
        if not post.is_liked_by(request.user):
            return Response({'error': 'You have not liked this post'}, status=status.HTTP_400_BAD_REQUEST)
        
        Like.objects.filter(user=request.user, post=post).delete()
        return Response({'message': 'Post unliked successfully'}, status=status.HTTP_200_OK)
    
    @action(detail=True, methods=['get'], permission_classes=[IsAuthenticatedOrReadOnly])
    def likes(self, request, pk=None):
        post = self.get_object()
        likes = post.likes.select_related('user')
        serializer = LikeSerializer(likes, many=True)
        return Response(serializer.data)

class CommentViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]
    serializer_class = CommentSerializer
    
    def get_queryset(self):
        return Comment.objects.all().select_related('author', 'post')
    
    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return CommentCreateSerializer
        return CommentSerializer
    
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def user_feed(request):
    """
    Get posts from users that the current user follows
    """
    if not request.user.is_authenticated:
        return Response({'error': 'Authentication required'}, status=status.HTTP_401_UNAUTHORIZED)
    
    # Get posts from followed users using the exact required syntax
    following_users = request.user.following.all()
    feed_posts = Post.objects.filter(author__in=following_users).order_by('-created_at')
    
    # Apply pagination
    page = request.query_params.get('page', 1)
    page_size = 10
    
    try:
        page = int(page)
    except ValueError:
        page = 1
    
    start_index = (page - 1) * page_size
    end_index = start_index + page_size
    
    paginated_posts = feed_posts[start_index:end_index]
    serializer = PostSerializer(paginated_posts, many=True, context={'request': request})
    
    return Response({
        'posts': serializer.data,
        'page': page,
        'has_next': end_index < feed_posts.count(),
        'total_posts': feed_posts.count()
    })
