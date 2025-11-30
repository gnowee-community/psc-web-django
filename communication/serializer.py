from rest_framework import serializers
from communication import models


class ChatSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Chat
        fields = "__all__"


class ChatResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ChatResponse
        fields = "__all__"
