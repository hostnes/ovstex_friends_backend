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
