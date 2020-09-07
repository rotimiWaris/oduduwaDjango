from django import forms
from .models import BlogPost, Comment


class BlogPostForm(forms.ModelForm):
    
    class Meta:
        model = BlogPost
        fields = ("title", 'category', 'image', 'content')
        widgets = {
            'title' : forms.TextInput(attrs={'class': 'form-control'}),
            'category' : forms.Select(attrs={'class': 'form-control'}),
            'content' : forms.Textarea(attrs={'class': 'form-control md-textarea rounded-0'})
        }

class UpdateBlogPostForm(forms.ModelForm):
    
    class Meta:
        model = BlogPost
        fields = ("title", 'category', 'image', 'content')
        widgets = {
            'title' : forms.TextInput(attrs={'class': 'form-control'}),
            'category' : forms.Select(attrs={'class': 'form-control'}),
            'content' : forms.Textarea(attrs={'class': 'form-control md-textarea rounded-0'})
        }

class BlogPostCommentForm(forms.ModelForm):
    
    class Meta:
        model = Comment
        fields = ("body",)
        widgets = {
            'body' : forms.Textarea(attrs={
                'class': 'form-control w-100',
                'id': "comment",
                'cols': '30',
                'rows': '9',
                'placeholder': 'Write Comment',
                })
        }