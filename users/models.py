from django.db import models
from django.contrib.auth.models import AbstractUser

from materials.models import Course, Lesson

NULLABLE = {"blank": True, "null": True}


class User(AbstractUser):
    username = None

    email = models.EmailField(unique=True, verbose_name='почта')

    phone = models.CharField(max_length=35, verbose_name='телефон', **NULLABLE)
    avatar = models.ImageField(upload_to='users/', verbose_name='аватар', **NULLABLE)
    country = models.CharField(max_length=100, verbose_name='страна', **NULLABLE)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.email


class Payments(models.Model):
    METHOD_CHOICES = [
        ('cash', 'оплата наличными'),
        ('non-cash', 'безналичный расчет'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='payment', verbose_name='пользователь',
                             **NULLABLE)
    date_payment = models.DateField(auto_now_add=True, verbose_name='дата оплаты')
    course_paid = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='payment',
                                    verbose_name='оплаченный курс', **NULLABLE)
    lesson_paid = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name='payment',
                                    verbose_name='оплаченный урок', **NULLABLE)
    payment_amount = models.PositiveIntegerField(verbose_name='сумма оплаты')
    payment_method = models.CharField(max_length=50, verbose_name='метод оплаты', choices=METHOD_CHOICES)

    session_id = models.CharField(max_length=255, verbose_name="ID сессии", **NULLABLE)
    payment_link = models.URLField(max_length=400, verbose_name="ссылка на оплату", **NULLABLE)

    class Meta:
        verbose_name = 'Платеж'
        verbose_name_plural = 'Платежи'

    def __str__(self):
        return f'{self.user} - {self.payment_amount}, {self.course_paid if self.course_paid else self.lesson_paid}'
