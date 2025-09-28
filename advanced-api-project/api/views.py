from rest_framework import generics, permissions
from .models import Book, Author
from .serializers import BookSerializer, AuthorSerializer

class BookListView(generics.ListAPIView):
    """
    ListView for retrieving all books.
    Read-only access for all users.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.AllowAny]  # Allow unauthenticated read access


class BookDetailView(generics.RetrieveAPIView):
    """
    DetailView for retrieving a single book by ID.
    Read-only access for all users.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.AllowAny]  # Allow unauthenticated read access


class BookCreateView(generics.CreateAPIView):
    """
    CreateView for adding a new book.
    Restricted to authenticated users only.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]  # Restrict to authenticated users


class BookUpdateView(generics.UpdateAPIView):
    """
    UpdateView for modifying an existing book.
    Restricted to authenticated users only.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]  # Restrict to authenticated users


class BookDeleteView(generics.DestroyAPIView):
    """
    DeleteView for removing a book.
    Restricted to authenticated users only.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]  # Restrict to authenticated users


class AuthorListView(generics.ListAPIView):
    """
    ListView for retrieving all authors with their books.
    Read-only access for all users.
    """
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    permission_classes = [permissions.AllowAny]  # Allow unauthenticated read access


class AuthorDetailView(generics.RetrieveAPIView):
    """
    DetailView for retrieving a single author by ID with their books.
    Read-only access for all users.
    """
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    permission_classes = [permissions.AllowAny]  # Allow unauthenticated read access
