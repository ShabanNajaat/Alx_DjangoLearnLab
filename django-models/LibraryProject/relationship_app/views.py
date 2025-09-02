from django.shortcuts import render
from .models import Book, Library

def list_books(request):
    books = Book.objects.all()
    return render(request, 'list_books.html', {'books': books})

from django.views import generic

class LibraryDetailView(generic.DetailView):
    model = Library
    template_name = 'library_detail.html'
