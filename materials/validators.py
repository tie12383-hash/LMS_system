import re
from django.core.exceptions import ValidationError


def validate_youtube_url(value):
    """Проверяет, что ссылка ведёт на youtube.com или youtu.be"""
    pattern = r'^(https?://)?(www\.)?(youtube\.com|youtu\.be)/'
    if not re.match(pattern, value):
        raise ValidationError('Разрешены только ссылки на YouTube.')
