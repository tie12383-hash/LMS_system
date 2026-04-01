from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from users.views import UserRegistrationView, UserProfileView, PaymentViewSet, CreatePaymentView, CheckPaymentStatusView

router = DefaultRouter()
router.register(r'payments', PaymentViewSet, basename='payment')

urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='user-register'),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('users/<int:pk>/', UserProfileView.as_view(), name='user-profile'),
    path('payments/create/', CreatePaymentView.as_view(), name='create-payment'),
    path('payments/<int:payment_id>/status/', CheckPaymentStatusView.as_view(), name='payment-status'),
    path('', include(router.urls)),
]