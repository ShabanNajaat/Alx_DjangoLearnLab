from django.db import models

class Author(models.Model):
    """
    Author model representing a book author.
    
    Fields:
    - name: a string field to store the author's name (CharField with max_length=100)
    """
    name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name

class Book(models.Model):
    """
    Book model representing a published book.
    
    Fields:
    - title: a string field for the book's title (CharField with max_length=200)
    - publication_year: an integer field for the year the book was published (IntegerField)
    - author: a foreign key linking to the Author model (ForeignKey with on_delete=CASCADE)
    
    Establishes a one-to-many relationship from Author to Books.
    """
    title = models.CharField(max_length=200)
    publication_year = models.IntegerField()
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='books')
    
    def __str__(self):
        return f"{self.title} by {self.author.name}"
