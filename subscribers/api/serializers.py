from rest_framework.serializers import ModelSerializer
from subscribers.models import Subscribers


class SubscribersSerializer(ModelSerializer):

    class Meta:
        model = Subscribers
        fields = '__all__'
