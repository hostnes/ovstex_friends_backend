from rest_framework import serializers
from .models import *


class RegionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Region
        fields = ['id', 'title']


class PersonalityTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PersonalityType
        fields = ['id', 'name', 'description', 'photo']
    def get_photo(self, obj):
        request = self.context.get('request')
        if obj.photo and hasattr(obj.photo, 'url'):
            return request.build_absolute_uri(obj.photo.url)
        return None

class CompatibilitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Compatibility
        fields = ['id', 'title', 'photo', 'description']
    def get_photo(self, obj):
        request = self.context.get('request')
        if obj.photo and hasattr(obj.photo, 'url'):
            return request.build_absolute_uri(obj.photo.url)
        return None

class UserSerializer(serializers.ModelSerializer):
    region_detail = RegionSerializer(source='region', read_only=True)
    compatibility = CompatibilitySerializer(required=False, allow_null=True)
    personality_type = PersonalityTypeSerializer(required=False, allow_null=True)

    class Meta:
        model = User
        fields = ['id', 'photo', 'email', 'name', 'gender', "password", "date_of_birth", 'compatibility', 'region_detail', 'region', 'personality_type', 'is_verified']

    def get_photo(self, obj):
        request = self.context.get('request')
        if obj.photo and hasattr(obj.photo, 'url'):
            return request.build_absolute_uri(obj.photo.url)
        return None

class PostSerializer(serializers.ModelSerializer):
    user_data = UserSerializer(source='user', read_only=True)
    class Meta:
        model = Post
        fields = ['text', 'photo', 'date_created', 'user', 'user_data']


class UserLikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserLike
        fields = ['id', 'from_user', 'to_user', 'created_at', 'is_already_liked']


class MessageSerializer(serializers.ModelSerializer):
    sender = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())  # Use PrimaryKeyRelatedField for sender
    sender_detail = UserSerializer(source='sender', read_only=True)

    class Meta:
        model = Message
        fields = ['id', 'conversation', 'sender', 'text', 'sent_at', 'sender_detail']


class ConversationSerializer(serializers.ModelSerializer):
    # Accept IDs as input while returning full user data on output
    participant_ids = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        many=True,
        write_only=True,
        source='participants'  # This maps to the participants field on the model
    )
    participants = UserSerializer(many=True, read_only=True)
    last_message = serializers.SerializerMethodField()

    class Meta:
        model = Conversation
        fields = ['id', 'participant_ids', 'participants', 'last_message', 'created_at', 'updated_at']

    def get_last_message(self, obj):
        last_message = obj.messages.last()
        return MessageSerializer(last_message).data if last_message else None

    def create(self, validated_data):
        # Extract participants from validated data
        participants = validated_data.pop('participants')
        conversation = Conversation.objects.create(**validated_data)
        conversation.participants.set(participants)
        return conversation


class ConversationDetailSerializer(serializers.ModelSerializer):
    participants = UserSerializer(many=True)
    messages = serializers.SerializerMethodField()

    class Meta:
        model = Conversation
        fields = ['id', 'participants', 'messages', 'created_at', 'updated_at']

    def get_messages(self, obj):
        # Retrieve messages and order by date (ascending or descending)
        messages = obj.messages.order_by('-sent_at')  # ascending
        return MessageSerializer(messages, many=True).data


class AnswerOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnswerOption
        fields = ['id', 'text']

class QuestionSerializer(serializers.ModelSerializer):
    options = AnswerOptionSerializer(many=True)

    class Meta:
        model = Question
        fields = ['id', 'text', 'options']

class TestSerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(many=True)

    class Meta:
        model = Test
        fields = ['id', 'title', 'description', 'questions']

class TestResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = TestResult
        fields = ['test', 'yes_count', 'no_count']
