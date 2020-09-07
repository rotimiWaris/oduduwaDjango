from django.contrib.auth.decorators import login_required, permission_required
from django.urls import path
from .views import (
    BlogPostHomeView,
    BlogPostDetailView,
    BlogPostCreateView,
    BlogPostUpdateView,
    BlogPostDeleteView,
    CategoryView,
    LikeView,
    CommentDeleteView,
    CommentEditView,
)

app_name = 'blog'

urlpatterns = [
    path('', BlogPostHomeView.as_view(), name='blogs'),
    path('create/', login_required(BlogPostCreateView.as_view()), name='create'),
    path('edit/<slug>/', login_required(BlogPostUpdateView.as_view()), name='update'),
    path('delete/<slug>/', login_required(BlogPostDeleteView.as_view()), name='delete'),
    path('<slug>/', BlogPostDetailView.as_view(), name='detail'),
    path('categories/<cat>/', CategoryView, name='category'),
    path('like/<slug>/', LikeView, name='like-post'),
    path('delete/comment/<int:pk>/', login_required(CommentDeleteView.as_view()), name='delete-comment'),
    path('edit/comment/<int:pk>/', login_required(CommentEditView.as_view()), name='edit-comment'),
]
