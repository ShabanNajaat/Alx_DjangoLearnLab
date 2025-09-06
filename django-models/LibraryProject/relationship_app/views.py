from django.shortcuts import render
from django.views.generic import DetailView
from .models import Library  # Explicit import for Library

# Function-based view that lists all books
def list_books(request):
    from .models import Book
    books = Book.objects.all()
    return render(request, 'relationship_app/list_books.html', {'books': books})

# Class-based view using DetailView for library details
class LibraryDetailView(DetailView):
    model = Library
    template_name = 'relationship_app/library_detail.html'
    context_object_name = 'library'
