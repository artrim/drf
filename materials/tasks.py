from celery import shared_task
from config import settings
from django.core.mail import send_mail

from materials.models import Subscription


@shared_task
def send_information_about_course_update(course_id):
    subscriptions = Subscription.objects.filter(course=course_id)
    if subscriptions:
        course_name = subscriptions[0].course.name
        emails = []
        for subscription in subscriptions:
            emails.append(subscription.user.email)

            send_mail(f'Обновление курса {course_name}', 'Курс, на который вы подписаны, обновлен',
                      settings.EMAIL_HOST_USER, emails)
