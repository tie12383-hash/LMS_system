from django.urls import path
from users.views import UserProfileUpdateView

urlpatterns = [
    path('users/<int:pk>/', UserProfileUpdateView.as_view(), name='user-profile-update'),
]