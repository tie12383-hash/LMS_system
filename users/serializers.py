from rest_framework import serializers
from users.models import User, Payment
from materials.serializers import CourseSerializer, LessonSerializer

class PaymentSerializer(serializers.ModelSerializer):
    # Для вывода названий курса добавим поля
    course_title = serializers.CharField(source='course.title', read_only=True)
    lesson_title = serializers.CharField(source='lesson.title', read_only=True)

    class Meta:
        model = Payment
        fields = ['id', 'payment_date', 'course', 'lesson', 'amount', 'payment_method',
                  'course_title', 'lesson_title']

class UserSerializer(serializers.ModelSerializer):
    payments = PaymentSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = ['id', 'email', 'phone', 'city', 'avatar', 'payments']