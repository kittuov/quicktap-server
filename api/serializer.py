from rest_framework.serializers import ModelSerializer
from django.contrib.auth.models import User
from game.models import Profile, Game


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = {"username", "password"}


class ProfileSerializer(ModelSerializer):
    class Meta:
        model = Profile
        # fields = {"firstName", "lastName", "image", "won", "id"}


class GameSerializer(ModelSerializer):
    class Meta:
        model = Game