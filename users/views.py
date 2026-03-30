from rest_framework import generics, permissions, viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from users.models import User, Payment
from users.serializers import (
    UserRegistrationSerializer,
    UserSerializer,
    UserPublicSerializer,
    PaymentSerializer
)
from users.permissions import IsOwner

class UserRegistrationView(generics.CreateAPIView):
    serializer_class = UserRegistrationSerializer
    permission_classes = [permissions.AllowAny]

class UserProfileView(generics.RetrieveUpdateAPIView):
    queryset = User.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        if self.request.user == self.get_object():
            return UserSerializer
        return UserPublicSerializer

class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['course', 'lesson', 'payment_method']
    ordering_fields = ['payment_date']
    ordering = ['-payment_date']
    permission_classes = [permissions.IsAuthenticated]
