from rest_framework import serializers

from users.models import Payment, User, Subscribe


class PaymentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Payment
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = '__all__'

class SubscribeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Subscribe
        fields = "__all__"
