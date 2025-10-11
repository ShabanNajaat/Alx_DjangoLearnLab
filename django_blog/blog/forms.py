from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Comment

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()
    
    class Meta:
        model = User
        fields = ['username', 'email']

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
    
    def clean_content(self):
        content = self.cleaned_data.get('content')
        if len(content.strip()) < 1:
            raise forms.ValidationError("Comment cannot be empty.")
        if len(content) > 1000:
            raise forms.ValidationError("Comment is too long. Maximum 1000 characters allowed.")
        return content
