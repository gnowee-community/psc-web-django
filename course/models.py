
from django.db import models
from django.contrib.auth import get_user_model

from utils.models import BaseModel

User = get_user_model()


class Course(BaseModel):
    STATUS_CHOICES = (
        ("d", "Draft"),
        ("p", "Published"),
        ("a", "Archived"),
    )
    title = models.CharField(max_length=150)
    description = models.TextField(blank=True, null=True)
    status = models.CharField(
        max_length=1, choices=STATUS_CHOICES, default="d")

    def __str__(self):
        return f"{self.id}: {self.title}"


class CourseTeacher(BaseModel):
    STATUS_CHOICES = (
        ("a", "Active"),
        ("i", "Inactive"),
    )

    course = models.ForeignKey('Course', on_delete=models.CASCADE)
    teacher = models.ForeignKey('staff.Teacher', on_delete=models.CASCADE)
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default="a")

    def __str__(self):
        return f"{self.course} - {self.teacher}"


class Material(BaseModel):
    TYPE_CHOICES = (
        ("document", "Document"),
        ("video", "Video"),
        ("link", "Link"),
        ("slides", "Slides"),
    )
    STATUS_CHOICES = (
        ("a", "Active"),
        ("i", "Inactive"),
    )

    course = models.ForeignKey('Course', on_delete=models.CASCADE)
    teacher = models.ForeignKey('staff.Teacher', on_delete=models.SET_NULL, null=True, blank=True)
    title = models.CharField(max_length=150)
    description = models.TextField(blank=True, null=True)
    file_url = models.CharField(max_length=255, blank=True, null=True)
    upload_date = models.DateTimeField(auto_now_add=True)
    type = models.CharField(max_length=10, choices=TYPE_CHOICES, default="document")
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default="a")

    def __str__(self):
        return f"{self.title} ({self.type})"
