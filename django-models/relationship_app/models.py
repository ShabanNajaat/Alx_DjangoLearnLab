from django.db import models

class Library(models.Model):
    name = models.CharField(max_length=100)
    books = models.ManyToManyField('Book')
    
    def _str_(self):
        return self.name

# ... other models (Author, Book, Librarian)
