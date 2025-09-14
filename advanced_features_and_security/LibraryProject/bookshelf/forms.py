from django import forms
from .models import Book

class BookForm(forms.ModelForm):
    """Form for book creation and editing with validation"""
    
    class Meta:
        model = Book
        fields = ['title', 'author', 'publication_year']
        widgets = {
            'publication_year': forms.NumberInput(attrs={
                'min': 1000,
                'max': 2025,  # Current year
            }),
        }
    
    def clean_title(self):
        """Custom validation for title"""
        title = self.cleaned_data.get('title')
        if len(title) < 2:
            raise forms.ValidationError("Title must be at least 2 characters long.")
        return title
    
    def clean_publication_year(self):
        """Custom validation for publication year"""
        year = self.cleaned_data.get('publication_year')
        if year < 1000 or year > 2025:
            raise forms.ValidationError("Please enter a valid publication year.")
        return year
