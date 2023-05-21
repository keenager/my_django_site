from django import forms
from .models import BlogPost


class BlogPostForm(forms.ModelForm):
    class Meta:
        model = BlogPost
        fields = ['title', 'tag', 'content', 'private']
        labels = {
            'title': '제목',
            'tag': '태그',
            'content': '내용',
            'private': '공개 여부',
        }
