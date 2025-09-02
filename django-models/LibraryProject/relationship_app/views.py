from django.shortcuts import render
from django.views.generic import DetailView
from .models import Book, Library  # MUST have this exact import line

# Function-based view that renders a simple text list of book titles and their authors
def list_books(request):
    books = Book.objects.all()
    return render(request, 'relationship_app/list_books.html', {'books': books})

# Class-based view that displays details for a specific library, listing all books available
class LibraryDetailView(DetailView):  # MUST use DetailView
    model = Library  # MUST specify the model
    template_name = 'relationship_app/library_detail.html'
    context_object_name = 'library'
