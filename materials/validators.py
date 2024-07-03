from rest_framework.serializers import ValidationError


def url_validator(value):
    if 'youtube.com' not in value:
        raise ValidationError('Нельзя прикреплять ссылки на сторонние сайты, кроме youtube.com')
