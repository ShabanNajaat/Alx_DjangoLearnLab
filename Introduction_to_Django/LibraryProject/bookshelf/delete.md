# Delete Operation

## Command:
```python
from bookshelf.models import Book

# First retrieve the book
book = Book.objects.get(title="Nineteen Eighty-Four")

# Delete the book
book.delete()
print("Book deleted successfully")

# Confirm deletion by trying to retrieve all books
remaining_books = Book.objects.all()
print(f"Books remaining in database: {remaining_books.count()}")
