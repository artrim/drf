from django.db import models


NULLABLE = {"blank": True, "null": True}


class Course(models.Model):
    name = models.CharField(max_length=150, verbose_name='название')
    description = models.TextField(verbose_name='описание', **NULLABLE)
    image = models.ImageField(upload_to='materials/course/', verbose_name='превью', **NULLABLE)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Курс'
        verbose_name_plural = 'Курсы'


class Lesson(models.Model):
    name = models.CharField(max_length=150, verbose_name='название')
    description = models.TextField(verbose_name='описание', **NULLABLE)
    image = models.ImageField(upload_to='materials/lesson/', verbose_name='превью', **NULLABLE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='lessons', verbose_name='курс')
    url = models.URLField(max_length=200, verbose_name='ссылка на видео', **NULLABLE)

    def __str__(self):
        return f'Урок: {self.name}, Курс: {self.course}'

    class Meta:
        verbose_name = 'Урок'
        verbose_name_plural = 'Уроки'
