from rest_framework import generics
from django_filters import rest_framework  # MUST HAVE THIS EXACT IMPORT
from rest_framework.filters import SearchFilter, OrderingFilter
from .models import Book, Author
from .serializers import BookSerializer, AuthorSerializer

class BookListView(generics.ListAPIView):
    """
    ListView for retrieving all books with filtering, searching, and ordering.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    
    # Step 1: Set Up Filtering - integrate Django REST Framework's filtering capabilities
    filter_backends = [rest_framework.DjangoFilterBackend, SearchFilter, OrderingFilter]
    
    # Filter by various attributes like title, author, and publication_year
    filterset_fields = ['title', 'author__name', 'publication_year']
    
    # Step 2: Implement Search Functionality - enable search on title and author
    search_fields = ['title', 'author__name']
    
    # Step 3: Configure Ordering - allow ordering by title and publication_year
    ordering_fields = ['title', 'publication_year']
    ordering = ['title']

class BookDetailView(generics.RetrieveAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

class BookCreateView(generics.CreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

class BookUpdateView(generics.UpdateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

class BookDeleteView(generics.DestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

class AuthorListView(generics.ListAPIView):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer

class AuthorDetailView(generics.RetrieveAPIView):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
