from django.db import models

class Author(models.Model):
    """
    Author model representing a book author.
    
    Fields:
    - name: CharField storing the author's name (max_length=100)
    
    Relationships:
    - One-to-many relationship with Book model (Author can have multiple Books)
    """
    name = models.CharField(max_length=100)
    
    def _str_(self):
        return self.name

class Book(models.Model):
    """
    Book model representing a published book.
    
    Fields:
    - title: CharField for the book's title (max_length=200)
    - publication_year: IntegerField for the year the book was published
    - author: ForeignKey linking to the Author model (one-to-many relationship)
    
    Validation:
    - publication_year should not be in the future (handled in serializer)
    """
    title = models.CharField(max_length=200)
    publication_year = models.IntegerField()
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='books')
    
    def _str_(self):
        return f"{self.title} by {self.author.name}"
