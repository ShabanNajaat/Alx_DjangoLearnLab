from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Book

@api_view(['GET'])
def book_list(request):
    books = Book.objects.all()
    data = [{'title': book.title, 'author': book.author} for book in books]
    return Response(data)
