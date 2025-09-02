# Views and URL Configuration

## Views Implemented:

### 1. Function-based View: list_books
- Lists all books in the database
- URL: /books/
- Template: list_books.html

### 2. Class-based View: LibraryDetailView (using DetailView)
- Displays details for a specific library
- URL: /library/<int:pk>/
- Template: library_detail.html

## URL Patterns:
- Function-based: path('books/', views.list_books, name='list_books')
- Class-based: path('library/<int:pk>/', views.LibraryDetailView.as_view(), name='library_detail')
