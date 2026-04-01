from rest_framework import generics, permissions, viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from users.models import User, Payment
from users.serializers import (
    UserRegistrationSerializer,
    UserSerializer,
    UserPublicSerializer,
    PaymentSerializer
)
from users.permissions import IsOwner
from materials.models import Course
from users.services import create_stripe_product, create_stripe_price, create_checkout_session
from django.conf import settings

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

class CreatePaymentView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        course_id = request.data.get('course_id')
        if not course_id:
            return Response({'error': 'course_id is required'}, status=status.HTTP_400_BAD_REQUEST)
        course = get_object_or_404(Course, id=course_id)

        if Payment.objects.filter(user=request.user, course=course, payment_status='succeeded').exists():
            return Response({'message': 'Курс уже оплачен'}, status=status.HTTP_400_BAD_REQUEST)

        product = create_stripe_product(course)
        price = create_stripe_price(product.id, 1000)
        session = create_checkout_session(
            price_id=price.id,
            success_url=f"{settings.SITE_URL}/payment/success?session_id={{CHECKOUT_SESSION_ID}}",
            cancel_url=f"{settings.SITE_URL}/payment/cancel"
        )

        payment = Payment.objects.create(
            user=request.user,
            course=course,
            amount=1000,
            payment_method='transfer',
            stripe_product_id=product.id,
            stripe_price_id=price.id,
            stripe_session_id=session.id,
            checkout_url=session.url,
            payment_status='pending'
        )
        return Response({
            'payment_id': payment.id,
            'checkout_url': session.url,
            'message': 'Ссылка на оплату создана'
        }, status=status.HTTP_201_CREATED)

class CheckPaymentStatusView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, payment_id):
        payment = get_object_or_404(Payment, id=payment_id, user=request.user)
        from users.services import retrieve_session
        session = retrieve_session(payment.stripe_session_id)
        if session.payment_status == 'paid':
            payment.payment_status = 'succeeded'
            payment.save()
            return Response({'status': 'succeeded'})
        else:
            return Response({'status': 'pending'})
