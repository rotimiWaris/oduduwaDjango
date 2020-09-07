from django import forms
from blog.models import UserProfile


class EditProfilePageForm(forms.ModelForm):
    
    class Meta:
        model = UserProfile
        fields = ('bio', 'profile_pic', 'class_name', 'role')
        widgets = {
            'bio' : forms.Textarea(attrs={'class': 'form-control md-textarea rounded-0'}),
            'class_name' : forms.Select(attrs={'class': 'form-control'}),
            'role' : forms.Select(attrs={'class': 'form-control'}),
        }