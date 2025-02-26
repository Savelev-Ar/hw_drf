from rest_framework import generics, filters

from users.serializers import PaymentSerializer
from users.models import Payment

from django_filters.rest_framework import DjangoFilterBackend


class PaymentListAPIView(generics.ListAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer

    filter_backends = (filters.OrderingFilter, DjangoFilterBackend,)
    filterset_fields = ('paid_course', 'paid_lesson', 'payment_method')
    ordering_fields = ('date_of_payment',)
