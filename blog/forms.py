from django import forms
from .models import *
import re
from django.core.exceptions import ValidationError


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = (
            'title',
            'text',
            'category',
            'published'
        )
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'text': forms.Textarea(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'})
        }

    def clean_title(self):
        title = self.cleaned_data['title']
        if re.match(r'\d', title):
            raise ValidationError('In title not a number')
        return title


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comments
        fields = (
            'user',
            'title'
        )
        widgets = {
            'user': forms.Select(attrs={'class': 'form-control'}),
            'title': forms.Textarea(attrs={'class': 'form-control'})
        }