from django.shortcuts import render
from django.views import generic
from .models import Book, Library

def list_books(request):
    books = Book.objects.all()
    return render(request, 'relationship_app/list_books.html', {'books': books})

class LibraryDetailView(generic.DetailView):
    model = Library
    template_name = 'relationship_app/library_detail.html'
