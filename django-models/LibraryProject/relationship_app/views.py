from django.shortcuts import render
from django.views.generic.detail import DetailView  # This exact line must be present
from .models import Library

def list_books(request):
    from relationship_app.models import Book
    books = Book.objects.all()
    return render(request, 'relationship_app/list_books.html', {'books': books})

class LibraryDetailView(DetailView):
    model = Library
    template_name = 'relationship_app/library_detail.html'
    context_object_name = 'library'
