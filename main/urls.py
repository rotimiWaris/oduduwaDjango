from django.contrib.auth.decorators import login_required, permission_required
from django.urls import path
from .views import (
    HomeView,
    ShowProfilePageView,
    EditProfilePageView,
)

app_name = 'main'

urlpatterns = [
    path('', HomeView.as_view(), name='index'),
    path('<slug>/accounts/profile/', ShowProfilePageView.as_view(), name='user-profile'),
    path('<slug>/accounts/edit/profile/', login_required(EditProfilePageView.as_view()), name='edit-profile'),
]
