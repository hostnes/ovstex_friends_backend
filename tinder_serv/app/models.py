from django.utils import timezone

from django.db import models
from django.db.models import Q


class Region(models.Model):
    title = models.CharField(max_length=100)

    def __str__(self):
        return self.title


class Compatibility(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    photo = models.ImageField(upload_to='compatibility')

    def __str__(self):
        return self.title


class User(models.Model):
    name = models.CharField(max_length=50, blank=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=50)
    photo = models.ImageField(upload_to='users', default="users/none_logo.png")
    compatibility = models.ForeignKey('Compatibility', default=1, blank=True, on_delete=models.CASCADE)
    region = models.ForeignKey('Region', blank=True, on_delete=models.CASCADE, null=True)
    gender = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return self.name

    def like_user(self, other_user):
        # Adds a like from this user to another user
        UserLike.objects.get_or_create(from_user=self, to_user=other_user)

    def get_likes_received(self):
        # Users who liked this user
        return User.objects.filter(likes_given__to_user=self)

    def get_mutual_matches(self):
        # Mutual matches
        return User.objects.filter(
            Q(likes_given__to_user=self) & Q(likes_received__from_user=self)
        )


class UserLike(models.Model):
    from_user = models.ForeignKey(User, related_name='likes_given', on_delete=models.CASCADE)
    to_user = models.ForeignKey(User, related_name='likes_received', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    is_already_liked = models.CharField(default="False", max_length=50)

    class Meta:
        unique_together = ('from_user', 'to_user')

    def __str__(self):
        return f"{self.from_user.name} likes {self.to_user.name}"

class Conversation(models.Model):
    participants = models.ManyToManyField(User, related_name="conversations")
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Conversation between {', '.join([user.email for user in self.participants.all()])}"


class Message(models.Model):
    conversation = models.ForeignKey(Conversation, related_name="messages", on_delete=models.CASCADE)
    sender = models.ForeignKey(User, related_name="sent_messages", on_delete=models.CASCADE)
    text = models.TextField()
    sent_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Message from {self.sender.email} at {self.sent_at}"


class Post(models.Model):
    user = models.ForeignKey(User, related_name="posts", on_delete=models.CASCADE)
    text = models.TextField()
    photo = models.ImageField(upload_to='posts', blank=True)
    date_created = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.text

