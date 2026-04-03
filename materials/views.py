from rest_framework import viewsets, generics
from materials.models import Course, Lesson
from materials.serializers import CourseSerializer, LessonSerializer
from materials.paginators import CoursePaginator, LessonPaginator
from materials.tasks import send_course_update_notification

class CourseViewSet(viewsets.ModelViewSet):
    pagination_class = CoursePaginator
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

    def perform_update(self, serializer):
        course = serializer.save()
        # Запускаем задачу асинхронно через 5 секунд, чтобы дать время завершить транзакцию
        send_course_update_notification.apply_async((course.id,), countdown=5)

class LessonListCreateView(generics.ListCreateAPIView):
    pagination_class = LessonPaginator
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer

class LessonRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
