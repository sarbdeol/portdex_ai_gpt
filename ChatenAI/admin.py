from django.contrib import admin
from .models import ChatLog

@admin.register(ChatLog)
class ChatLogAdmin(admin.ModelAdmin):
    list_display = ('chat_id', 'user_message', 'ai_response', 'timestamp')
    search_fields = ('chat_id', 'user_message')