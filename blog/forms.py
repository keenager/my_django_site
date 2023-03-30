from django import forms
from .models import BlogPost


class BlogPostForm(forms.ModelForm):
    class Meta:
        model = BlogPost
        fields = ['title', 'tag', 'content']
        labels = {
            'title': '제목',
            'tag': '태그',
            'content': '내용',
        }
