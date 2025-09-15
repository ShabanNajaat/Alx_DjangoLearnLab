# First API Endpoint Documentation

## Endpoint Created:
- *URL*: /api/books/
- *Method*: GET
- *Response*: JSON list of all books

## Components:

### 1. Serializer (api/serializers.py)
```python
class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = '_all_'
