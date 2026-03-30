from rest_framework import serializers
from users.models import User, Payment
from materials.models import Course, Lesson

class PaymentSerializer(serializers.ModelSerializer):
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

class UserPublicSerializer(serializers.ModelSerializer):
    """Для просмотра чужого профиля (без приватных полей)"""
    class Meta:
        model = User
        fields = ['id', 'email', 'phone', 'city', 'avatar']

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['email', 'password', 'phone', 'city', 'avatar']

    def create(self, validated_data):
        user = User.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password'],
            phone=validated_data.get('phone', ''),
            city=validated_data.get('city', ''),
            avatar=validated_data.get('avatar')
        )
        return user