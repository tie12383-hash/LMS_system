from django.urls import path, include
from rest_framework.routers import DefaultRouter
from users.views import UserProfileUpdateView, PaymentViewSet

router = DefaultRouter()
router.register(r'payments', PaymentViewSet, basename='payment')

urlpatterns = [
    path('users/<int:pk>/', UserProfileUpdateView.as_view(), name='user-profile-update'),
    path('', include(router.urls)),
]