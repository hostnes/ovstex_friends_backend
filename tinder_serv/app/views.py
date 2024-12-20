import random
import re
from django.views.decorators.csrf import csrf_exempt

from django.http import HttpResponse
from django.shortcuts import render
from .models import *
from django.shortcuts import get_object_or_404
from rest_framework import generics, serializers, status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import *
from .serializers import *
from django_filters import rest_framework as filters

def is_valid_email(email):
    pattern = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    return re.match(pattern, email) is not None
class UserFilter(filters.FilterSet):
    email = filters.CharFilter(lookup_expr='exact')

    class Meta:
        model = User
        fields = ['email', 'password']


class UserListCreateView(generics.ListCreateAPIView):
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = UserFilter
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_queryset(self):
        user_id = self.request.query_params.get("owner_id")

        if user_id:
            return self.queryset.exclude(id=user_id)
        return self.queryset


class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class RegionListCreateView(generics.ListCreateAPIView):
    queryset = Region.objects.all()
    serializer_class = RegionSerializer


class PostListCreateView(generics.ListCreateAPIView):
    queryset = Post.objects.all().order_by('-date_created')
    serializer_class = PostSerializer


class UserLikeDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = UserLike.objects.all()
    serializer_class = UserLikeSerializer

class LikeView(APIView):
    def post(self, request):
        user_id = request.data.get("user_id")
        target_user_id = request.data.get("target_user_id")

        if not user_id or not target_user_id:
            return Response({"error": "user_id and target_user_id are required"}, status=status.HTTP_400_BAD_REQUEST)

        user = get_object_or_404(User, id=user_id)
        target_user = get_object_or_404(User, id=target_user_id)

        # Лайкнуть пользователя и получить объект UserLike
        user_like, created = UserLike.objects.get_or_create(from_user=user, to_user=target_user)

        # Serialize the UserLike object
        serializer = UserLikeSerializer(user_like)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class LikesReceivedView(APIView):
    def get(self, request):
        user_id = request.query_params.get("user_id")

        if not user_id:
            return Response({"error": "user_id is required"}, status=status.HTTP_400_BAD_REQUEST)

        user = get_object_or_404(User, id=user_id)
        liked_by_users = user.get_likes_received()

        serializer = UserSerializer(liked_by_users, many=True, context={'request': request})
        data = []
        count = 0

        for i in serializer.data:
            try:
                il = UserLike.objects.get(from_user=liked_by_users[count].id, to_user=user_id, is_already_liked="False").id
                i["like"] = il
                data.append(i)
            except:
                pass
            count += 1
        return Response(data, status=status.HTTP_200_OK)


class MatchesView(APIView):
    def get(self, request):
        user_id = request.query_params.get("user_id")

        if not user_id:
            return Response({"error": "user_id is required"}, status=status.HTTP_400_BAD_REQUEST)

        user = get_object_or_404(User, id=user_id)
        matched_users = user.get_mutual_matches()

        serializer = UserSerializer(matched_users, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

class ConversationListCreateView(generics.ListCreateAPIView):
    serializer_class = ConversationSerializer

    def get_queryset(self):
        queryset = Conversation.objects.all().order_by('-updated_at')  # Sort by updated_at in descending order
        user_ids = self.request.query_params.getlist('user_id')

        if user_ids:
            for user_id in user_ids:
                queryset = queryset.filter(participants__id=user_id)

        return queryset.distinct()


class ConversationDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Conversation.objects.all()
    serializer_class = ConversationDetailSerializer


class MessageListCreateView(generics.ListCreateAPIView):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer


class MessageDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer



class TestDetailView(APIView):
    def get(self, request, pk):
        try:
            test = Test.objects.get(pk=pk)
            serializer = TestSerializer(test)
            return Response({
    "id": 1,
    "title": "Тест на тип личности",
    "description": "твой тип решит этот тест",
    "questions": [
        {
            "id": 3,
            "text": "Вы эффективно расставляете приоритеты и планируете задачи, часто завершая их досрочно?",
            "test": 1
        },
        {
            "id": 4,
            "text": "Истории и эмоции людей говорят вам больше, чем цифры и данные?",
            "test": 1
        },
        {
            "id": 5,
            "text": "Даже небольшая ошибка может заставить вас сомневаться в своих способностях и знаниях?",
            "test": 1
        },
        {
            "id": 6,
            "text": "Вы чувствуете себя комфортно, просто подойдя к человеку, который вам интересен, и завязав с ним разговор?",
            "test": 1
        },
        {
            "id": 7,
            "text": "Вы часто позволяете событиям дня разворачиваться самим собой, без предварительного плана?",
            "test": 1
        },
        {
            "id": 8,
            "text": "Вы редко беспокоитесь о том, производите ли вы хорошее впечатление на людей, которых встречаете?",
            "test": 1
        },
        {
            "id": 9,
            "text": "Вам нравится участвовать в командных занятиях?",
            "test": 1
        },
        {
            "id": 10,
            "text": "Вам нравится экспериментировать с новыми и неопробованными подходами?",
            "test": 1
        },
        {
            "id": 11,
            "text": "ы предпочитаете быть деликатным, а не абсолютно честным?",
            "test": 1
        },
        {
            "id": 12,
            "text": "Вы активно ищете новый опыт и области знаний для изучения?",
            "test": 1
        },
        {
            "id": 13,
            "text": "Вы склонны беспокоиться, что ситуация станет хуже?",
            "test": 1
        },
        {
            "id": 14,
            "text": "Вы предпочитаете сначала сделать домашние дела, а потом уже отдыхать?",
            "test": 1
        }
    ]
})
        except Test.DoesNotExist:
            return Response({"error": "Test not found"}, status=status.HTTP_404_NOT_FOUND)

class TestResultView(APIView):
    # def post(self, request, pk):
    #     try:
    #         test = Test.objects.get(pk=pk)
    #         yes_count = request.data.get("yes", 0)
    #         no_count = request.data.get("no", 0)
    #         result = TestResult.objects.create(test=test, yes_count=yes_count, no_count=no_count)
    #         serializer = TestResultSerializer(result)
    #         return Response(serializer.data, status=status.HTTP_201_CREATED)
    #     except Test.DoesNotExist:
    #         return Response({"error": "Test not found"}, status=status.HTTP_404_NOT_FOUND)
    def post(self, request, pk):
        try:
            personality_types = PersonalityType.objects.all()
            if not personality_types.exists():
                return Response({"error": "No personality types available"}, status=status.HTTP_404_NOT_FOUND)

            random_personality = random.choice(personality_types)
            serializer = PersonalityTypeSerializer(random_personality)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class AssignRandomPersonalityTypeView(APIView):
    def post(self, request, pk):
        user_id = request.data.get("user_id")
        if not user_id:
            return Response({"error": "User ID is required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

        try:
            personality_types = PersonalityType.objects.all()
            if not personality_types.exists():
                return Response({"error": "No personality types available"}, status=status.HTTP_404_NOT_FOUND)
            compatibility_types = Compatibility.objects.all()
            random_personality = random.choice(personality_types)
            random_compatibility = random.choice(compatibility_types)
            user.personality_type = random_personality
            user.compatibility = random_compatibility
            user.save()

            serializer = UserSerializer(user, context={"request": request})
            return Response(serializer.data, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class QuestionListCreateView(generics.ListCreateAPIView):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer

class QuestionDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer