from rest_framework import serializers

from materials.models import Course, Lesson
from materials.validators import url_validator


class LessonSerializer(serializers.ModelSerializer):
    url = serializers.CharField(validators=[url_validator])

    class Meta:
        model = Lesson
        fields = '__all__'


class CourseSerializer(serializers.ModelSerializer):
    lessons_count = serializers.SerializerMethodField()
    lessons = LessonSerializer(many=True, read_only=True)

    def get_lessons_count(self, obj):
        return obj.lessons.count()

    class Meta:
        model = Course
        fields = '__all__'
