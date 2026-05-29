from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from users.models import Subscription
from datetime import timedelta
from django.utils import timezone
from materials.models import Course


@shared_task
def send_course_update_notification(course_id):
    """Отправляет email всем подписчикам курса о его обновлении."""
    try:
        course = Course.objects.get(id=course_id)
    except Course.DoesNotExist:
        return

    # Проверка, не отправляли ли уведомление менее 4 часов назад
    if course.last_notification_sent and (timezone.now() - course.last_notification_sent) < timedelta(hours=4):
        return  # слишком рано для нового уведомления

    subscriptions = Subscription.objects.filter(course=course).select_related('user')
    if not subscriptions:
        return

    subject = f'Курс "{course.title}" был обновлён'
    message = f'Здравствуйте! Курс "{course.title}" получил обновления. Зайдите в систему, чтобы ознакомиться.'

    emails = [sub.user.email for sub in subscriptions]
    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, emails, fail_silently=False)

    # Обновление времени последнего уведомления
    course.last_notification_sent = timezone.now()
    course.save(update_fields=['last_notification_sent'])


@shared_task
def deactivate_inactive_users():
    """Блокирует пользователей, которые не заходили более месяца."""
    month_ago = timezone.now() - timedelta(days=30)
    from users.models import User
    inactive_users = User.objects.filter(last_login__lt=month_ago, is_active=True)
    count = inactive_users.update(is_active=False)
    return f'Deactivated {count} users'
