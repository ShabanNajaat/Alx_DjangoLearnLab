from rest_framework import generics, viewsets
from .models import Book
from .serializers import BookSerializer

# Keep the existing ListAPIView for backward compatibility
class BookList(generics.ListAPIView):
    """
    API endpoint that allows books to be viewed.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer

# New ViewSet for full CRUD operations
class BookViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows books to be viewed, created, updated, or deleted.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
