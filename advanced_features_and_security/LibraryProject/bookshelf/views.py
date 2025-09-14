from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib import messages
from django.db import models
from .models import Book
from .forms import ExampleForm, BookForm  # MUST USE THIS EXACT IMPORT

def form_example(request):
    """Example view demonstrating secure form handling"""
    if request.method == 'POST':
        form = ExampleForm(request.POST)
        if form.is_valid():
            # Process the secure, validated data
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            message = form.cleaned_data['message']
            
            # Here you would typically save to database or send email
            messages.success(request, f'Thank you {name}! Your message has been received.')
            return redirect('form_example_success')
    else:
        form = ExampleForm()
    
    return render(request, 'bookshelf/form_example.html', {'form': form})

def form_example_success(request):
    """Success page after form submission"""
    return render(request, 'bookshelf/form_success.html')

@permission_required('bookshelf.can_view', raise_exception=True)
def book_list(request):
    books = Book.objects.all()
    return render(request, 'bookshelf/book_list.html', {'books': books})

# ... rest of your existing views ...
