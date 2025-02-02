from rest_framework import viewsets, generics
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from materials.models import Course, Lesson, Subscription
from materials.paginators import MyPagination
from materials.permissions import IsModer, IsOwner
from materials.serializers import CourseSerializer, LessonSerializer, SubscriptionSerializer
from materials.tasks import send_information_about_course_update


class CourseViewSet(viewsets.ModelViewSet):
    """Viewset for course"""
    serializer_class = CourseSerializer
    queryset = Course.objects.all()
    pagination_class = MyPagination

    def perform_create(self, serializer):
        new_course = serializer.save()
        new_course.owner = self.request.user
        new_course.save()

    def get_permissions(self):
        if self.action in ['update', 'partial_update', 'list', 'retrieve']:
            self.permission_classes = [IsModer | IsOwner]
        elif self.action == 'create':
            self.permission_classes = [~IsModer]
        elif self.action == 'destroy':
            self.permission_classes = [~IsModer | IsOwner]
        return super().get_permissions()

    def perform_update(self, serializer):
        update_course = serializer.save()
        send_information_about_course_update.delay(update_course.pk)
        update_course.save()


class LessonCreateAPIView(generics.CreateAPIView):
    """Lesson create endpoint"""
    serializer_class = LessonSerializer
    permission_classes = (~IsModer, IsAuthenticated)

    def perform_create(self, serializer):
        new_lesson = serializer.save()
        new_lesson.owner = self.request.user
        new_lesson.save()


class LessonListAPIView(generics.ListAPIView):
    """Lesson list endpoint"""
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    pagination_class = MyPagination


class LessonRetrieveAPIView(generics.RetrieveAPIView):
    """Lesson retrieve endpoint"""
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = (IsAuthenticated, IsModer | IsOwner,)


class LessonUpdateAPIView(generics.UpdateAPIView):
    """Lesson update endpoint"""
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = (IsAuthenticated, IsModer | IsOwner,)


class LessonDestroyAPIView(generics.DestroyAPIView):
    """Lesson destroy endpoint"""
    queryset = Lesson.objects.all()
    permission_classes = (IsAuthenticated, IsOwner | ~IsModer,)


class SubscriptionAPIView(APIView):
    """Subscription endpoint"""
    serializer_class = SubscriptionSerializer
    permission_classes = [IsAuthenticated, IsOwner]

    def post(self, *args, **kwargs):
        user = self.request.user
        course_id = self.request.data.get('course')
        course_item = get_object_or_404(Course, pk=course_id)
        subs_item = Subscription.objects.filter(user=user, course=course_item)
        if subs_item.exists():
            subs_item.delete()
            message = 'Подписка удалена'
        else:
            Subscription.objects.create(user=user, course=course_item)
            message = 'Подписка добавлена'
        return Response({"message": message})
