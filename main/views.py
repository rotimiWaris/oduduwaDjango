from django.shortcuts import render
from django.views.generic import ListView, DetailView, UpdateView
from django.shortcuts import render, get_object_or_404, redirect, get_list_or_404
from django.contrib.auth.decorators import login_required
from django.urls import reverse, reverse_lazy
from blog.models import BlogPost, UserProfile
from .forms import EditProfilePageForm

# Create your views here.

class HomeView(ListView):
    model = BlogPost
    # context_object_name = 
    template_name='index.html'
    
    
class ShowProfilePageView(DetailView):
    model = UserProfile
    template_name='user-profile.html'
    # slug_field = 'user'
    # slug_url_kwarg = 'username'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        page_user = get_object_or_404(UserProfile, slug=self.kwargs['slug'].replace('.', ''))
        
        context['page_user'] = page_user
        return context
    

class EditProfilePageView(UpdateView):
    model = UserProfile
    template_name = "edit_profile.html"
    form_class = EditProfilePageForm
    # fields = ['bio', 'profile_pic', 'class_name', 'role']
    success_url = reverse_lazy('main:index')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        page_user = get_object_or_404(UserProfile, slug=self.kwargs['slug'].replace('.', ''))
        
        context['page_user'] = page_user
        return context
    
