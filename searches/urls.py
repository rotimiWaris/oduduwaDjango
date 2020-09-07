from django.urls import path

from .views import (
    SearchBlogView,
)

app_name = 'searches'

urlpatterns = [
    path('', SearchBlogView.as_view(), name='blog-query'),
]
