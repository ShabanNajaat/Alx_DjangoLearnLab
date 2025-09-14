from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib import messages
from django.db import models
from .models import Book
from .forms import BookForm  # We'll create this form

# Safe query practices - Using Django ORM properly
def safe_book_search(request):
    """Example of safe query practices"""
    search_query = request.GET.get('q', '')
    
    # UNSAFE: Book.objects.raw(f"SELECT * FROM bookshelf_book WHERE title = '{search_query}'")
    # SAFE: Use Django's ORM with parameterized queries
    
    books = Book.objects.filter(title__icontains=search_query)  # Safe ORM usage
    return render(request, 'bookshelf/search_results.html', {'books': books})

# Using Django Forms for validation
@permission_required('bookshelf.can_create', raise_exception=True)
def book_create(request):
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():  # Django forms handle validation and sanitization
            form.save()
            messages.success(request, 'Book created successfully!')
            return redirect('book_list')
    else:
        form = BookForm()
    
    return render(request, 'bookshelf/book_form.html', {'form': form})

# Safe object retrieval
@permission_required('bookshelf.can_edit', raise_exception=True)
def book_edit(request, pk):
    # Safe: Using get_object_or_404 with proper error handling
    book = get_object_or_404(Book, pk=pk)
    
    if request.method == 'POST':
        form = BookForm(request.POST, instance=book)
        if form.is_valid():
            form.save()
            messages.success(request, 'Book updated successfully!')
            return redirect('book_list')
    else:
        form = BookForm(instance=book)
    
    return render(request, 'bookshelf/book_form.html', {'form': form, 'book': book})
