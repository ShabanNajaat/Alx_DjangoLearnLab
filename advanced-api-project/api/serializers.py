from rest_framework import serializers
from .models import Author, Book
from datetime import datetime

class BookSerializer(serializers.ModelSerializer):
    """
    Serializer for the Book model.
    
    Handles serialization/deserialization of Book instances.
    Includes custom validation for publication_year field.
    
    Fields:
    - All fields from Book model: id, title, publication_year, author
    
    Validation:
    - publication_year cannot be in the future
    """
    
    class Meta:
        model = Book
        fields = '_all_'  # Include all fields from the Book model
    
    def validate_publication_year(self, value):
        """
        Custom validation for publication_year field.
        
        Ensures that the publication year is not in the future.
        
        Args:
            value (int): The publication year to validate
            
        Returns:
            int: The validated publication year
            
        Raises:
            serializers.ValidationError: If publication year is in the future
        """
        current_year = datetime.now().year
        if value > current_year:
            raise serializers.ValidationError(
                f"Publication year cannot be in the future. Current year is {current_year}."
            )
        return value

class AuthorSerializer(serializers.ModelSerializer):
    """
    Serializer for the Author model with nested Book serialization.
    
    Handles serialization/deserialization of Author instances.
    Includes nested serialization of related Book objects.
    
    Fields:
    - id: Author ID
    - name: Author's name
    - books: Nested serialization of related books (read-only)
    
    The nested books are serialized using BookSerializer to show
    complete book details for each related book.
    """
    
    # Nested serializer for related books
    books = BookSerializer(many=True, read_only=True)
    
    class Meta:
        model = Author
        fields = ['id', 'name', 'books']  # Include author fields and nested books
