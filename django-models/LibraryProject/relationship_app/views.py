from django.shortcuts import render
from django.views.generic import DetailView
from .models import Book, Library

# Function-based view to list all books
def list_books(request):
    books = Book.objects.all()
    # For plain text response instead of HTML template
    book_list = []
    for book in books:
        book_list.append(f"{book.title} by {book.author.name}")
    
    return render(request, 'relationship_app/list_books.html', {
        'books': books,
        'book_list_text': "\n".join(book_list)
    })

# Class-based view to display library details
class LibraryDetailView(DetailView):
    model = Library
    template_name = 'relationship_app/library_detail.html'
    context_object_name = 'library'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        library = self.get_object()
        # For plain text response
        book_list = []
        for book in library.books.all():
            book_list.append(f"{book.title} by {book.author.name} (Published {book.publication_year})")
        
        context['book_list_text'] = "\n".join(book_list)
        return context
