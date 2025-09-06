from django.shortcuts import render
from django.views.generic import DetailView
from .models import Library  # This line must be exactly like this

# Function-based view that lists all books
def list_books(request):
    from relationship_app.models import Book
    books = Book.objects.all()
    return render(request, 'list_books.html', {'books': books})

# Class-based view using DetailView for library details
class LibraryDetailView(DetailView):
    model = Library
    template_name = 'library_detail.html'
    context_object_name = 'library'
