from django import forms
from .models import Comment, Blog


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ( "comment",)

class BlogForm(forms.ModelForm):
    class Meta:
        model = Blog
        fields = ['title', 'body', 'image']

