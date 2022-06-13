from rest_framework import serializers
from Room.models import User


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['api_key', 'email', 'name']