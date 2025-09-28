from rest_framework import serializers
from .models import Author, Book
from datetime import datetime

class BookSerializer(serializers.ModelSerializer):
    """
    BookSerializer that serializes all fields of the Book model.
    
    Includes custom validation to ensure the publication_year is not in the future.
    """
    
    class Meta:
        model = Book
        fields = '__all__'  # Serializes all fields of the Book model
    
    def validate_publication_year(self, value):
        """
        Custom validation to ensure the publication_year is not in the future.
        """
        current_year = datetime.now().year
        if value > current_year:
            raise serializers.ValidationError(
                f"Publication year cannot be in the future. Current year is {current_year}."
            )
        return value

class AuthorSerializer(serializers.ModelSerializer):
    """
    AuthorSerializer that includes the name field and a nested BookSerializer.
    
    Serializes the related books dynamically using nested serialization.
    """
    
    # Nested BookSerializer to handle the one-to-many relationship
    books = BookSerializer(many=True, read_only=True)
    
    class Meta:
        model = Author
        fields = ['id', 'name', 'books']  # Includes name field and nested books
