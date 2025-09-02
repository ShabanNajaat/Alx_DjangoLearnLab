from django.http import HttpResponse
from .models import Book

def list_books(request):
    books = Book.objects.all()
    output = ""
    for book in books:
        output += f"{book.title} by {book.author.name}<br>"
    return HttpResponse(output)
    from django.views import generic
from .models import Library

class LibraryDetailView(generic.DetailView):
    model = Library
    template_name = 'relationship_app/library_detail.html'
