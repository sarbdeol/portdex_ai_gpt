from django.db import models

class ChatLog(models.Model):
    chat_id = models.CharField(max_length=255)
    user_message = models.TextField()
    ai_response = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"ChatLog {self.chat_id} at {self.timestamp}"