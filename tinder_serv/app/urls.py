from django.urls import path
from .views import *

urlpatterns = [
    path('users/', UserListCreateView.as_view(), name='user-list-create'),
    path('users/<int:pk>/', UserDetailView.as_view(), name='user-detail'),

    path('posts/', PostListCreateView.as_view(), name='user-list-create'),

    path('like/', LikeView.as_view(), name='like-user'),
    path('likes/received/', LikesReceivedView.as_view(), name='likes-received'),
    path('like/<int:pk>/', UserLikeDetailView.as_view(), name='like-detail'),

    path('matches/', MatchesView.as_view(), name='matches'),
]
