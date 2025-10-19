
from django.db import models
from django.contrib.auth import get_user_model

from utils.models import BaseModel

User = get_user_model()


# Course model as per provided schema
class Course(BaseModel):
    STATUS_CHOICES = (
        ("d", "Draft"),
        ("p", "Published"),
        ("a", "Archived"),
    )
    title = models.CharField(max_length=150)
    description = models.TextField(blank=True, null=True)
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default="draft")

    def __str__(self):
        return f"{self.id}: {self.title}"
