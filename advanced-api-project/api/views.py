from rest_framework import generics
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated, AllowAny
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from .models import Book, Author
from .serializers import BookSerializer, AuthorSerializer
from .filters import BookFilter  # Import our custom filter

class BookListView(generics.ListAPIView):
    """
    ListView for retrieving all books with advanced filtering, searching, and ordering capabilities.
    
    Filtering Features:
    - Filter by title (contains, case-insensitive)
    - Filter by author name (contains, case-insensitive) 
    - Filter by publication year (exact, greater than, less than, range)
    
    Search Features:
    - Search across title and author fields
    
    Ordering Features:
    - Order by any book field (title, publication_year, author__name)
    - Default ordering by title
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [AllowAny]
    
    # Filter, Search, and Ordering configuration
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = BookFilter  # Use our custom BookFilter
    search_fields = ['title', 'author__name']  # Fields to search across
    ordering_fields = ['title', 'publication_year', 'author__name']  # Fields available for ordering
    ordering = ['title']  # Default ordering

class BookDetailView(generics.RetrieveAPIView):
    """
    DetailView for retrieving a single book by ID.
    Read-only access for all users.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [AllowAny]

class BookCreateView(generics.CreateAPIView):
    """
    CreateView for adding a new book.
    Restricted to authenticated users only.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]

class BookUpdateView(generics.UpdateAPIView):
    """
    UpdateView for modifying an existing book.
    Restricted to authenticated users only.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]

class BookDeleteView(generics.DestroyAPIView):
    """
    DeleteView for removing a book.
    Restricted to authenticated users only.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]

class AuthorListView(generics.ListAPIView):
    """
    ListView for retrieving all authors with their books.
    Read-only access for all users.
    """
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    permission_classes = [AllowAny]

class AuthorDetailView(generics.RetrieveAPIView):
    """
    DetailView for retrieving a single author by ID with their books.
    Read-only access for all users.
    """
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    permission_classes = [AllowAny]
