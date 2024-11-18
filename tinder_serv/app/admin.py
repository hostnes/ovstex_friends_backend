from django.contrib import admin
from .models import *


# Регистрация модели User
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['email', 'name', 'gender']  # Поля, отображаемые в списке
    search_fields = ['email', 'name']  # Поля, по которым можно искать
    list_filter = ['gender']  # Фильтры по полям


# Регистрация модели Conversation
@admin.register(Conversation)
class ConversationAdmin(admin.ModelAdmin):
    list_display = ['created_at']
    search_fields = ['participants__email']
    filter_horizontal = ['participants']  # Добавляет удобный выбор участников в админке


# Регистрация модели Message
@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ['conversation', 'sender', 'text', 'sent_at']
    search_fields = ['sender__email', 'text']
    list_filter = ['sent_at']

@admin.register(Compatibility)
class CompatibilityAdmin(admin.ModelAdmin):
    list_display = ['title']  # Поля, отображаемые в списке

@admin.register(Region)
class RegionAdmin(admin.ModelAdmin):
    list_display = ['title']  # Поля, отображаемые в списке

@admin.register(PersonalityType)
class PersonalityTypeAdmin(admin.ModelAdmin):
    list_display = ['name']  # Поля, отображаемые в списке

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['text']  # Поля, отображаемые в списке


@admin.register(UserLike)
class PostAdmin(admin.ModelAdmin):
    list_display = ['from_user', 'to_user']  # Поля, отображаемые в списке



admin.site.register(Test)
admin.site.register(Question)
admin.site.register(AnswerOption)
admin.site.register(TestResult)
