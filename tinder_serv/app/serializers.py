from rest_framework import serializers
from .models import *


class RegionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Region
        fields = ['id', 'title']


class CompatibilitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Compatibility
        fields = ['id', 'title', 'photo', 'description']


class UserSerializer(serializers.ModelSerializer):
    region = RegionSerializer(required=False, allow_null=True)
    compatibility = CompatibilitySerializer(required=False, allow_null=True)

    class Meta:
        model = User
        fields = ['id', 'photo', 'email', 'name', 'gender', "password", 'compatibility', 'region']


class PostSerializer(serializers.ModelSerializer):
    user_data = UserSerializer(source='user', read_only=True)
    class Meta:
        model = Post
        fields = ['text', 'photo', 'date_created', 'user', 'user_data']


class UserLikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserLike
        fields = ['from_user', 'to_user', 'created_at']

