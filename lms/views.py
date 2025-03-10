from datetime import timedelta, datetime

from rest_framework import viewsets, generics

from lms.models import Course, Lesson
from lms.paginators import LMSPaginator
from lms.serializers import CourseSerializer, LessonSerializer
from users.permissions import IsModerator, IsOwner
from rest_framework.permissions import IsAuthenticated

from lms.tasks import send_email


class CourseViewSet(viewsets.ModelViewSet):
    serializer_class = CourseSerializer
    queryset = Course.objects.all()
    pagination_class = LMSPaginator

    def perform_create(self, serializer):
        course = serializer.save()
        course.owner = self.request.user
        course.save()

    def perform_update(self, serializer, *args, **kwargs):
        course = serializer.save()
        if CourseViewSet.dict_last_updates.get(course):
            last_update = CourseViewSet.dict_last_updates.get(course)
            if datetime.now() - last_update >= timedelta(hours=4):
                send_email.delay(course.pk)
        CourseViewSet.dict_last_updates.update({course: datetime.now()})

    def get_permissions(self):

        if self.action == 'create':
            self.permission_classes = [~IsModerator]
        elif self.action == 'destroy':
            self.permission_classes = [IsOwner]
        elif self.action == 'list':
            self.permission_classes = [IsModerator | IsAuthenticated]
        elif self.action in ['retrieve', 'update']:
            self.permission_classes = [IsOwner | IsModerator]
        return super().get_permissions()


class LessonCreateAPIView(generics.CreateAPIView):
    serializer_class = LessonSerializer
    permission_classes = [~IsModerator]

    def perform_create(self, serializer):
        lesson = serializer.save()
        lesson.owner = self.request.user
        lesson.save()


class LessonListAPIView(generics.ListAPIView):
    serializer_class = LessonSerializer
    permission_classes = [IsModerator | IsOwner]
    pagination_class = LMSPaginator

    def get_queryset(self):
        user = self.request.user
        if user.groups.filter(name='moderators').exists():
            return Lesson.objects.all()
        else:
            return Lesson.objects.filter(owner=user)


class LessonRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsModerator | IsOwner]


class LessonUpdateAPIView(generics.UpdateAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsModerator | IsOwner]


class LessonDestroyAPIView(generics.DestroyAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [~IsModerator | IsOwner]
