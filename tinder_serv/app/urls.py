from django.urls import path
from .views import *

urlpatterns = [
    path('users/', UserListCreateView.as_view(), name='user-list-create'),
    path('users/<int:pk>/', UserDetailView.as_view(), name='user-detail'),

    path('regions/', RegionListCreateView.as_view(), name='user-detail'),

    path('posts/', PostListCreateView.as_view(), name='user-list-create'),

    path('like/', LikeView.as_view(), name='like-user'),
    path('likes/received/', LikesReceivedView.as_view(), name='likes-received'),
    path('like/<int:pk>/', UserLikeDetailView.as_view(), name='like-detail'),

    path('matches/', MatchesView.as_view(), name='matches'),

    path('conversations/', ConversationListCreateView.as_view(), name='conversation-list-create'),
    path('conversations/<int:pk>/', ConversationDetailView.as_view(), name='conversation-detail'),

    path('messages/', MessageListCreateView.as_view(), name='message-list-create'),
    path('messages/<int:pk>/', MessageDetailView.as_view(), name='message-detail'),

    path('tests/<int:pk>/', TestDetailView.as_view(), name='test-detail'),
    path('tests/<int:pk>/result/', AssignRandomPersonalityTypeView.as_view(), name='test-result'),

    path('question/', QuestionListCreateView.as_view(), name='question-list-create'),
    path('question/<int:pk>/', QuestionDetailView.as_view(), name='question-detail'),
]
