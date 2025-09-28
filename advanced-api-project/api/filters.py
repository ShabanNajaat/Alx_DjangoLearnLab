import django_filters
from .models import Book

class BookFilter(django_filters.FilterSet):
    """
    FilterSet for Book model to enable advanced filtering capabilities.
    
    Provides filtering on:
    - title: Case-insensitive contains search
    - author: Filter by author name (exact match)
    - publication_year: Exact year, range, and comparison filters
    """
    
    title = django_filters.CharFilter(lookup_expr='icontains', label='Title contains')
    author = django_filters.CharFilter(field_name='author__name', lookup_expr='icontains', label='Author name contains')
    publication_year = django_filters.NumberFilter(label='Exact publication year')
    publication_year__gt = django_filters.NumberFilter(
        field_name='publication_year', 
        lookup_expr='gt', 
        label='Publication year greater than'
    )
    publication_year__lt = django_filters.NumberFilter(
        field_name='publication_year', 
        lookup_expr='lt', 
        label='Publication year less than'
    )
    publication_year_range = django_filters.RangeFilter(
        field_name='publication_year',
        label='Publication year range (e.g., 1900-2000)'
    )
    
    class Meta:
        model = Book
        fields = ['title', 'author', 'publication_year']
