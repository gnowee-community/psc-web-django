from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Chat(models.Model):
    course = models.ForeignKey('course.Course', on_delete=models.CASCADE, null=True, blank=True)
    sender = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    message = models.TextField(blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    auditory = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"Chat {self.id} - {self.sender} in Course {self.course_id}"


class ChatResponse(models.Model):
    course = models.ForeignKey('course.Course', on_delete=models.CASCADE, null=True, blank=True)
    chat = models.ForeignKey('Chat', on_delete=models.CASCADE, null=True, blank=True)
    sender = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    message = models.TextField(blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    auditory = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"Response {self.id} to Chat {self.chat_id} by {self.sender}"


