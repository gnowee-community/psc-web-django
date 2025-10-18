
from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


# Course model as per provided schema
class Course(models.Model):
    STATUS_CHOICES = (
        ("d", "Draft"),
        ("p", "Published"),
        ("a", "Archived"),
    )
    title = models.CharField(max_length=150)
    description = models.TextField(blank=True, null=True)
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default="draft")
    created_by = models.ForeignKey(
        User, on_delete=models.DO_NOTHING, null=True, blank=True, related_name="course_created_by")
    updated_by = models.ForeignKey(
        User, on_delete=models.DO_NOTHING, null=True, blank=True, related_name="course_updated_by")
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.id}: {self.title}"
