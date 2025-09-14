from django import forms
from .models import Book

class ExampleForm(forms.Form):  # MUST HAVE THIS EXACT CLASS NAME
    """Example form for security demonstration"""
    name = forms.CharField(
        max_length=100,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your name'
        })
    )
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your email'
        })
    )
    message = forms.CharField(
        required=True,
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your message',
            'rows': 4
        })
    )

class BookForm(forms.ModelForm):
    """Form for book creation and editing with validation"""
    
    class Meta:
        model = Book
        fields = ['title', 'author', 'publication_year']
        widgets = {
            'publication_year': forms.NumberInput(attrs={
                'min': 1000,
                'max': 2025,
            }),
        }
