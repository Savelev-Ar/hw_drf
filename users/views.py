from django.shortcuts import get_object_or_404
from rest_framework import generics, filters
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from users.serializers import PaymentSerializer, UserSerializer, SubscribeSerializer
from users.models import Payment, User, Subscribe, Course

from django_filters.rest_framework import DjangoFilterBackend


class PaymentListAPIView(generics.ListAPIView):
    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()

    filter_backends = (filters.OrderingFilter, DjangoFilterBackend,)
    filterset_fields = ('paid_course', 'paid_lesson', 'payment_method')
    ordering_fields = ('payment_date',)


class UserCreateAPIView(generics.CreateAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        user = serializer.save(is_active=True)
        user.set_password(user.password)
        user.save()


class UserListAPIView(generics.ListAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()


class UserRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()


class UserUpdateAPIView(generics.UpdateAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()


class UserDestroyAPIView(generics.DestroyAPIView):
    queryset = User.objects.all()


class SubscribeView(generics.GenericAPIView):
    serializer_class = SubscribeSerializer
    queryset = Subscribe.objects.all()

    def post(self, *args, **kwargs):
        user = self.request.user
        course_id = self.request.data.get('course')
        course_item = get_object_or_404(Course, pk=course_id)
        subs_item = Subscribe.objects.all().filter(user=user).filter(course=course_item)

        # Если подписка у пользователя на этот курс есть - удаляем ее
        if subs_item.exists():
            subs_item.delete()
            message = 'подписка удалена'
        # Если подписки у пользователя на этот курс нет - создаем ее
        else:
            Subscribe.objects.create(user=user, course=course_item)
            message = 'подписка добавлена'
        # Возвращаем ответ в API
        return Response({"message": message})
