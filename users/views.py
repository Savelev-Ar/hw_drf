from rest_framework import generics, filters

from users.serializers import PaymentSerializer, UserSerializer
from users.models import Payment, User

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

    def perform_create(self, serializer):
        user = serializer.save(is_active=True)
        user.set_password(user.password)
        user.save()
