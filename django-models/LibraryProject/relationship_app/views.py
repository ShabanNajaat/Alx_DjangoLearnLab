from django.shortcuts import render, redirect
from django.contrib.auth import login  # Explicit import for login
from django.contrib.auth.forms import UserCreationForm  # Explicit import for UserCreationForm
from django.views.generic.detail import DetailView
from .models import Library

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

# Registration view
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Use the imported login function
            return redirect('list_books')
    else:
        form = UserCreationForm()  # Use the imported UserCreationForm
    return render(request, 'relationship_app/register.html', {'form': form})
